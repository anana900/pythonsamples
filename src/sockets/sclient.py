'''
Created on Feb 21, 2021

@author: ananacd
'''
import socket as soc
import scommon as hs
import sys
import select


class Client:
    def __init__(self, server_port=65432, server_host=soc.gethostbyname(soc.gethostname())):
        self.address = (server_host, server_port)
        
        self.client = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        self.client.connect(self.address)
        
        print("Client is connecting to {0[0]}:{0[1]}".format(self.address))

    def run(self, data):
        while True:
            read_socket_list = [sys.stdin, self.client]
            read_s, write_s, ex_s = select.select(read_socket_list, [], [])

            for rs in read_s:
                if rs == self.client:
                    data_from_server = hs.socket_message_recv(self.client)
                    print("{}".format(data_from_server))
                else:
                    data = input(">: ")
                    hs.socket_message_send(self.client, data)

                    if data == "koniec":
                        self.client.close()
                        break


if __name__ == '__main__':
    client = Client(int(sys.argv[1]))
    client.run("Czesc, co slychac?")
