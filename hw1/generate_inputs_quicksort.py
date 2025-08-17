import random

#Generates a file with x numbers separated by new lines
def generate_input_file(filename, num_count, min_value, max_value):
    with open(filename, 'w') as f:
        for i in range(num_count-1):
            f.write(f"{random.randint(min_value, max_value)}\n")
        f.write(f"{random.randint(min_value, max_value)}")


generate_input_file(f"input_{10}.txt", num_count=10, min_value=1, max_value=100)
generate_input_file(f"input_{100}.txt", num_count=100, min_value=1, max_value=1000)
generate_input_file(f"input_{1000}.txt", num_count=1000, min_value=1, max_value=10000)
generate_input_file(f"input_{10000}.txt", num_count=10000, min_value=1, max_value=100000)
generate_input_file(f"input_{100000}.txt", num_count=100000, min_value=1, max_value=1000000)
generate_input_file(f"input_{1000000}.txt", num_count=1000000, min_value=1, max_value=10000000)