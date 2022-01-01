from constants import *
from client import Client
from server import Server


class p2p:
    peers = ['127.0.0.1']

def main():

    sample_msg = "Turning into server.."
    while True:
        try:
            print("Establishing Connection...")
            time.sleep(randint(TIME_START,TIME_END))
            for peer in p2p.peers:
                try:
                    client = Client(peer)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass


                # become the server
                try:
                    server = Server(sample_msg)
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    pass

        except KeyboardInterrupt as e:
            sys.exit(0)

if __name__ == "__main__":
    main()
