from tkinter import *
import typing


class AgregarContactoPage:
    window: Tk
    contact_entry: Entry
    on_add_contact: typing.Any

    def __init__(self, user, on_add_contact):
        self.user = user
        self.on_add_contact = on_add_contact

        self.window = Tk()
        self.window.geometry('300x200')
        self.window.title("Chat - Agregar contacto")

        # Contact
        self.contact_entry = Entry(self.window, width=15)
        self.contact_entry.insert(0, 'pepe2@redes2020.xyz')
        self.contact_entry.grid(column=1, row=0)
        self.contact_entry.place(relx=0.5, rely=0.1, anchor=CENTER)

        btn = Button(
            self.window,
            text="Agregar contacto",
            command=self.click_add_contact
        )
        btn.grid(column=1, row=1)
        btn.place(relx=0.5, rely=0.4, anchor=CENTER)


    def show_window(self):
        self.window.mainloop()

    def click_add_contact(self):
        contact = self.contact_entry.get()
        if not contact == "":
            self.on_add_contact(contact)
        else:
            print("Campo vacio.")
