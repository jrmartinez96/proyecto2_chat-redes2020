from tkinter import *
import typing

class CambiarEstadoPage:
    window: Tk
    estado_entry: Entry
    on_change: typing.Any

    def __init__(self, on_change):
        self.on_change = on_change

        self.window = Tk()
        self.window.geometry('300x200')
        self.window.title("Chat - Cambiar estado")

        label_estado = Label(self.window, text="Estado de usuario")
        label_estado.grid(column=1, row=0)
        label_estado.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.estado_entry = Entry(self.window, width=15)
        self.estado_entry.insert(0, '')
        self.estado_entry.grid(column=2, row=0)
        self.estado_entry.place(relx=0.5, rely=0.3, anchor=CENTER)

        btn = Button(
            self.window,
            text="Cambiar estado",
            command=self.change_state()
        )
        btn.grid(column=1, row=1)
        btn.place(relx=0.5, rely=0.6, anchor=CENTER)

    def run(self):
        self.window.mainloop()

    def change_state(self):
        print(self.estado_entry.get())