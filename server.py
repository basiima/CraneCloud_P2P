from constants import *
import os.path
from os import path

class Server:
    def __init__(self, sample_msg):
        try:
            self.sample_msg = sample_msg

            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.s.bind((HOST, PORT))

            self.s.listen(1)

            self.networks = []

            self.peers = []

            print("Server Started!")

            self.run()
        except Exception as e:
            sys.exit()


    def run(self):
        while True:
            network, packet = self.s.accept()
            self.peers.append(packet)
            print("LIST OF PEERS: {}".format(self.peers) )
            self.send_peers()
            c_thread = threading.Thread(target=self.controller, args=(network, packet))
            c_thread.daemon = True
            c_thread.start()
            self.networks.append(network)
            print("{}, connected".format(packet))
            print("-" * 50)


    def send_peers(self):
        peer_list = ""
        for peer in self.peers:
            peer_list = peer_list + str(peer[0]) + ","

        for network in self.networks:
            data = PEER_BYTE + bytes(peer_list, 'utf-8')
            network.send(PEER_BYTE + bytes(peer_list, 'utf-8'))


    def controller(self, network, packet):
        try:
            while True:
                data = (network.recv(SIZE)).decode()
                for network in self.networks:
                    if data == "discover":
                        resp = "LIST OF PEERS: {}".format(self.peers)
                        network.send(resp.encode())

                    elif data == "disconnect":
                        self.disconnect(network, packet)

                    elif data.startswith('download'):
                        split_data = data.split()
                        if str(path.exists(split_data[1])) == 'True':
                            print(f"{split_data[1]} is available for download")
                        else:
                            print(f"{split_data[1]} does not exist on the network")
                    else:
                        print(f"{packet}: {data}")
        except Exception as e:
            sys.exit()
            

    def disconnect(self, network, packet):
        self.networks.remove(network)
        self.peers.remove(packet)
        network.close()
        self.send_peers()
        print("{}, disconnected".format(packet))
        print("-" * 50)
