from sys import argv

input_file1 = argv[1]
input_file2 = argv[2]


def get_int_list(f_name):
    with open(f_name, mode='r') as input_data:
        lines = input_data.readlines()
        elements = lines[0].split(" ")
        elements = list(filter(lambda t: t != '', elements))
        return sorted(list(map(int, elements)))


list1 = get_int_list(input_file1)
list2 = get_int_list(input_file2)
print(list1)
print(list2)
print(list1 == list2)
