import sys 
import socket

program_name = sys.argv[0]
parameters = sys.argv[1:]
user_name = socket.gethostname()
welcome_msg = "Hello, {name}!. This is a messaging application. Please enter your network information.".format(name = user_name)


if len(sys.argv) < 1:
	print("Please enter more arguments")
	sys.exit(1)

else:
	print(welcome_msg)






