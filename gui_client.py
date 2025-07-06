import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, END
import pickle
from huffman import encode, decode


def ask_username():
    popup = tk.Tk()
    popup.title("Enter Username")
    popup.geometry("300x100")

    label = tk.Label(popup, text="Enter your username:")
    label.pack(pady=5)

    username_entry = tk.Entry(popup)
    username_entry.pack()

    def confirm():
        popup.username = username_entry.get()
        popup.destroy()

    tk.Button(popup, text="OK", command=confirm).pack(pady=5)
    popup.mainloop()
    return getattr(popup, 'username', 'Anonymous')



class ChatClient:
    def __init__(self, master, username):
        self.master = master
        self.username = username;
        self.master.title(f"Chat - {self.username}")

        # Chat window
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=20, state='disabled')
        self.chat_area.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Input field
        self.entry = tk.Entry(master, width=40)
        self.entry.grid(row=1, column=0, padx=10, pady=5)
        self.entry.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=5)

        # Socket connection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.sock.connect(('127.0.0.1', 5555))
        self.sock.connect(('192.168.0.104', 5555))


        # Start receiving thread
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, event=None):
        msg = self.entry.get()
        if msg:
            encoded_msg, code_map = encode(msg)
            message_pack = {
                'username': self.username,  # ✅ INCLUDE THIS
                'data': encoded_msg,
                'code_map': code_map
            }
            self.sock.send(pickle.dumps(message_pack))
            self.display_message(f"You: {msg}")
            self.entry.delete(0, END)


    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                message_pack = pickle.loads(data)
                decoded_msg = decode(message_pack['data'], message_pack['code_map'])
                sender = message_pack.get('username', 'Unknown')
                self.display_message(f"{sender}: {decoded_msg}")
            except:
                break


    def display_message(self, msg):
        self.chat_area.config(state='normal')
        self.chat_area.insert(END, msg + '\n')
        self.chat_area.config(state='disabled')
        self.chat_area.see(END)

if __name__ == "__main__":
    username = ask_username()
    root = tk.Tk()
    client = ChatClient(root, username)
    client.username = username  # Attach to client instance
    root.mainloop()

