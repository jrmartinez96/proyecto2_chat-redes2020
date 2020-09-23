import tkinter as tk
import sleekxmpp
from windows.menu_page import MenuPage
from windows.agregar_contacto_page import AgregarContactoPage
from classes.Contact import Contact
import win10toast


# ------------------- VARIABLES -------------------
class User:
    user = ""
    password = ""
    menuPage: MenuPage
    addContactPage: AgregarContactoPage
    contacts = []
    toaster = win10toast.ToastNotifier()

    def __init__(self, jid, password):
        self.user = jid
        self.password = password
        self.xmpp = sleekxmpp.ClientXMPP(jid, password)
        self.xmpp.add_event_handler("session_start", self.handleXMPPConnected, threaded=True)
        self.xmpp.add_event_handler("message", self.handleIncomingMessage, threaded=True)
        self.xmpp.add_event_handler("presence", self.handleIncomingPresence, threaded=True)

    def run(self):
        a = self.xmpp.connect()
        if a:
            self.xmpp.process()
            print("connected")
            return 1
        return 0

    def disconnect(self):
        self.xmpp.disconnect(wait=True)

    def handleXMPPConnected(self, event):
        print("on_session_start")
        self.menuPage = MenuPage(
            self,
            onclosewindown=self.on_close_menu_window,
            on_refresh_contacts=self.get_roster,
            on_delete_contact=self.on_delete_contact,
            on_add_contact_page=self.open_add_contact_page,
            on_open_chat_page=self.open_chat_window
        )
        self.xmpp.send_presence(pstatus="holis")

        self.menuPage.show_window()

    def handleIncomingMessage(self, message):
        print(message)

        if message["type"] == "chat":
            for contact in self.contacts:
                if contact.jid in message["from"].__str__():
                    contact.add_message(message["body"])
                    self.toaster.show_toast('Chat - Nuevo mensaje de ' + contact.jid, message["body"])

    def handleIncomingPresence(self, presence):
        print(presence)
        if presence["type"] == "subscribe":
            self.xmpp.send_presence(pto=presence["from"], pfrom=presence["to"], ptype="subscribed")
        elif presence["type"] == "unsubscribe":
            self.xmpp.send_presence(pto=presence["from"], pfrom=presence["to"], ptype="unsubscribed")
        elif presence["type"] == "unavailable":
            for contact in self.contacts:
                contact_from = presence["from"].__str__()
                end_index_from = contact_from.index("/")
                contact_from_format = contact_from[0:end_index_from]
                if contact.jid == contact_from_format:
                    contact.status = "No disponible"
        else:
            pos_contact = Contact("", "", "", self.user)
            contact_from = presence["from"].__str__()
            end_index_from = contact_from.index("/")
            contact_from_format = contact_from[0:end_index_from]
            resource = contact_from[end_index_from + 1:len(contact_from)]

            for contact in self.contacts:
                if contact.jid == contact_from_format:
                    pos_contact = contact

            if pos_contact.jid == "":
                self.contacts.append(Contact(contact_from_format, presence["status"], resource=resource, me=self.user))
            else:
                pos_contact.status = presence["status"]
                pos_contact.resource = resource

        self.menuPage.update_roster(self.contacts)


    # --------------------- MENU PAGE FUNCTIONS ---------------------
    def on_close_menu_window(self):
        self.disconnect()
        self.menuPage.destroy_window()

    def get_roster(self):
        def after_get_roster(r):
            print(self.xmpp.roster)
            roster_respose = self.xmpp.roster
            us = list(roster_respose)[0]
            roster = list(roster_respose[us])

            for possible_contact in roster:
                if not roster_respose[us][possible_contact]["subscription"] == "none":
                    if not roster_respose[us][possible_contact]["subscription"] == "from":
                        can_append = True
                        for contact in self.contacts:
                            if contact.jid == possible_contact:
                                can_append = False

                        if can_append:
                            self.contacts.append(Contact(possible_contact, "", "", self.user))

            self.menuPage.update_roster(self.contacts)

        self.xmpp.get_roster(block=False, callback=after_get_roster)

    def probe_contacts(self):
        for contact in self.contacts:
            self.xmpp.send_presence(ptype="probe", pto=contact.jid, pfrom=self.user)

    def on_delete_contact(self, contact):
        end_index = contact.index("---")
        contact_format = contact[0:end_index]
        self.xmpp.send_presence(pto=contact_format, pfrom=self.user, ptype="unsubscribe")

    def open_add_contact_page(self):
        self.addContactPage = AgregarContactoPage(
            self,
            on_add_contact=self.on_add_contact
        )
        self.addContactPage.show_window()

    def open_chat_window(self, contact):
        end_index = contact.index("---")
        contact_format = contact[0:end_index]

        for contactt in self.contacts:
            if (contactt.jid == contact_format):
                contactt.open_chat(on_enviar_mensaje=self.on_enviar_mensaje)


    # --------------------- ADD CONTACT PAGE FUNCTIONS ---------------------
    def on_add_contact(self, contact):
        self.xmpp.send_presence(pto=contact, pfrom=self.user, ptype="subscribe")

    # --------------------- CHAT PAGE FUNCTIONS ---------------------
    def on_enviar_mensaje(self, mensaje, contact):
        self.xmpp.send_message(mto=contact, mbody=mensaje, mtype="chat")


# ------------------------------ LOGIN ------------------------------ #
def loginWindow():
    def on_closing():
        window.destroy()
        print("closing login")

    window = tk.Tk()
    window.geometry('350x200')
    window.title("Chat - Login")
    window.protocol("WM_DELETE_WINDOW", on_closing)

    username = tk.Entry(window, width=15)
    username.insert(0, 'pepe@redes2020.xyz')
    username.grid(column=1, row=0)
    username.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    password = tk.Entry(window, width=15, show="*")
    password.insert(0, 'contra123')
    password.grid(column=1, row=0)
    password.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

    def clickLogin():
        print(username.get())
        user = User(username.get(), password.get())
        connected = user.run()
        if connected == 1:
            window.destroy()


    btn = tk.Button(
        window,
        text="Iniciar sesión",
        command=clickLogin
        )
    btn.grid(column=1, row=1)
    btn.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    window.mainloop()

# ------------------------------ MAIN RUN ------------------------------ #
loginWindow()
