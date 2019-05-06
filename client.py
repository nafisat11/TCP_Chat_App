import sys 
import socket
import time 
import select

program_name = sys.argv[0]
host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
welcome_msg = "Hello, {name}!".format(name = host_name)


if (len(sys.argv) < 3 or (sys.argv[3] == '--h' or sys.argv[3] == '--help')):
	print('''Usage: python3 client.py hostname PORT [OPTION]\nThis is a messaging application.\n\n
  -e, --exit      exit the application\n
  -h, --help      display this help 
  -i, --ip        display IP address of server
  -t, --tcp       Transmission Control Protocol. Use if you require high reliability. Slower transmission time.\n
  -u, --udp       User Datagram Protocol. Use if you require fast, efficient transmission. 
		 ''')
	sys.exit(1)


if (sys.argv[3] == '-i' or sys.argv[3] == '--ip'):
	print("IP address of the server is: ", ip)

host = sys.argv[1]
port = sys.argv[2]


def tcp_com():
	try:
		s_tcp = socket.socket(AF_INET, SOCK_STREAM)
		time.sleep(2)
	except:
		print("Failed to create socket")
		sys.exit()

	try:
		s_tcp.connect((host, port))

	except:
		print("Unable to connect to socket")
		sys.exit

	print(welcome_msg + "Connected to TCP server. You can now start sending messages.")

	while 1:
		reading, writing, s_error = select.select([sys.stdin, s_tcp], [], [])

		for s in reading:
			if s == s_tcp:
				received_data = s_tcp.recv(1024)

				if not received_data:
					print("Disconnected from server\nPlease exit")
				else:
					sys.stdout(received_data)
					

			else:
				msg = input("Enter message to send: ")
				s_tcp.send(msg)
				print("Server reply: " + received_data[0])



def udp_com():
	try:
		s_udp = socket.socket(AF_INET, SOCK_DGRAM)
		time.sleep(2)
	except:
		print("Failed to create socket")
		sys.exit()


	print(welcome_msg + "Connected to UDP server. You can now start sending messages.")

	while 1:
		msg = input("Enter message to send: ")
		s_udp.sendto(msg, (host, port))
		received_data = s_udp.recvfrom(1024)
		print("Server reply: " + received_data[0])


if (sys.argv[3] == '-t' or sys.argv[3] == '--tcp'):
	tcp_com()

if (sys.argv[3] == '-u' or sys.argv[3] == '--udp'):
	udp_com()

if (sys.argv[3] == '-e' or sys.argv[3] == '--exit'):
	sys.exit()






