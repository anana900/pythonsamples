'''
Created on Feb 21, 2021

@author: anana
'''
import socket as soc
import threading as th
import scommon as hs


class Server():
    
    QUEUE_NO_CONN = 10
    chatrooms = {"Boys":{}, "Girls":{}}
    klienci = dict()

    def __init__(self, port=65432, host=soc.gethostbyname(soc.gethostname())):
        self.server_address = (host, port)
        
        self.server = soc.socket(soc.AF_INET, soc.SOCK_STREAM)
        self.server.bind(self.server_address)
        
        self.server.listen(self.QUEUE_NO_CONN)
        
        print("Server started: {0[0]}:{0[1]}".format(self.server_address))
    
    def chatroom_add_participant(self, client_socket, client_addr, message):
        if "chatroom:" in message:
            chatroom = message[9:]
            if chatroom in self.chatrooms.keys():
                chatroom_clients = self.chatrooms[chatroom]
                chatroom_clients[client_addr] = client_socket
                self.chatrooms.update({chatroom:chatroom_clients})
                print("Client {} added to chatroom {}".format(client_addr, chatroom))
                print("{} chatroom participants: {}".format(chatroom,self.chatrooms[chatroom].keys()))
            else:
                print("No such chatroom {}".format(chatroom))

    def chatroom_broadcast(self, client_soc, client_addr, messg):
        if "chatroom:" in messg:
            return 0

        for rooms, client_socks in self.chatrooms.items():
            if client_addr in client_socks.keys():
                for cls in client_socks.values():
                    if cls != client_soc:
                        hs.socket_message_send(cls, messg)

    def handle_single_client(self, client_socket, client_address):
        while True:
            data_from_client = hs.socket_message_recv(client_socket)
            print(data_from_client)
            
            self.chatroom_add_participant(client_socket, client_address, data_from_client)
            self.chatroom_broadcast(client_socket, client_address, data_from_client)
            
            hs.socket_message_send(client_socket, "OK")
        
            if data_from_client == "koniec":
                print("Rozlaczanie z klientem: {0[0]}:{0[1]}".format(client_address))
                client_socket.close()
                del self.klienci[th.currentThread().ident]
                break        

    def run(self):
        while True:
            client_soc, client_address = self.server.accept()
            t = th.Thread(target=self.handle_single_client, args=(client_soc,client_address))
            t.setDaemon(True)
            t.start()
            
            self.klienci[t.ident] = client_address
            print("Watki, połączenie z klientem: {0} {1[0]}:{1[1]}".format(t.ident, client_address))
            
        self.server.close()


if __name__ == '__main__':
    server = Server()
    server.run()
