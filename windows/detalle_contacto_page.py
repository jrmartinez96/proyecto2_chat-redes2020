from tkinter import *
from classes.Contact import Contact

class DetalleContactoPage:
    window: Tk

    def __init__(self, contact: Contact):
        self.window = Tk()
        self.window.geometry('300x200')
        self.window.title("Chat - " + contact.jid)

        label_jid = Label(self.window, text="JID: " + contact.jid)
        label_jid.grid(column=1, row=1)

        label_resource = Label(self.window, text="Resource: " + contact.resource)
        label_resource.grid(column=1, row=2)

        label_status = Label(self.window, text="Status: " + contact.status)
        label_status.grid(column=1, row=3)

        label_cantidad_mensajes = Label(self.window, text="Cantidad de mensajes intercambiados: " + len(contact.messages).__str__())
        label_cantidad_mensajes.grid(column=1, row=4)

    def run(self):
        self.window.mainloop()