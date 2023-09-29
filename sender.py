from socket import *
from util import *

RECEIVER_NAME = 'localhost'
RECEIVER_PORT = 10458


class Sender:
    def __init__(self):
        """ 
        Your constructor should not expect any argument passed in,
        as an object will be initialized as follows:
        sender = Sender()
        
        Please check the main.py for a reference of how your function will be called.
        """
        self.sender_socket = socket(AF_INET, SOCK_STREAM)
        self.sender_socket.connect((RECEIVER_NAME, RECEIVER_PORT))
        self.app_msg_str = ''
        self.packet_num = 0
        self.ack_num = 0
        self.seq_num = 0
        self.receiver_seq_num = 0

    def rdt_send(self, app_msg_str):
        """reliably send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)
        1. Create a data packet and send it to the receiver.
        2. If an ack is received before timeout, then move on to the next packet.
        3. If an ack is not received before timeout, then retransmit the packet.
        4. If a duplicate ack is received, then retransmit the packet.
        Args:
            app_msg_str: the message string (to be put in the data field of the packet)

        """
        self.app_msg_str = app_msg_str
        self.packet_num += 1
        packet = make_packet(app_msg_str, self.ack_num, self.seq_num)
        print('Original message string: {}'.format(self.app_msg_str))
        print('Packet created: {}'.format(packet))
        self.sender_socket.send(packet)
        print('Packet num.{} successfully sent to the receiver.'.format(self.packet_num))
        ack_packet = None
        # Start timer
        self.sender_socket.settimeout(5.0)
        # If ack is not received before timeout, then retransmit the packet.
        try:
            ack_packet = self.sender_socket.recv(2048)
        except timeout:
            print('Socket timeout! Resend!\n')
            print('[Timeout retransmission]')
            self.rdt_send(self.app_msg_str)
        if ack_packet is not None:
            # Get the 11th and 12th bytes of the packet to access the seq num and ack num.
            length_ack_seq = ack_packet[10:12]
            length_ack_seq_int = int.from_bytes(length_ack_seq, "big")
            # Find out if the least significant bit (i.e. seq num) is set to 0 or 1.
            if length_ack_seq_int & 1 == 0:
                self.receiver_seq_num = 0
            else:
                self.receiver_seq_num = 1
            # If the seq num of the ack packet matches the seq num of data packet just sent
            # then toggle the seq num for the next packet.
            if self.receiver_seq_num == self.seq_num:
                print('Packet is received correctly. Sender seq num {} = Receiver seq num {}. All good!'.format(
                    self.seq_num, self.receiver_seq_num))
                self.seq_num ^= 1
            else:
                print('Receiver acked the previous packet, resend!\n')
                print('[ACK-previous retransmission]')
                self.rdt_send(self.app_msg_str)

    ####### Your Sender class in sender.py MUST have the rdt_send(app_msg_str)  #######
    ####### function, which will be called by an application to                 #######
    ####### send a message. DO NOT change the function name.                    #######
    ####### You can have other functions if needed.                             #######
