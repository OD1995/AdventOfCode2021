import requests

input_url = "https://adventofcode.com/2021/day/9/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)


input_str = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""

input_str = input_req.text

heights = [
    [
        int(y)
        for y in list(x)
    ]
    for x in input_str.split("\n")
    if x != ""
]

def get_surrounding_vals(
    x,
    x_max,
    y,
    y_max,
    heights
):
    surrounding_coords = get_surrounding_coords(
        x,
        x_max,
        y,
        y_max
    )
    surrounding_vals = [
        heights[y][x]
        for (x,y) in surrounding_coords
    ]
    return surrounding_vals

def get_surrounding_coords(
    x,
    x_max,
    y,
    y_max
):
    diffs = {}
    for var,var_str,var_max in [
        [x,'x',x_max],
        [y,'y',y_max]
    ]:
        if var == 0:
            diffs[var_str] = [0,1]
        elif var == var_max - 1:
            diffs[var_str] = [-1,0]
        else:
            diffs[var_str] = [-1,0,1]
    surrounding_coords = [
        (x+x0,y+y0)
        for y0 in diffs['y']
        for x0 in diffs['x']
        if (y0 != x0) and ((y0 == 0) or (x0 == 0))
    ]    
    return surrounding_coords

## Part 1
x_max = len(heights[0])
y_max = len(heights)
low_points = {}
for y in range(y_max):
    for x in range(x_max):
        current_val = heights[y][x]
        surrounding_vals = get_surrounding_vals(
            x,
            x_max,
            y,
            y_max,
            heights
        )
        if current_val < min(surrounding_vals):
            low_points[(x,y)] = current_val
print(
    sum(
        [x+1 for x in low_points.values()]
    )
)

## Part 2
input_str = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""




def get_basin(
    get_sc_list,
    sc_list_done,
    basin_coords,
    heights
):
    for X,Y in get_sc_list:
        surrounding_coords = get_surrounding_coords(
            X,
            x_max,
            Y,
            y_max
        )
        get_sc_list.remove((X,Y))
        sc_list_done.append((X,Y))
        for x,y in surrounding_coords:
            val = heights[y][x]
            # print(f"({x},{y})","--->",val)
            if val != 9:
                if (x,y) not in sc_list_done:
                    get_sc_list.append((x,y))
                if (x,y) not in basin_coords:
                    basin_coords.append((x,y))
    return get_sc_list, sc_list_done, basin_coords
all_basins = {}
for (lpx,lpy),lp in low_points.items():
    i = 0
    # if lpx != 9:
    #     continue
    get_sc_list = [(lpx,lpy)]
    sc_list_done = []
    basin_coords = [(lpx,lpy)]
    while len(get_sc_list) > 0:
        # print(i)
        (
            get_sc_list,
            sc_list_done,
            basin_coords
        ) = get_basin(
            get_sc_list,
            sc_list_done,
            basin_coords,
            heights
        )
        # print("get_sc_list:",get_sc_list)
        # print("sc_list_done:",sc_list_done)
        # print("basin_coords:",basin_coords)
        i += 1
    all_basins[(lpx,lpy)] = basin_coords
        
basin_sizes = [len(S) for S in all_basins.values()]
basin_sizes.sort(reverse=True)
print(basin_sizes[0] * basin_sizes[1] * basin_sizes[2])