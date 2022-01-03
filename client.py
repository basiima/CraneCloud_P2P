from constants import *

class Client:
    def __init__(self, addr):
       self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
       self.s.connect((addr, PORT))
       self.previous_data = None

       print("Client Connected succesfully!")

       i_thread = threading.Thread(target=self.send_data)
       i_thread.daemon = True
       i_thread.start()

       while True:
        r_thread = threading.Thread(target=self.recieve_message)
        r_thread.start()
        r_thread.join()

        data = self.recieve_message()

        if not data:
           print("Unable to establish connection.....")
           break

        elif data[0:1] == b'\x11':
            print("Getting Data...")
            self.update_peers(data[1:])

        self.send_data()


    def update_peers(self, peers):
        p2p.peers = str(peers, "utf-8").split(',')[:-1]


    def send_disconnect_signal(self):
       print("Server Disconnected!")
       self.s.send("q".encode('utf-8'))
       sys.exit()

    def recieve_message(self):
       try:
           data = self.s.recv(SIZE)
           print(data.decode())
           return data

       except KeyboardInterrupt:
           self.send_disconnect_signal()


    def send_data(self):
        try:
            message = input("Please enter a message: ")
            self.s.send(message.encode())
            
        except KeyboardInterrupt as e:
            self.send_disconnect_signal()
            return
