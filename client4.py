import socket
def Main():
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	#hostname = socket.gethostname()
	#IPAddr = socket.gethostbyname(hostname)
	host = input(str("Please enter the ipv4 address of the sender: "))
	port = 80
	s.connect((host,port))
	data = s.recv(1024)
	message = {'1':'saloni','2':'himanshi','3':'rajneesh bhaiya'}
	#while data != b'q':

	print("Received from server: "+str(data.decode("utf-8")))
	#message = 'himanshi'
	s.send(message[data.decode("utf-8")].encode("utf-8"))
	#data = s.recv(1024)
	s.close()
if __name__ == '__main__':
	Main()


 