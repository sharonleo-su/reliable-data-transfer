from sender import Sender


# note: no arguments will be passed in
sender = Sender()


for i in range(1, 10):
    # this is where your rdt_send will be called
    print('\n')
    sender.rdt_send('msg' + str(i))

# Send a bytestring "end" to indicate to the receiver that all packets have been transmitted
# so that the receiver can close its connection socket.
sender.sender_socket.send(b'end')
