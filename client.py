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

    epoll_fd = select.epoll()
    epoll_fd.register(s_tcp.fileno(), select.EPOLLIN)
    epoll_fd.register(0, select.EPOLLIN)

    try:
        while True:
            events = epoll_fd.poll(1)
            for fd, event in events:
                if fd == s_tcp.fileno():
                    received_data = s_tcp.recv(1024).decode()

                    if not received_data:
                        sys.stdout.write(
                            "\nDisconnected from server. Please start a new session.\n"
                        )
                        sys.exit(1)

                    elif event & select.EPOLLIN:
                        sys.stdout.write("Server reply: " + received_data)
                        sys.stdout.flush()

                elif event & select.EPOLLHUP:
                    epoll_fd.unregister(fd)
                    epoll_fd.close()

                msg = sys.stdin.readline()
                s_tcp.send(msg.encode())
                sys.stdout.flush()

    finally:
        epoll_fd.unregister(s_tcp.fileno())
        epoll_fd.unregister(0)
        epoll_fd.close()


def udp_com():
    try:
        s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print("Failed to create socket")
        sys.exit(1)

    print(welcome_msg + " Connected to UDP server. You can now start sending messages.")

    while True:
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
