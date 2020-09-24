from tkinter import *

class ChatPage:
    """Clase de la pantalla de Chat

        Attributes:
            window              instancia de la pantalla tkinter
            message_entry       Entrada de texto de mensaje
            messages_list       Lista de mensajes

    """
    window: Tk
    message_entry: Entry
    messages_list: Listbox


    def definewindow(self, on_enviar_mensaje, contact_name, on_add_self_message):
        self.window = Tk()
        self.window.geometry('500x500')
        self.window.title("Chat - Chat " + contact_name)

        # Contacts
        label_chat = Label(self.window, text="Chat - " + contact_name)
        label_chat.grid(column=0, row=0)
        self.messages_list = Listbox(self.window, width=60)
        self.messages_list.grid(row=1, column=0)

        # Buttons Contacts
        frame_input = Frame(self.window)
        frame_input.grid(column=0, row=2)

        message_entry = Entry(frame_input, width=15)
        message_entry.grid(column=0, row=0)

        def enviarmsj():
            mensaje = message_entry.get()
            on_enviar_mensaje(mensaje=mensaje, contact=contact_name) # enviar al sevidor
            on_add_self_message(message=mensaje) # agregar al gui

        chat_button = Button(frame_input, text="Enviar mensaje", command=enviarmsj)
        chat_button.grid(column=1, row=0)

    def run(self, on_enviar_mensaje, contact_name, on_add_self_message, messages):
        self.definewindow(on_enviar_mensaje=on_enviar_mensaje, contact_name=contact_name, on_add_self_message=on_add_self_message)
        self.on_update_messages(messages)
        self.window.mainloop()

    def on_update_messages(self, messages):
        self.messages_list.delete(0, END)
        for message in messages:
            self.messages_list.insert(END, message)
