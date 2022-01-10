import requests

input_url = "https://adventofcode.com/2021/day/11/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)


input_str = """
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""

input_str = input_req.text


## Part 1
lights = [
    [
        int(y)
        for y in x
    ]
    for x in input_str.split("\n")
    if x != ""
]

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
        if not ((y0 == 0) and (x0 == 0))
    ]    
    return surrounding_coords

def display_octos(i,octo_dict,y_max,x_max,step_flashers,p=False):
    L = [
        [0] * x_max
        for y in range(y_max)
    ]
    for (x,y),val in octo_dict.items():
        L[y][x] = val
    if p:
        print(f"After step {i}")
        print(f"{len(step_flashers)} flashers")
        for l in L:
            print("".join([str(x) for x in l]))

y_max = len(lights)
x_max = len(lights[0])
octo_dict = {
    (x,y) : lights[y][x]    
    for y in range(y_max)
    for x in range(x_max)
}
flashes = 0
i = 0
display_octos(i,octo_dict,y_max,x_max,[])
for step_no in range(100):
    step_flashers = []
    flashers = []
    ## Add 1 to each octo
    for (x,y),val in octo_dict.items():
        if val == 9:
            flashers.append((x,y))
            step_flashers.append((x,y))
            flashes += 1
            new_val = 0
        else:
            new_val = val + 1
        if (x,y) not in step_flashers:
            octo_dict[(x,y)] = new_val
        else:
            octo_dict[(x,y)] = 0
    old_flash_count = 0
    new_flash_count = 1
    while new_flash_count > old_flash_count:
        old_flash_count = flashes
        add_to_flashers = []
        remove_from_flashers = []
        for fx,fy in flashers:
            surround_coords = get_surrounding_coords(fx,x_max,fy,y_max)
            ## Add 1 to surrounders of each flasher
            for x1,y1 in surround_coords:
                val = octo_dict[(x1,y1)]
                if val == 9:
                    add_to_flashers.append((x1,y1))
                    step_flashers.append((x1,y1))
                    flashes += 1
                    new_val = 0
                else:
                    new_val = val + 1
                if (x1,y1) not in step_flashers:
                    octo_dict[(x1,y1)] = new_val
                else:
                    octo_dict[(x1,y1)] = 0
            remove_from_flashers.append((fx,fy))
        new_flash_count = flashes
        flashers = [
            x
            for x in flashers + add_to_flashers
            if x not in remove_from_flashers
        ]
    display_octos(step_no+1,octo_dict,y_max,x_max,step_flashers)
                
display_octos(step_no+1,octo_dict,y_max,x_max,step_flashers)
print("\n")
print(flashes)
                
                
                
## Part 2
                
def check_if_all_flashing(octo_dict):
    return sum(octo_dict.values()) == 0
octo_dict = {
    (x,y) : lights[y][x]    
    for y in range(y_max)
    for x in range(x_max)
}
flashes = 0
i = 0     
step = 0
while True:
    step += 1
    step_flashers = []
    flashers = []
    ## Add 1 to each octo
    for (x,y),val in octo_dict.items():
        if val == 9:
            flashers.append((x,y))
            step_flashers.append((x,y))
            flashes += 1
            new_val = 0
        else:
            new_val = val + 1
        if (x,y) not in step_flashers:
            octo_dict[(x,y)] = new_val
        else:
            octo_dict[(x,y)] = 0
    old_flash_count = 0
    new_flash_count = 1
    while new_flash_count > old_flash_count:
        old_flash_count = flashes
        add_to_flashers = []
        remove_from_flashers = []
        for fx,fy in flashers:
            surround_coords = get_surrounding_coords(fx,x_max,fy,y_max)
            ## Add 1 to surrounders of each flasher
            for x1,y1 in surround_coords:
                val = octo_dict[(x1,y1)]
                if val == 9:
                    add_to_flashers.append((x1,y1))
                    step_flashers.append((x1,y1))
                    flashes += 1
                    new_val = 0
                else:
                    new_val = val + 1
                if (x1,y1) not in step_flashers:
                    octo_dict[(x1,y1)] = new_val
                else:
                    octo_dict[(x1,y1)] = 0
            remove_from_flashers.append((fx,fy))
        new_flash_count = flashes
        flashers = [
            x
            for x in flashers + add_to_flashers
            if x not in remove_from_flashers
        ]
    if check_if_all_flashing(octo_dict):
        break
print(step)
display_octos(step,octo_dict,y_max,x_max,step_flashers,p=True)