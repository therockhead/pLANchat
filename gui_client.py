import customtkinter as ctk
import socket
import threading
import pickle
from cryptography.fernet import Fernet, InvalidToken
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from huffman import encode, decode


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") # can be green also :3


class LoginPopup(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Secure Chat Login")
        self.geometry("800x650")
        self.resizable(False, False)

        self.username = None
        self.fernet = None

        ctk.CTkLabel(self, text="Username:").pack(pady=(15, 5))
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.pack(padx=20)

        ctk.CTkLabel(self, text="Encryption Key:").pack(pady=(15, 5))
        self.key_entry = ctk.CTkEntry(self, show='*')
        self.key_entry.pack(padx=20)

        ctk.CTkButton(self, text="Connect", command=self.submit).pack(pady=20)

    def submit(self):
        username = self.username_entry.get()
        key = self.key_entry.get()

        try:
            fernet = Fernet(key.encode())
        except Exception:
            ctk.CTkMessagebox(title="Invalid Key", message="Please enter a valid Fernet key.", icon="cancel")
            return

        self.username = username
        self.fernet = fernet
        self.destroy()


class ChatClient(ctk.CTk):
    def __init__(self, username, fernet):
        super().__init__()
        self.username = username
        self.fernet = fernet

        self.title(f"Huffman Secure Chat - {username}")
        self.geometry("800x650")
        self.resizable(False, False)

        # Logs & chart tracking
        self.chat_log = []
        self.orig_sizes = []
        self.comp_sizes = []
        self.msg_count = 0

        # Chat Display
        self.chat_area = ctk.CTkTextbox(self, width=760, height=300, font=("Consolas", 14), state='disabled')
        self.chat_area.pack(padx=10, pady=10)

        # Message entry and buttons
        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(pady=5, padx=10, fill='x')

        self.entry = ctk.CTkEntry(entry_frame, placeholder_text="Type your message...")
        self.entry.pack(side=ctk.LEFT, fill='x', expand=True, padx=(0, 10), pady=5)
        self.entry.bind("<Return>", self.send_message)

        ctk.CTkButton(entry_frame, text="Send", command=self.send_message).pack(side=ctk.LEFT)

        # Buttons: Save chart & log
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=5)

        ctk.CTkButton(btn_frame, text="Save Chart", command=self.save_chart).pack(side=ctk.LEFT, padx=10)
        ctk.CTkButton(btn_frame, text="Save Log", command=self.save_log).pack(side=ctk.LEFT, padx=10)
        # self.theme_toggle_btn = ctk.CTkButton(btn_frame, text="Toggle Theme", command=self.toggle_theme)
        # self.theme_toggle_btn.pack(side=ctk.LEFT, padx=10)

        # Compression chart
        self.fig, self.ax = plt.subplots(figsize=(5.5, 2.5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(pady=10)
        self.ax.set_title("Compression Per Message")
        self.ax.set_ylabel("Bits")
        self.ax.set_xlabel("Messages")

        # Socket Setup
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1', 5555))
        threading.Thread(target=self.receive_messages, daemon=True).start()


    # def toggle_theme(self):
    #     current_mode = ctk.get_appearance_mode()
    #     new_mode = "light" if current_mode == "dark" else "dark"
    #     self.after_idle(lambda: ctk.set_appearance_mode(new_mode))


    def send_message(self, event=None):
        msg = self.entry.get()
        if msg:
            encoded_msg, code_map, original_bits, compressed_bits = encode(msg)
            encrypted = self.fernet.encrypt(encoded_msg.encode())

            message_pack = {
                'username': self.username,
                'data': encrypted,
                'code_map': code_map,
                'original_bits': original_bits,
                'compressed_bits': compressed_bits
            }

            self.sock.send(pickle.dumps(message_pack))
            self.display_message(f"You: {msg}")
            self.display_message(f"[Compression] {original_bits} → {compressed_bits} bits | Saved: {100 - (compressed_bits * 100) // original_bits}%")
            self.entry.delete(0, ctk.END)
            self.update_chart(original_bits, compressed_bits)

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
        self.chat_area.configure(state='normal')
        self.chat_area.insert(ctk.END, msg + "\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(ctk.END)

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



# 🔰 Main App Entry Point
if __name__ == "__main__":
    login = LoginPopup()
    login.mainloop()

    if login.username and login.fernet:
        app = ChatClient(login.username, login.fernet)
        app.mainloop()
