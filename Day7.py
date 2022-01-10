import requests

input_url = "https://adventofcode.com/2021/day/7/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)

horizontal_positions = [
    int(x)
    for x in input_req.text.split(",")
    if x != ""
]

# horizontal_positions = [16,1,2,0,4,2,7,1,2,14]

## Part 1

def get_fuel(P,h_p):
    return sum(
        [
            abs(x-P)
            for x in h_p
        ]
    )

pos = int(sum(horizontal_positions) / len(horizontal_positions))

while True:
    pos_fuel = get_fuel(pos,horizontal_positions)
    pos_up_fuel = get_fuel(pos+1,horizontal_positions)
    pos_down_fuel = get_fuel(pos-1,horizontal_positions)
    if min(pos_fuel,pos_up_fuel,pos_down_fuel) == pos_fuel:
        break
    elif pos_down_fuel < pos_fuel:
        pos -= 1
    elif pos_up_fuel < pos_fuel:
        pos += 1
print(pos_fuel)


## Part 2
def calculate_fuel(y):
    return sum(range(1,y+1))

def get_fuel2(P,h_p):
    return sum(
        [
            calculate_fuel(abs(x-P))
            for x in h_p
        ]
    )

while True:
    pos_fuel = get_fuel2(pos,horizontal_positions)
    pos_up_fuel = get_fuel2(pos+1,horizontal_positions)
    pos_down_fuel = get_fuel2(pos-1,horizontal_positions)
    if min(pos_fuel,pos_up_fuel,pos_down_fuel) == pos_fuel:
        break
    elif pos_down_fuel < pos_fuel:
        pos -= 1
    elif pos_up_fuel < pos_fuel:
        pos += 1
print(pos_fuel)