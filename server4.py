import socket
def Main():
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	hostname = socket.gethostname()
	IPAddr = socket.gethostbyname(hostname)
	port = 80
	s.bind((IPAddr, port))
	s.listen(1)
	c, addr=s.accept()
	print ("Connection from: "+str(addr))
	
	#while True:
	message = str(input("->"))
	print ("sending: "+str(message))
	c.send(message.encode("utf-8"))
	ran = c.recv(1024)
	print ("Data corresponding to sent id is:  " + str(ran.decode("utf-8")))
		#if message=='q':
			#break;
		#message = input("-> ")
	c.close()
if __name__=='__main__':
	Main()