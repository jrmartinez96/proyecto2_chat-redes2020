from windows.chat_page import ChatPage

class Contact:
    jid = ""
    status = ""
    resource = ""
    messages = []
    chat_page = ChatPage()
    me = ""

    def __init__(self, jid, status, resource, me):
        self.jid = jid
        self.status = status
        self.resource = resource
        self.me = me

    def set_jid(self, jid):
        self.jid = jid

    def set_status(self, status):
        self.status = status

    def add_message(self, message):
        self.messages.append(self.jid + ": " + message)
        self.chat_page.on_update_messages(self.messages)

    def open_chat(self, on_enviar_mensaje):
        self.chat_page.run(
            on_enviar_mensaje=on_enviar_mensaje,
            contact_name=self.jid,
            on_add_self_message=self.on_add_self_message,
            messages=self.messages
        )

    def on_add_self_message(self, message):
        self.messages.append(self.me + ": " + message)
        self.chat_page.on_update_messages(self.messages)
