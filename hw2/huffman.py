'''
Greedy Algorithms: Write an algorithm in the language of your choice to provide
a Huffman encoding from the contents of a .txt file (just the 26 lower case letters
of the alphabet in some arbitrary combination and length) and apply it to
compress the file. Your program should output 2 things, the frequency table for
the characters, and the size of the file (in bytes) before and after the encoding.

Note: You will build the frequency table based on the content of the file.
'''

import sys
import os
import heapq

#Referenced GeeksForGeeks's Huffman Coding in Python (https://www.geeksforgeeks.org/huffman-coding-in-python/)
class Node:
    def __init__(self, char=None, frequency=None):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.frequency < other.frequency


def create_frequency_table(text):
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    return frequency


def create_huffman_tree(frequency):
    priority_queue = []
    
    #Create leaf nodes for each character and add them to priority queue
    for char, freq in frequency.items():
        heapq.heappush(priority_queue, Node(char, freq))
    
    #Build the Huffman tree
    while len(priority_queue) > 1:
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)
        merged = Node(char=None, frequency=left_child.frequency + right_child.frequency)
        merged.left = left_child
        merged.right = right_child
        heapq.heappush(priority_queue, merged)
    
    return priority_queue[0] if priority_queue else None


def create_huffman_codes(node, current_code, codes):
    if node is None:
        return codes
    
    if node.char is not None:
        codes[node.char] = current_code
        return codes
    
    create_huffman_codes(node.left, current_code + "0", codes)
    create_huffman_codes(node.right, current_code + "1", codes)
    return codes


def encode_text(text, codes):
    encoded_text = ""
    for char in text:
        if char in codes: 
            encoded_text += codes[char]
    return encoded_text


#Referenced https://www.w3schools.com/dsa/dsa_ref_huffman_coding.php
def pad_encoded_text(encoded_text):
    padding = 8 - (len(encoded_text) % 8)
    if padding == 8:
        padding = 0
    
    padded_info = "{0:08b}".format(padding)
    padded_text = padded_info + encoded_text + "0" * padding
    return padded_text


def to_bytes_array(padded_text):
    byte_array = bytearray()
    for i in range(0, len(padded_text), 8):
        byte = padded_text[i:i+8]
        byte_array.append(int(byte, 2))
    return byte_array





#--- Main Program ---
if len(sys.argv) < 2:
    print("Usage: python huffman.py <input_file>")
    sys.exit(1)

#Create output file 
input_file = sys.argv[1]
input_basename = os.path.basename(input_file)
input_name = os.path.splitext(input_basename)[0]
output_file = f"{input_name}_compressed.bin"


#Run Huffman encoding and compression
with open(input_file, 'r') as file:
    text = file.read()


frequency = create_frequency_table(text)
huffman_tree = create_huffman_tree(frequency)
huffman_codes = {}
huffman_codes = create_huffman_codes(huffman_tree, "", huffman_codes)

encoded_text = encode_text(text, huffman_codes)
padded_text = pad_encoded_text(encoded_text)
byte_array = to_bytes_array(padded_text)
with open(output_file, 'wb') as f:
    f.write(bytes(byte_array))

#Calculate original and compressed file size
original_size = len(text)
compressed_size = os.path.getsize(output_file)

#Print frequency table and file sizes (in bytes)
print("Character Frequency Table and Huffman Codes:")
for char in sorted(frequency.keys()):
    print(f"'{char}' ({huffman_codes[char]}): {frequency[char]}")

print(f"\nFile size before compression: {original_size} bytes")
print(f"File size after compression: {compressed_size} bytes")