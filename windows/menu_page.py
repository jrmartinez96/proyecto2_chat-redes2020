from tkinter import *
import typing


class MenuPage:
    window: Tk
    contacts: Listbox
    on_del_con: typing.Any
    on_add_con: typing.Any
    on_open_chat: typing.Any

    def __init__(self, user, onclosewindown, on_refresh_contacts, on_delete_contact, on_add_contact_page, on_open_chat_page):
        self.user = user
        self.on_del_con = on_delete_contact
        self.on_add_con = on_add_contact_page
        self.on_open_chat = on_open_chat_page

        self.window = Tk()
        self.window.geometry('500x500')
        self.window.title("Chat - Login")
        self.window.protocol("WM_DELETE_WINDOW", onclosewindown)

        # Contacts
        label_contacts = Label(self.window, text="Contactos")
        label_contacts.grid(column=0, row=0)
        self.contacts = Listbox(self.window, width=60)
        self.contacts.grid(row=1, column=0)

        # Buttons Contacts
        frame_contacts = Frame(self.window)
        frame_contacts.grid(column=0, row=2)

        refresh_contacts_button = Button(frame_contacts, text="Refresh", command=on_refresh_contacts)
        refresh_contacts_button.grid(column=0, row=0)

        chat_button = Button(frame_contacts, text="Abrir chat", command=self.click_chat_button)
        chat_button.grid(column=1, row=0)

        delete_user_button = Button(frame_contacts, text="Eliminar usuario", command=self.click_delete_contact)
        delete_user_button.grid(column=2, row=0)

        add_user_button = Button(frame_contacts, text="Agregar usuario", command=self.click_agregar_contacto)
        add_user_button.grid(column=3, row=0)

    def show_window(self):
        self.window.mainloop()

    def destroy_window(self):
        self.window.destroy()

    def update_roster(self, roster):
        self.contacts.delete(0, END)
        for contact in roster:
            self.contacts.insert(END, contact.jid + "---- " + contact.status)

    def click_chat_button(self):
        curse_selection = self.contacts.curselection()
        if not curse_selection.__str__() == "()":
            contact = self.contacts.get(curse_selection)
            self.on_open_chat(contact)
        else:
            print("No contact selected")

    def click_delete_contact(self):
        curse_selection = self.contacts.curselection()
        if not curse_selection.__str__() == "()":
            contact = self.contacts.get(curse_selection)
            self.on_del_con(contact)
        else:
            print("No contact selected")

    def click_agregar_contacto(self):
        self.on_add_con()
