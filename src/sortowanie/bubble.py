import random
import time


def bubble(data_to_sort) -> list:
    # define flag to monitor if swap has palace or not
    switched_flag = True
    # repeat iteration as soon as swap has pace before
    while switched_flag:
        switched_flag = False
        # as we operate on current and next element, iteration is limited to next to the last element
        for index in range(len(data_to_sort)-1):
            if data_to_sort[index] > data_to_sort[index+1]:
                # perform swap in Python manner
                data_to_sort[index], data_to_sort[index+1] = data_to_sort[index+1], data_to_sort[index]
                switched_flag = True
    return data_to_sort


if __name__ == '__main__':
    # generate list of 10k random integers from -1e6 to 1e6
    list_to_be_sorted = [random.randint(-1000000, 1000000) for _ in range(10000)]
    # measure execution time
    time_start = time.time()
    bubble(list_to_be_sorted)
    print(round(time.time() - time_start, 6), "[s]")
