(*This Project is under development*) 🛠️
--------------------------------------------------------------------------------

# 🔐 pLANchat - A LAN based chat system using Huffman Coding - A lossless data compression algorithm


This is a secure, real-time messaging app built using Python that combines:
- Text compression using **Huffman Coding**
- End-to-end encryption with **Fernet**
- A **modern GUI** using `customtkinter`
- Live **compression analytics** (bar charts)
- Chat log saving, image export, and more
- more features will be added next....

> It’s built with simplicity, security, and fun in mind — ideal for demonstrating Data Structures (DSA) in a real-world use case.

---

## Inspiration
![image](https://github.com/user-attachments/assets/ff571ff8-aba6-4032-b665-f9d9959b8510)

A few years back, I watched a TV series named 'Silicon Valley'. In that series, Richard developed a loss less data compression algorithm and later he with his other friends, 
started the company named 'Pied Piper'. The series focuses on Richard's and his team's struggles to maintain the company while facing competition from larger entities.

That was my inspiration. I found data compression interesting. I wanted to make some projects implementing this kind of algorithms. And eventually, I got the chance to do something like that. :3 


##  DSA Concepts & Structures Used

This project is deeply grounded in core **Data Structures and Algorithms**, applied through Huffman Coding and real-time encrypted communication.

### Huffman Coding – Core DSA Concepts used

| Concept            | Data Structure Used     | Why Used                                                  |
|--------------------|-------------------------|------------------------------------------------------------|
| Frequency Table    | `dict` (HashMap)        | To count the frequency of each character in O(n) time      |
| Priority Queue     | `heapq` (Min-Heap)      | To efficiently pick the least frequent nodes during merge |
| Binary Tree        | `Node` class            | To build the Huffman Tree (recursive structure)            |
| Bit Mapping        | `dict` (Code Map)       | To map characters to binary Huffman codes                  |
| Tree Traversal     | DFS (recursion)         | For generating prefix codes from the Huffman Tree          |

### Algorithms in Action

- **Greedy Algorithm**: Huffman coding uses a greedy strategy to combine least frequent characters first
- **DFS (Depth-First Search)**: Recursively generates binary codes from the tree
- **Min-Heap Operations**: Used to always access the smallest frequency nodes in O(log n) time

> 📂 All these are implemented in the `huffman.py` file — with clarity and pure logic to demonstrate DSA skills in action.

---

## Project Highlights

- **Real-time Chat:** Communicate between two users over a local network.
- **Encryption:** Messages are encrypted using a user-supplied Fernet key.
- **Huffman Coding:** Each message is compressed using Huffman algorithm before encryption.
- **Live Analytics:** Bar chart showing original vs compressed message sizes.
- **Chat History:** Save conversations as `.hufflog` files.
- **Chart Export:** Save compression chart as a `.png` image.
- **User Authentication:** Users input a username and encryption key before entering the chat.

---

## Technologies Used

| Area             | Technology         |
|------------------|--------------------|
| GUI              | customtkinter      |
| Networking       | socket, threading  |
| Encryption       | cryptography.Fernet|
| Compression Algo | Custom Huffman Code|
| Data Serialization | pickle           |
| Visualization    | matplotlib         |

---

## File Structure
```bash
huffman_chat_app/
│
├── server.py           # Handles clients, decompresses incoming messages
├── gui_client.py           # Sends compressed messages to server
├── huffman.py          # All Huffman compression/decompression logic
└── encryption-key.py            # Optional helper functions (for encoding/decoding binary)
└── requirements.txt            # libraries needed to run
```
## How It Works

### 1. Login
- A GUI login screen prompts the user for:
  - Username
  - Encryption key (Fernet key)
  - will be modified later .....

### 2. Chat Interface
- Users can send and receive encrypted messages.
- Messages are first compressed using **Huffman Coding**, then encrypted with **Fernet**, and finally sent over the socket.
- Received messages are decrypted, decoded, and displayed in a chat window.

### 3. Compression Analytics
- A bar chart updates in real-time to compare:
  - Original message size (in bits)
  - Compressed message size
- This provides visual feedback on how efficient the Huffman compression is per message.

---

## 🖼 Screenshots



---

## 🐍 Python Setup Guide (For First-Time Users)

Before running the chat app, you need to make sure Python is properly installed on your computer.

### Check if Python is Already Installed
```bash
python --version
```
If you see something like: You are good to Go... 

Otherwise-
### Install Python
Go to the official Python website
=> https://www.python.org/downloads/

Download the latest version of Python (preferably 3.10+)

✔️ **IMPORTANT**:

 During installation, check the box that says: ```Add Python to PATH```

Finish the installation.


##  How to Run the Project

### 1. Clone the repo

```bash
git clone https://github.com/therockhead/pLANchat.git
cd pLANchat
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the server
```bash
python3 server.py
```
or (if first one doesn't work) -
```bash
python server.py
```

### 4. Run the GUI file 
```bash
python gui_client.py
```
or (if first one doesn't work) -
```bash
python3 gui_client.py
```

Another user (user2) should also follow the steps from 1 to 4 and should enter the same encryption key to chat with the user (user1)
