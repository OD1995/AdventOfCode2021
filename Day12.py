import requests

input_url = "https://adventofcode.com/2021/day/12/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)


input_str = """
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

input_str = """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""

input_str = """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""

input_str = input_req.text

routes = [
    x.split("-")
    for x in input_str.split("\n")
    if x != ""
]

unique_caves = set(
    [
        y
        for x in routes
        for y in x
    ]
)

connections = {}

for cave in unique_caves:
    connected = []
    for route in routes:
        if cave in route:
            connected.append(
                route[0] if route[1] == cave else route[1]
            )
    connections[cave] = connected


## Part 1
def double_small_cave(route):
    character_count = {}
    for r in route:
        if r in character_count:
            character_count[r] += 1
        else:
            character_count[r] = 1
    for k,v in character_count.items():
        if k.islower() & (v > 1):
            return True
    return False

def F(connections,unfinished_routes,complete_routes):
    add_to_unfinished_routes = []
    remove_from_unfinished_routes = []
    for unfinished_route in unfinished_routes:
        unfinished_route_list = list(unfinished_route)
        last_cave = unfinished_route[-1]
        for R3 in connections[last_cave]:
            new_route = tuple(unfinished_route_list + [R3])
            if double_small_cave(new_route):
                pass
            elif R3 == 'end':
                complete_routes.append(new_route)
            else:
                add_to_unfinished_routes.append(new_route)
        remove_from_unfinished_routes.append(unfinished_route)
    unfinished_routes = [
        x
        for x in unfinished_routes + add_to_unfinished_routes
        if x not in remove_from_unfinished_routes
    ]
    return unfinished_routes,complete_routes


complete_routes = []
unfinished_routes = []

for R in connections['start']:
    new_route = ('start',R)
    if R == 'end':
        complete_routes.append(new_route)
    else:
        unfinished_routes.append(new_route)

# while len(unfinished_routes) != 0:
#     unfinished_routes,complete_routes = F(connections,unfinished_routes,complete_routes)

# print(len(complete_routes))

## Part 2
def double_small_cave2(route):
    character_count = {}
    SE = ['start','end']
    for r in route:
        if r in character_count:
            character_count[r] += 1
        else:
            character_count[r] = 1
    small_cave_entry_count = 0
    for k,v in character_count.items():
        if (k in SE) & (v > 1):
            return True
        elif k.islower() & (k not in SE):
            if v == 2:
                small_cave_entry_count += 1
            elif v > 2:
                return True
    if small_cave_entry_count > 1:
        return True
    else:
        return False

def F2(connections,unfinished_routes,complete_routes):
    add_to_unfinished_routes = []
    remove_from_unfinished_routes = []
    for unfinished_route in unfinished_routes:
        unfinished_route_list = list(unfinished_route)
        last_cave = unfinished_route[-1]
        for R3 in connections[last_cave]:
            new_route = tuple(unfinished_route_list + [R3])
            if double_small_cave2(new_route):
                pass
            elif R3 == 'end':
                complete_routes.append(new_route)
            else:
                add_to_unfinished_routes.append(new_route)
        remove_from_unfinished_routes.append(unfinished_route)
    unfinished_routes = [
        x
        for x in unfinished_routes + add_to_unfinished_routes
        if x not in remove_from_unfinished_routes
    ]
    return unfinished_routes,complete_routes


complete_routes = []
unfinished_routes = []

for R in connections['start']:
    new_route = ('start',R)
    if R == 'end':
        complete_routes.append(new_route)
    else:
        unfinished_routes.append(new_route)

while len(unfinished_routes) != 0:
    unfinished_routes,complete_routes = F2(connections,unfinished_routes,complete_routes)

print(len(complete_routes))


# 1 65 67
# 2 570 572
# 3 2963 2965
# 4 12185 12187
# 5 34348 34350
# 6 80818 80820
# 7 147280 147282

# 1 36 67
# 2 316 572
# 3 1773 2965
# 4 7700 12187
# 5 24963 34350
# 6 63434 80820
# 7 104717 147282
# 8 175713 231813