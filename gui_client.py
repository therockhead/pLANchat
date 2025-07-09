import socket
import threading
from cryptography.fernet import Fernet, InvalidToken
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import scrolledtext, END
import pickle
from huffman import encode, decode
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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


class LoginPopup:
    def __init__(self, master):
        self.master = master
        self.master.title("Secure Chat Login")
        self.username = None
        self.fernet = None

        tk.Label(master, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        tk.Label(master, text="Encryption Key:").pack(pady=5)
        self.key_entry = tk.Entry(master, show='*')
        self.key_entry.pack()

        tk.Button(master, text="Connect", command=self.submit).pack(pady=10)

    def submit(self):
        username = self.username_entry.get()
        key = self.key_entry.get()

        try:
            fernet = Fernet(key.encode())  
        except Exception:
            messagebox.showerror("Invalid Key", "Please enter a valid Fernet key.")
            return

        self.username = username
        self.fernet = fernet
        self.master.destroy()


class ChatClient:
    def __init__(self, master, username, fernet):
        self.master = master
        self.username = username
        self.fernet = fernet

        master.title(f"Secure Chat - {username}")

        # saving each line of chat
        self.chat_log = []  # Store each line of chat

        # Chart part
        self.orig_sizes = []
        self.comp_sizes = []
        self.msg_count = 0

        # GUI layout
        self.chat_area = tk.Text(master, state='disabled', width=50, height=20)
        self.chat_area.pack(padx=10, pady=10)

        self.entry = tk.Entry(master, width=40)
        self.entry.pack(side=tk.LEFT, padx=10)
        self.entry.bind("<Return>", self.send_message)

        # my buttons
        tk.Button(master, text="Send", command=self.send_message).pack(side=tk.LEFT)
        tk.Button(master, text="Save Chart", command=self.save_chart).pack(side=tk.LEFT, padx=5)
        tk.Button(master, text="Save Log", command=self.save_log).pack(side=tk.LEFT)

        # Bar Chart Setup
        self.fig, self.ax = plt.subplots(figsize=(5, 2))
        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas.get_tk_widget().pack(pady=10)
        self.ax.set_title("Compression Per Message")
        self.ax.set_ylabel("Bits")
        self.ax.set_xlabel("Messages")

        # Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1', 5555))  
        threading.Thread(target=self.receive_messages, daemon=True).start()



    def send_message(self, event=None):
        msg = self.entry.get()
        if msg:
            encoded_msg, code_map, original_bits, compressed_bits = encode(msg)
            encrypted = self.fernet.encrypt(encoded_msg.encode())

            message_pack = {
                'username': self.username,
                'data': encrypted,
                'code_map': code_map
            }

            self.sock.send(pickle.dumps(message_pack))
            self.display_message(f"You: {msg}")
            self.display_message(f"[Compression] {original_bits} → {compressed_bits} bits | Saved: {100 - (compressed_bits * 100) // original_bits}%")
            self.entry.delete(0, tk.END)

            # update in the bar chart
            self.update_chart(original_bits, compressed_bits) #updates the bar chart after every send operation :)

    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(4096)
                message_pack = pickle.loads(data)

                encrypted = message_pack['data']
                decrypted = self.fernet.decrypt(encrypted).decode()
                decoded = decode(decrypted, message_pack['code_map'])
                sender = message_pack.get('username', 'Unknown')

                self.display_message(f"{sender}: {decoded}")
                if 'original_bits' in message_pack and 'compressed_bits' in message_pack:
                    orig = message_pack['original_bits']
                    comp = message_pack['compressed_bits']
                    saved = 100 - (comp * 100 // orig)
                    self.display_message(f"[Compression] {orig} → {comp} bits | Saved: {saved}%")
                    self.update_chart(orig, comp)
            except InvalidToken:
                self.display_message("[ERROR] Invalid decryption key!")
            except:
                break

    def display_message(self, msg):
        self.chat_log.append(msg)
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, msg + "\n")
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def update_chart(self, orig, comp):
        self.msg_count += 1
        self.orig_sizes.append(orig)
        self.comp_sizes.append(comp)

        self.ax.clear()
        self.ax.bar(range(self.msg_count), self.orig_sizes, label="Original", color='skyblue')
        self.ax.bar(range(self.msg_count), self.comp_sizes, label="Compressed", color='orange')

        self.ax.set_title("Compression Per Message")
        self.ax.set_ylabel("Bits")
        self.ax.set_xlabel("Messages")
        self.ax.legend()

        self.canvas.draw()

    def save_chart(self):
        filename = f"compression_chart.png"
        self.fig.savefig(filename)
        self.display_message(f"[INFO] Chart saved as {filename}")

    def save_log(self):
        filename = f"chat_history_{self.username}.hufflog"
        with open(filename, 'w', encoding='utf-8') as f:
            for line in self.chat_log:
                f.write(line + '\n')
        self.display_message(f"[INFO] Chat log saved as {filename}")


if __name__ == "__main__":
    login_root = tk.Tk()
    login_gui = LoginPopup(login_root)
    login_root.mainloop()

    # Launch chat only if valid
    if login_gui.username and login_gui.fernet:
        chat_root = tk.Tk()
        app = ChatClient(chat_root, login_gui.username, login_gui.fernet)
        chat_root.mainloop()


