import os


class Packet:
    def __init__(self, bits):
        self.remainder = ''
        self.version = 0
        self.subpackets = []
        self.value = None
        self.length_type = None

        if not bits or not(int(bits)):
            return

        self.version = int(bits[:3], base=2)
        self.type = int(bits[3:6], base=2)

        if self.type == 4:
            self.construct_literal(bits[6:])
        else:
            self.construct_operator(bits[6:])

    def construct_literal(self, bits):
        binary_string = ''
        i = 0
        while bits[i] == '1':
            binary_string += bits[i+1:i+5]
            i += 5
        binary_string += bits[i+1:i+5]
        self.value = int(binary_string, base=2)
        self.remainder = bits[i+5:]

    def construct_operator(self, bits):
        self.length_type = int(bits[0])
        if self.length_type == 0:
            start = 16
            end = start + int(bits[1:start], base=2)
            remainder = bits[start:end]
            while remainder:
                new_packet = Packet(remainder)
                self.subpackets.append(new_packet)
                remainder = new_packet.remainder
            self.remainder = bits[end:]
        else:
            start = 12
            num_subpackets = int(bits[1:start], base=2)
            remainder = bits[start:]
            for _ in range(num_subpackets):
                new_packet = Packet(remainder)
                self.subpackets.append(new_packet)
                remainder = new_packet.remainder
            self.remainder = remainder

    def sum_version_numbers(self):
        return self.version + sum(p.sum_version_numbers() for p in self.subpackets)

    def get_value(self):
        if self.type == 0:
            return sum(p.get_value() for p in self.subpackets)
        if self.type == 1:
            product = 1
            for p in self.subpackets:
                product *= p.get_value()
            return product
        if self.type == 2:
            return min(p.get_value() for p in self.subpackets)
        if self.type == 3:
            return max(p.get_value() for p in self.subpackets)
        if self.type == 4:
            return self.value
        if self.type == 5:
            return int(self.subpackets[0].get_value() > self.subpackets[1].get_value())
        if self.type == 6:
            return int(self.subpackets[0].get_value() < self.subpackets[1].get_value())
        if self.type == 7:
            return int(self.subpackets[0].get_value() == self.subpackets[1].get_value())
        raise ValueError(f'Unexpected Packet Type ID: {self.type}')

    def __repr__(self):
        string = '\n\nPacket:\n'
        for k, v in self.__dict__.items():
            string += f'{k}={v}\n'
        return string + ''


def get_data(path, filename):
    with open(os.path.join(path, filename), 'r') as f:
        return f.read().strip()


def hex_to_bin(hex_data):
    binary_data = ''
    for hex_char in hex_data:
        byte = ''.join([c for c in bin(int(hex_char, base=16))][2:])
        for _ in range(4 - len(byte)):
            byte = '0' + byte
        binary_data += byte
    return binary_data


if __name__ == '__main__':
    hex_data = get_data('data', 'day_16.txt')
    binary_data = hex_to_bin(hex_data)
    packet = Packet(binary_data)
    print(f'Part 1 Solution: {packet.sum_version_numbers()}')
    print(f'Part 2 Solution: {packet.get_value()}')
