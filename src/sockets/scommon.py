'''
Created on Feb 21, 2021

@author: anana
'''

HEADER = 60

def socket_message_send(s, data_msg, header = HEADER):
    header_msg = "{1:<{0}}".format(header, len(str(data_msg)))
    s.send(header_msg.encode())
    s.send(str(data_msg).encode())
    
def socket_message_recv(s, header = HEADER):
    data = s.recv(header)
    return (s.recv(int(data.decode()))).decode()