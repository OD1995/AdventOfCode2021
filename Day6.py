import requests

input_url = "https://adventofcode.com/2021/day/6/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)

fish_ages = [
    int(x)
    for x in input_req.text.split(",")
]

# fish_ages = [3,4,3,1,2]

# ## Part 1
ages_dict = {
    a : 0
    for a in range(9)
}
for fa in fish_ages:
    ages_dict[fa] += 1
days = 80
for day in range(1,days+1):
    new_fish = ages_dict[0]
    for a in range(1,9):
        ages_dict[a-1] = ages_dict[a]
    ages_dict[8] = new_fish
    ages_dict[6] += new_fish
    a = 1

print(sum(ages_dict.values()))

# ## Part 2
ages_dict = {
    a : 0
    for a in range(9)
}
for fa in fish_ages:
    ages_dict[fa] += 1
days = 256
for day in range(1,days+1):
    new_fish = ages_dict[0]
    for a in range(1,9):
        ages_dict[a-1] = ages_dict[a]
    ages_dict[8] = new_fish
    ages_dict[6] += new_fish
    a = 1

print(sum(ages_dict.values()))
