import requests

input_url = "https://adventofcode.com/2021/day/3/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)

input_list = [
    x
    for x in input_req.text.split("\n")
    if len(x) > 0
]

def get_num_from_binary(S):
    rm = 0
    mag = 1
    for val in reversed(S):
        rm += mag * int(val)
        mag *= 2
    return rm

## Part 1
gamma_string = ""
epsilon_string = ""
for i in range(12):
    binary_dict = {
        "0" : 0,
        "1" : 1
    }
    for y in input_list:
        binary_dict[y[i]] += 1
    if binary_dict["0"] > binary_dict["1"]:
        gamma_string += "0"
        epsilon_string += "1"
    else:
        gamma_string += "1"
        epsilon_string += "0"
print(get_num_from_binary(gamma_string)*get_num_from_binary(epsilon_string))


## Part 2
def get_val(input_list,i,oxy):
    binary_dict = {
        "0" : 0,
        "1" : 0
    }
    for y in input_list:
        binary_dict[y[i]] += 1
    if binary_dict["0"] > binary_dict["1"]:
        return "0" if oxy else "1"
    elif binary_dict["0"] < binary_dict["1"]:
        return "1" if oxy else "0"
    else:
        return "1" if oxy else "0"
input_list_oxy = input_list
input_list_co2 = input_list
oxy_not_done = True
co2_not_done = True
for i in range(12):
    if oxy_not_done:
        val_oxy = get_val(input_list_oxy,i,oxy=True)
        input_list_oxy = [
            x
            for x in input_list_oxy
            if x[i] == val_oxy
        ]
        if len(input_list_oxy) == 1:
            oxy_not_done = False
            oxy_val = input_list_oxy[0]
    if co2_not_done:
        val_co2 = get_val(input_list_co2,i,oxy=False)
        input_list_co2 = [
            x
            for x in input_list_co2
            if x[i] == val_co2
        ]
        if len(input_list_co2) == 1:
            co2_not_done = False
            co2_val = input_list_co2[0]
print(get_num_from_binary(oxy_val)*get_num_from_binary(co2_val))






