import requests

input_url = "https://adventofcode.com/2021/day/15/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)

input_str = """
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""

# input_str = """
# 19999
# 19131
# 11191
# """

input_str = input_req.text

risks = [
    [
        int(y)
        for y in x
    ]
    for x in input_str.split("\n")
    if x.strip() != ""
]
x_len = len(risks[0])
x_lim = x_len - 1
y_len = len(risks)
y_lim = y_len - 1

## Part 1 
total_risks = [
    [0] * (x_len)
    for i in range(y_len)
]

def get_min_surrounding_non0_vals(x,y,x_len,y_len,total_risks,part=1,directions=None):
    if [x,y] in [[0,1],[1,0]]:
        return 0

    if x == 0:
        left = False
    else:
        left = True
    if x == x_len - 1:
        right = False
    else:
        right = True
    if y == 0:
        up = False
    else:
        up = True
    if y == y_len - 1:
        down = False
    else:
        down = True
    L = {}
    if up:
        val = total_risks[y-1][x]
        if val > 0:
            L['up'] = val
    if down:
        val = total_risks[y+1][x]
        if val > 0:
            L['down'] = val
    if left:
        val = total_risks[y][x-1]
        if val > 0:
            L['left'] = val
    if right:
        val = total_risks[y][x+1]
        if val > 0:
            L['right'] = val
    if part == 1:
        return min(L.values())
    elif part == 2:
        return min(L.values())



def do_work1(x_len,y_len,risks,total_risks):
    changes = 0
    for x in range(x_len):
        for y in range(y_len):
            if (x == 0) & (y == 0):
                pass
            else:
                new_val = get_min_surrounding_non0_vals(x,y,x_len,y_len,total_risks) + risks[y][x]
                current_val = total_risks[y][x]
                if (current_val == 0) or (new_val < current_val):
                    changes += 1
                    total_risks[y][x] = new_val
    return total_risks,changes
changes = 1
loops1 = 0
while changes > 0:
    total_risks,changes = do_work1(x_len,y_len,risks,total_risks)
    loops1 += 1
    print(loops1,changes)

print(total_risks[y_len-1][x_len-1])


## Part 2
def deal_with_wrap_around(x):
    while x > 9:
        x -= 9
    return x

x_len2 = x_len * 5
y_len2 = y_len * 5
total_risks2 = [
    [0] * (x_len2)
    for i in range(y_len2)
]
new_risk_val = [
    [0] * x_len2
    for i in range(y_len2)
]


def do_work2(x_len,y_len,x_len2,y_len2,risks,total_risks):
    changes = 0
    for x in range(x_len2):
        for y in range(y_len2):
            if (x == 0) & (y == 0):
                pass
            else:
                yq,yr = divmod(y,y_len)
                xq,xr = divmod(x,x_len)
                base_risk_val = risks[yr][xr]
                incremented_risk_val = base_risk_val + xq + yq
                risk_val = deal_with_wrap_around(incremented_risk_val)
                new_total_val = get_min_surrounding_non0_vals(x,y,x_len2,y_len2,total_risks) + risk_val
                current_total_val = total_risks[y][x]
                if (current_total_val == 0) or (new_total_val < current_total_val):
                    if [x,y] == [2,1]:
                        a=1
                    changes += 1
                    total_risks[y][x] = new_total_val
    return total_risks,changes
changes = 1
loops2 = 0
while changes > 0:
    total_risks2,changes = do_work2(x_len,y_len,x_len2,y_len2,risks,total_risks2)
    loops2 += 1
    print(loops2,changes)

print(total_risks2[y_len2-1][x_len2-1])