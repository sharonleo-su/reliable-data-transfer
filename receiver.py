from socket import *
from time import sleep
from util import *


class Receiver:
    def __init__(self):
        self.port = 10458
        self.packet_num = 0
        self.ack_num = 1
        self.seq_num = 0
        self.sender_seq_num = None
        self.server_socket = None
        self.connection_socket = None

    def start_server(self):
        """
        Start TCP server. Create the welcome socket and wait for an incoming connection.
        """
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(('', self.port))
        self.server_socket.listen(1)

    def rdt_rcv(self):
        while True:
            data_packet = self.connection_socket.recv(2048)
            # If the socket receives an "end" message then close the connection.
            if data_packet == b'end':
                self.connection_socket.close()
                break
            self.packet_num += 1
            print('\n')
            print('Packet num.{} received: {}'.format(self.packet_num, data_packet))
            data_str = data_packet[12:].decode('utf-8')
            # Get the 11th and 12th bytes of the packet to access the seq num and ack num.
            length_ack_seq = data_packet[10:12]
            length_ack_seq_int = int.from_bytes(length_ack_seq, "big")
            # Find out if the least significant bit (i.e. seq num) is set to 0 or 1.
            if length_ack_seq_int & 1 == 0:
                self.sender_seq_num = 0
            else:
                self.sender_seq_num = 1
            if verify_checksum(data_packet):
                if self.packet_num % 6 == 0 and self.packet_num % 3 == 0:
                    self.simulate_timeout()
                    print('All done for this packet!')
                elif self.packet_num % 6 == 0:
                    self.simulate_timeout()
                    print('All done for this packet!')
                elif self.packet_num % 3 == 0:
                    self.simulate_corruption()
                    # Send duplicate ack, i.e. ack with previous seq num.
                    ack_packet = self.make_ack_packet(self.ack_num, self.seq_num)
                    print('All done for this packet!')
                    self.connection_socket.send(ack_packet)
                else:
                    # Send ack with seq num the same as that of the data packet received.
                    self.seq_num = self.sender_seq_num
                    ack_packet = self.make_ack_packet(self.ack_num, self.seq_num)
                    print('Packet is expected, message string delivered: {}'.format(data_str))
                    print('Packet is delivered, now creating and sending the ACK packet ... ')
                    print('All done for this packet!')
                    self.connection_socket.send(ack_packet)

    @staticmethod
    def make_ack_packet(ack_num, seq_num):
        return make_packet('', ack_num, seq_num)

    @staticmethod
    def simulate_timeout():
        print('Simulating packet loss: sleep a little while to trigger timeout on the send side.')
        sleep(6)

    @staticmethod
    def simulate_corruption():
        print('Simulating bit errors/corruption: ACK the previous packet!')


if __name__ == '__main__':
    receiver = Receiver()
    receiver.start_server()
    receiver.connection_socket, addr = receiver.server_socket.accept()
    receiver.rdt_rcv()
