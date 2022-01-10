import requests

input_url = "https://adventofcode.com/2021/day/13/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)


input_str = """
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""

input_str = input_req.text

coords = []
dots_dict = {}
max_x = 0
max_y = 0
for s in input_str.split("\n\n")[0].split("\n"):
    if s.strip() != "":
        x,y = [
            int(a)
            for a in s.split(",")
        ]
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
        coords.append((x,y))
        dots_dict[(x,y)] = 1



folds = [
    [
        int(y) if i == 1 else y
        for i,y in enumerate(x.replace("fold along ","").split("="))
    ]
    for x in input_str.split("\n\n")[1].split("\n")
    if x.strip() != ""
]


# fold_axis,fold_val = folds[0]
for fold_axis,fold_val in folds:
    axis_ix = 1 if fold_axis == "y" else 0

    for C in list(dots_dict):
        if dots_dict[C] > 0:
            dist_from_fold_line = C[axis_ix] - fold_val
            if dist_from_fold_line > 0:
                if axis_ix == 1:
                    new_coords = (C[0],fold_val-dist_from_fold_line)
                else:
                    new_coords = (fold_val-dist_from_fold_line,C[1])
                if new_coords in dots_dict:
                    dots_dict[new_coords] += 1
                else:
                    dots_dict[new_coords] = 1
                dots_dict[C] = 0
    b = 1

# print(len({x:y for x,y in dots_dict.items() if y > 0}))

dotted_dict = {x:y for x,y in dots_dict.items() if y > 0}
ndt = {}
max_x = 0
max_y = 0
for (x,y),val in dots_dict.items():
    if val > 0:
        ndt[(x,y)] = 1
        max_x = max(x,max_x)
        max_y = max(y,max_y)

L = [
    ["."]*(max_x+1)
    for i in range(max_y+1)
]

for (x,y) in ndt.keys():
    L[y][x] = "#"

def display_L(L,from_X,to_X,from_Y,to_Y):
    for i in range(from_Y,to_Y+1):
        print("".join(L[i][from_X:to_X+1]))

min_xy = 1000000
for (x,y) in ndt.keys():
    if (x+y) < min_xy:
        min_xy = x+y
        xx,yy = x,y

a = 1