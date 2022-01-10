import requests

input_url = "https://adventofcode.com/2021/day/2/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)

input_list = [
    x.split(" ")
    for x in input_req.text.split("\n")
    if len(x) > 0
]

## Part 1
H = 0
D = 0
for direction,magnitude in input_list:
    if direction == "forward":
        H += int(magnitude)
    elif direction == "down":
        D += int(magnitude)
    elif direction == "up":
        D -= int(magnitude)
print(H*D)

## Part 2
H = 0
D = 0
A = 0
for direction,magnitude in input_list:
    if direction == "forward":
        H += int(magnitude)
        D += A * int(magnitude)
    elif direction == "down":
        A += int(magnitude)
    elif direction == "up":
        A -= int(magnitude)
print(H*D)