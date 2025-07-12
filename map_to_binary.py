import struct

FILE = "map0.bin"
number_map = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
bits = 4

def write_map_to_binary_file(filename, num_map, bits_per_number):
    if bits_per_number > 32 or bits_per_number < 1:
        raise ValueError("Bits per number must be between 1 and 32.")

    total_bits = len(num_map) * len(num_map[0]) * bits_per_number
    total_bytes = (total_bits + 7) // 8  # round up to full bytes

    bit_stream = ""
    for row in num_map:
        for num in row:
            if num >= (1 << bits_per_number):
                raise ValueError(f"Number {num} too large for {bits_per_number} bits.")
            bit_stream += format(num, f'0{bits_per_number}b')

    # Pad to make full bytes
    bit_stream += '0' * ((8 - len(bit_stream) % 8) % 8)

    byte_array = bytearray()
    for i in range(0, len(bit_stream), 8):
        byte_chunk = bit_stream[i:i+8]
        byte_array.append(int(byte_chunk, 2))

    with open(filename, 'wb') as f:
        f.write(byte_array)

write_map_to_binary_file(FILE, number_map, bits)
