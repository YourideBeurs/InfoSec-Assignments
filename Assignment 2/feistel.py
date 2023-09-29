import struct
import sys

import struct

def feistel_cipher(key, data, decrypt=False):
    # Define the Feistel function
    def feistel_function(right_half, subkey):
        return right_half ^ subkey

    # Split data into 8-byte blocks
    block_size = 8
    num_blocks = len(data) // block_size
    encrypted_data = bytearray()

    for block_index in range(num_blocks):
        block_start = block_index * block_size
        block_end = (block_index + 1) * block_size
        block = data[block_start:block_end]

        # Split block into left and right halves
        left_half, right_half = struct.unpack("<II", block)

        # Perform Feistel network rounds
        num_rounds = len(key) // 4  # Since each round uses 4 bytes of the key
        for round_num in range(num_rounds):
            subkey = struct.unpack("<I", key[round_num*4 : (round_num+1)*4])[0]
            
            if decrypt:
                subkey = struct.unpack("<I", key[-(round_num+1)*4 : -round_num*4])[0]

            new_right_half = left_half ^ feistel_function(right_half, subkey)
            left_half, right_half = right_half, new_right_half

        # Merge left and right halves before storing in the result
        encrypted_data += struct.pack("<II", left_half, right_half)

    return encrypted_data


def main():
    content = sys.stdin.buffer.read()
    mode_byte, _, rest = content.partition(b'\xFF')
    key, _, input_data = rest.partition(b'\xFF')

    mode = 'd' if mode_byte == b'd' else 'e'
    
    if mode == 'd':
        decrypted_data = feistel_cipher(key, input_data, decrypt=True)
        sys.stdout.buffer.write(decrypted_data)
    elif mode == 'e':
        encrypted_data = feistel_cipher(key, input_data)
        sys.stdout.buffer.write(encrypted_data)

if __name__ == "__main__":
    main()
