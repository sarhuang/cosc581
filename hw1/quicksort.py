import sys
import time

#Read numbers from file (separated by newline)
def read_file(filename):
    with open(filename, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]


#Partitions elements less than pivot to left and greater than pivot to right
#Note that it doesn't sort the values
def partition(arr, start_index, end_index, pivot_index):
    pivot_value = arr[pivot_index]

    #Swap pivot and last element (pivot now at end)
    arr[pivot_index], arr[end_index] = arr[end_index], arr[pivot_index] 
    store_index = start_index

    #Iterates through list, except for the pivot now at the end
    for i in range(start_index, end_index):
        #All elements smaller than the pivot are moved to the left side
        if arr[i] < pivot_value:
            arr[i], arr[store_index] = arr[store_index], arr[i]
            store_index += 1
    #Pivot is swapped back to where it should be
    arr[store_index], arr[end_index] = arr[end_index], arr[store_index] 
    return store_index  #the final index of the pivot



#Selects median using partition method for small array (this is how we avoid directly sorting)
def select_median(arr, start_index, end_index):
    middle_index = (end_index - start_index) // 2 + start_index
    
    while True:
        pivot_final_index = partition(arr, start_index, end_index, start_index)
        
        #Pivot is after the median, search to the left of the pivot
        if pivot_final_index > middle_index:
            end_index = pivot_final_index - 1
        #Pivot is before the median, search to the right of the pivot
        elif pivot_final_index < middle_index:
            start_index = pivot_final_index + 1
        else:
            return arr[middle_index]
        
        


# Selects a pivot using the median-of-medians algorithm
def median_of_medians(arr, r):
    if len(arr) <= r:
        return select_median(arr, 0, len(arr)-1)

    #Split into groups of size r
    groups = []
    for i in range(0, len(arr), r):
        group = arr[i:min(i + r, len(arr))]
        if len(group) == r:  
            groups.append(group)

    #Find median of each group
    medians = []
    for group in groups:
        median = select_median(group, 0, len(group)-1)
        medians.append(median)

    #Recursively find the median of medians
    return median_of_medians(medians, r)



#Sorts the array using quicksort with median-of-medians pivot selection
def quicksort(arr, r):
    if len(arr) <= 1:
        return arr
    
    pivot = median_of_medians(arr, r)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left, r) + middle + quicksort(right, r)


def scope():
    if len(sys.argv) != 2:
        print("Usage: ./sort inputfile")
        sys.exit(1)

    input_file = sys.argv[1]
    numbers = read_file(input_file)

    #Different r values for testing
    r_values = [3, 5, 7, 9, 11]  
    times = []

    for r in r_values:
        print("r value: ", r)
        start_time = time.time()
        sorted_numbers = quicksort(numbers, r)
        times.append(time.time() - start_time)
        print(f"{sorted_numbers}\n")
    
    for i in range(len(times)):
        print(f"r value {r_values[i]} duration: {times[i]}")

scope()