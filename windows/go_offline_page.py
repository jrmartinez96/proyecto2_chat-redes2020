from tkinter import *

class GoOflinePage:
    window: Tk

    def __init__(self, on_go_offline):
        self.window = Tk()
        self.window.geometry('150x150')
        self.window.title("Chat - ¿Cerrar sesión?")

        label_cerrar = Label(self.window, text="¿Cerrar sesión?")
        label_cerrar.grid(column=1, row=0)
        label_cerrar.place(relx=0.5, rely=0.1, anchor=CENTER)

        btnNo = Button(
            self.window,
            text="No",
            command=self.on_no
        )
        btnNo.grid(column=1, row=1)
        btnNo.place(relx=0.4, rely=0.4, anchor=CENTER)

        btnSi = Button(
            self.window,
            text="Si",
            command=on_go_offline
        )
        btnSi.grid(column=1, row=1)
        btnSi.place(relx=0.7, rely=0.4, anchor=CENTER)

    def run(self):
        self.window.mainloop()

    def on_no(self):
        self.window.destroy()