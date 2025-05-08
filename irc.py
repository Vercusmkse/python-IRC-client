import socket
import sys
import time

def send_text(sock, text):
    """Send a text to the IRC server."""
    sock.sendall((text + "\r\n").encode())

def connect_to_server(host, port, username):
    """Connect to the IRC server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
   
    # Identify the client
    send_text(sock, f"NICK {username}")
    send_text(sock, f"USER {username} 0 * :{username}")
   
    # Wait for server response
    time.sleep(2)

    return sock

def listen(channel, sock):
    """Listen for messages from the IRC server."""
    send_text(sock, f"JOIN {channel}")

    while True:
        reply = sock.recv(2048).decode("utf-8", errors="ignore")
        if reply:
            if "ERROR :Closing Link" in reply:
                print("Error, couldn't connect.")
                break
           
            # Handle incoming messages
            lines = reply.strip().split("\r\n")
            for line in lines:
                print(line)  # Print raw message for debugging
                if "PRIVMSG" in line:
                    parts = line.split(" ")
                    user = parts[0][1:].split("!")[0]
                    message = " ".join(parts[3:])[1:]
                    print(f"<{user}> {message}")

def send(channel, username, sock):
    """Send messages to the IRC server."""
    send_text(sock, f"JOIN {channel}")

    while True:
        message = input(f"{username} > ")
        if message.lower() == "exit":
            print("Exiting...")
            break
        send_text(sock, f"PRIVMSG {channel} :{message}")

def main():
    if len(sys.argv) != 6:
        print("Usage: python3 irc.py <listen/send> <host> <port> <channel> <username>")
        return

    option = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3])
    channel = sys.argv[4]
    username = sys.argv[5]

    try:
        sock = connect_to_server(host, port, username)

        if option == "listen":
            listen(channel, sock)
        elif option == "send":
            send(channel, username, sock)
        else:
            print("Invalid Option! Choose between listen or send.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()