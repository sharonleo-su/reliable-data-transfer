def create_checksum(packet_wo_checksum):
    """create the checksum of the packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet_wo_checksum: the packet byte data (including headers except for checksum field)

    Returns:
      the checksum in bytes

    """
    sum_of_integers = 0
    # Read the packet two bytes at a time.
    for i in range(0, len(packet_wo_checksum) - 1, 2):
        # Convert the ASCII codes of the first two characters into 1-byte representations and concatenate them.
        binary_concat = packet_wo_checksum[i].to_bytes(1, "big") + packet_wo_checksum[i + 1].to_bytes(1, "big")
        # Convert the concatenated binary to int
        binary_concat_int = int.from_bytes(binary_concat, "big")
        # Update the sum.
        sum_of_integers += binary_concat_int
        # If number of bits in sum is 17, then truncate it to a 16-bit value and add 1 to the result for wraparound.
        if sum_of_integers.bit_length() > 16:
            truncated_sum = sum_of_integers ^ 65536
            sum_of_integers = truncated_sum + 1
    # Find one's complement of the final sum
    ones_complement = sum_of_integers ^ 65535
    # Convert the one's complement to a byte representation to obtain the checksum.
    checksum = ones_complement.to_bytes(2, "big")
    return checksum


def verify_checksum(packet):
    """verify packet checksum (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet: the whole (including original checksum) packet byte data

    Returns:
      True if the packet checksum is the same as specified in the checksum field
      False otherwise

    """
    new_checksum = create_checksum(packet)
    # If there is no bit error, then the new checksum calculated would be zero, since the
    # checksum field of the packet contains the one's complement.
    if new_checksum == b'\x00\x00':
        return True
    else:
        return False


def make_packet(data_str, ack_num, seq_num):
    """Make a packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      data_str: the string of the data (to be put in the Data area)
      ack_num: an int tells if this packet is an ACK packet (1: ack, 0: non ack)
      seq_num: an int tells the sequence number, i.e., 0 or 1

    Returns:
      a created packet in bytes

    """
    # make sure your packet follows the required format!
    packet = bytearray(b'COMPNETW')
    # Add a dummy checksum field.
    checksum_field = b'\x00\x00'
    packet.extend(checksum_field)
    data_bytes = bytearray(data_str, 'utf-8')
    # Total packet length is header length plus data length. Header length is constant at 12.
    packet_length = len(data_bytes) + 12
    # Form a 2-bit unit consisting of the ack num and seq num.
    ack_seq = str(ack_num) + str(seq_num)
    ack_seq_binary = int(ack_seq, base=2)
    # Add the ack num and seq num to the left-shifted length to form a 16-bit segment.
    length_ack_seq = (packet_length << 2) + ack_seq_binary
    length_ack_seq_bytes = length_ack_seq.to_bytes(2, "big")
    packet.extend(length_ack_seq_bytes)
    packet.extend(data_bytes)
    # if packet length is not divisible by 4, then add padding bits to make it divisible by 4.
    if len(packet) % 4 != 0:
        for n in range(4 - (len(packet) % 4)):
            packet.extend(b'\x00')
    # Calculate the checksum for the packet and insert it in the checksum field.
    checksum = create_checksum(packet)
    packet[8:10] = checksum
    return packet


###### These three functions will be automatically tested while grading. ######
###### Hence, your implementation should NOT make any changes to         ######
###### the above function names and args list.                           ######
###### You can have other helper functions if needed.                    ######

