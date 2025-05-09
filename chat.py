import socket
import threading
#import termcolor
import os
version = 0.1
HOST = '0.0.0.0'  # Listen for messages from any device
PORT = 6969       # Port for communication
alias = "newko" # User alias
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
def refresh():
    clear_screen()
    cleaned_lines = []
    for line in messages:
        if line.strip():
            cleaned_lines.append(line)
    for i in cleaned_lines:
        print(i)

messages = ["################################",
            "###:3:3:3:3###:3:3:3###:3:3#####",
            "######:3#####:3########:3##:3###",
            "######:3#####:3########:3:3#####",
            "######:3######:3:3:3###:3#######",
            "################################",
            "Trans-fem Communication Protocol\n"]
hosts = []
def receive_messages():
    global messages
    """Continuously listens for incoming messages."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind(("", PORT))
        messages.append(f"Listening for broadcasts on port {PORT}...")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            tcp_socket.bind((HOST, PORT))
            tcp_socket.listen()
            messages.append(f"Listening for private messages on {HOST}:{PORT}...")
            

            while True:
                # Handle broadcast messages
                udp_socket.settimeout(0.5)
                try:
                    data, addr = udp_socket.recvfrom(1024)
                    if data:
                        if "Signing on" in data.decode():
                            messages.append("hosts:")
                            broadcast("5555"+alias)
                            
                            #messages.append("sending alias to new host")
                        elif "5555" in data.decode():
                            messages.append(data.decode().replace("5555", "").split(":")[0]+"("+addr[0]+")")
                            
                        else:   
                            messages.append(f"[GC] {addr[0]}/{data.decode()}")
                        refresh()
                except socket.timeout:
                    pass

                # Handle private messages
                tcp_socket.settimeout(0.5)
                try:
                    conn, addr = tcp_socket.accept()
                    with conn:
                        data = conn.recv(1024)
                        if data:
                            if data.startswith(b"[FILE]"):  # Identify that it's a file
                                file_info = data.split(b"\n", 1)
                                file_name = file_info[0][6:].decode()  # Extract filename from header
                                file_content = file_info[1]

                                with open(f"received_{file_name}", "wb") as file:
                                    file.write(file_content)  # Write the first chunk

                                    while True:
                                        chunk = conn.recv(1024)
                                        if not chunk:
                                            break  # End loop when file transfer completes
                                        file.write(chunk)  # Write subsequent chunks

                                messages.append(f"[FILE RECEIVED] {file_name}")
                                refresh()

                            else:
                                messages.append(f"[PM] {addr[0]}/{data.decode()}")
                            refresh()
                            conn.sendall(b":3")
                except socket.timeout:
                    pass

def send_pm(message, recipient='127.0.0.1'):
    """Sends a private message to the specified recipient."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((recipient, PORT))
            client_socket.sendall(f"{alias}: {message}".encode())
            response = client_socket.recv(1024)
            print(f"[PM ACK] {response.decode()}", "green")
        except socket.error:
            messages.append(f"Error: Unable to connect to {recipient}")
def send_file(file_path, recipient='127.0.0.1'):
    """Send a file in chunks with an explicit header."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((recipient, PORT))
            with open(file_path, "rb") as file:
                client_socket.sendall(f"[FILE]{os.path.basename(file_path)}\n".encode())  # Send header first
                
                while chunk := file.read(1024):
                    client_socket.sendall(chunk)  # Send the file content in chunks
                
            print(f"File '{file_path}' sent successfully.")
        except socket.error:
            print(f"Error: Unable to connect to {recipient}")



def broadcast(message):
    """Sends a broadcast message to all devices on the network."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender_socket:
        sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sender_socket.sendto(f"{alias}: {message}".encode(), ("255.255.255.255", PORT))

# Start listening for messages in a separate thread
threading.Thread(target=receive_messages, daemon=True).start()
# host discovery

# Interactive messaging loop
while True:
    mode = input("\nEnter '1' for PM, '2' for broadcast, or 'exit' to quit: ")
    if mode == "exit":
        messages.append("Exiting chat...")
        break
    elif mode == "1":
        recipient = input("Enter recipient IP: ")
        while True:

            message = input("")
            if message == "0":
                send_pm("Connection terminated", recipient)
                break
            if "/" in message:
                filename = message.replace("/", "").split()
                send_file(filename[0], recipient)
            else:
                send_pm(message, recipient)
    elif mode == "2":
        broadcast("Signing on")
        while True:
            
            message = input("")
            if message == "0":
                broadcast("Signing off")
                break
            if "/" in message:
                filename = message.replace("/", "").split()
                send_file(filename[0], filename[1])
            else:
                broadcast(message)