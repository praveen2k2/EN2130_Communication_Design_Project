# Define the byte sequence to detect
detect_sequence = b'11010000'

# Calculate the number of bits
number_of_bits = len(detect_sequence) * 8

print(f"The number of bits in the detect sequence is: {number_of_bits}")