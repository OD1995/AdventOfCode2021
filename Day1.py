import requests

input_url = "https://adventofcode.com/2021/day/1/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)

input_list = [
    int(x)
    for x in input_req.text.split("\n")
    if len(x) > 0
]

## Part 1
count = 0
for i in range(len(input_list)-1):
    this_one = input_list[i]
    next_one = input_list[i+1]
    if next_one > this_one:
        count += 1
print(count)

## Part 2
count2 = 0
letter_dict = {}
i = 2
# for i in range(2,27):
while True:
    # this_letter = chr(ord('@')+i-1)
    # next_list = chr(ord('@')+i)
    this_list = input_list[i-2:i+1]
    next_list = input_list[i-1:i+2]
    if len(next_list) < 3:
        break
    # letter_dict[this_letter] = sum(this_list)
    # letter_dict[next_letter] = sum(next_list)
    if sum(next_list) > sum(this_list):
        count2 += 1
    i += 1
print(count2)