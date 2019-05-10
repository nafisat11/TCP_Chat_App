import sys
import socket
import argparse
import select

host_name = socket.gethostname()
ip_address = socket.gethostbyname(host_name)
welcome_msg = "Hello, {name}!".format(name=host_name)

parser = argparse.ArgumentParser(description="This is a TCP/UDP messaging application.")
parser.add_argument("hostname", help="enter hostname of server")
parser.add_argument("port", type=int, help="enter server port number")
parser.add_argument(
    "-i", "--ip", help="display IP address of server", action="store_true"
)
parser.add_argument(
    "-t",
    "--tcp",
    help="Transmission Control Protocol. Use if you require high reliability. Slower transmission time",
    action="store_true",
)
parser.add_argument(
    "-u",
    "--udp",
    help="User Datagram Protocol. Use if you require fast, efficient transmission",
    action="store_true",
)
args = parser.parse_args()

host = args.hostname
port = args.port


def tcp_com():
    try:
        s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print("Failed to create socket")
        sys.exit(1)

    try:
        s_tcp.connect((host, port))

    except socket.gaierror:
        print("Unable to connect to socket")
        sys.exit(1)

    print(welcome_msg + " Connected to TCP server. You can now start sending messages.")

    while True:
        reading_data, writing_data, socket_error = select.select(
            [sys.stdin, s_tcp], [], []
        )

        for s in reading_data:
            if s == s_tcp:
                received_data = s_tcp.recv(1024).decode()

                if not received_data:
                    print("\nDisconnected from server. Please start a new session")
                    sys.exit(1)
                else:
                    sys.stdout.write("Server reply: " + received_data)
                    sys.stdout.flush()

            else:
                msg = sys.stdin.readline()
                s_tcp.send(msg.encode())
                sys.stdout.flush()


def udp_com():
    try:
        s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print("Failed to create socket")
        sys.exit(1)

    print(welcome_msg + " Connected to UDP server. You can now start sending messages.")

    while 1:
        msg = input("Enter message to send: ")
        s_udp.sendto(msg.encode(), (host, port))
        received_data = s_udp.recvfrom(1024).decode()
        print("Server reply: " + received_data)


def main():

    if args.ip:
        print("IP address of the server is: ", ip_address)

    if args.tcp:
        tcp_com()

    if args.udp:
        udp_com()


if __name__ == "__main__":
    main()
