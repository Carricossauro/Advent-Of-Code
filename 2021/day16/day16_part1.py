# Part 1

hexBinTable = {
	"0": "0000",
	"1": "0001",
	"2": "0010",
	"3": "0011",
	"4": "0100",
	"5": "0101",
	"6": "0110",
	"7": "0111",
	"8": "1000",
	"9": "1001",
	"A": "1010",
	"B": "1011",
	"C": "1100",
	"D": "1101",
	"E": "1110",
	"F": "1111"
}

def bin_decimal(binary):
	decimal = 0

	for i, num in enumerate(binary[::-1]):
		decimal += 2**i * int(num)

	return decimal

def hex_binary(hexadecimal):
	binary = []

	for symbol in hexadecimal:
		binary.append(hexBinTable[symbol])

	return "".join(binary)

def literal_value(bits):
	bit_string = ""
	groups = 0
	while bits:
		groups += 5
		bit_string += bits[1:5]
		print(bit_string, bits)
		if bits[0] == '0':
			break
		else:
			bits = bits[5:]

	return bin_decimal(bit_string), groups

# VVVTTTI... -> not literal value
# VVVTTT... -> literal value
def read_packet(packets, bits):
	packet_number = packets["total"]
	packet_version = bin_decimal(bits[:3])
	packet_type = bin_decimal(bits[3:6])
	packet_lengthTypeID = -1 if packet_type == 4 else int(bits[6])
	packet_subPackets = []
	packet_literalValue = -1

	offset = 0
	packets["total"] += 1
	if packet_type == 4: # start at position 6
		packet_literalValue, offset = literal_value(bits[6:])
		offset += 6
		packets[packet_number] = (packet_version, packet_type, packet_lengthTypeID, packet_subPackets, packet_literalValue)
	else: # start at position 7

		if packet_lengthTypeID == 0: # length in bits (15 bits)
			length = bin_decimal(bits[7:7+15])

			i = 1
			while offset < length and not all(map(lambda x: x == 0, bits[7+15+offset:7+15+length])):
				x, child_packet_number = read_packet(packets, bits[7+15+offset:])
				offset += x
				packet_subPackets.append(child_packet_number)
				i += 1

			offset = length + 15
		else: # number of subpackets (11 bits)
			number_of_packets = bin_decimal(bits[7:7+11])

			for i in range(number_of_packets):
				x, child_packet_number = read_packet(packets, bits[7+11+offset:])
				offset += x
				packet_subPackets.append(child_packet_number)

			offset += 11
		offset += 7
		packets[packet_number] = (packet_version, packet_type, packet_lengthTypeID, packet_subPackets, packet_literalValue)
	return offset, packet_number

file = open("day16.txt", 'r')

hexadecimal = file.read()[:-1]

bits = hex_binary(hexadecimal)

# Key    : (0000000, 1111, 222222222222, 3333333333, 444444444444)
# number : (version, type, lengthTypeID, subPackets, literalValue)
packets = {
	"total": 0
}

read_packet(packets, bits)

packet_list = [(k,v) for k,v in packets.items() if k != "total"]
packet_list.sort()

total_versions = 0
for p in packet_list:
	print(p)
	total_versions += p[1][0]

print(total_versions)