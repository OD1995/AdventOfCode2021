import requests

input_url = "https://adventofcode.com/2021/day/20/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)

input_str = """
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""
input_str = input_req.text

iea_str,ii_str = input_str.split("\n\n")

iea = "".join(iea_str.strip().split("\n"))
input_image = [
    list(x)
    for x in ii_str.split("\n")
    if x != ""
]
a=1

def get_output_image(input_image,iea,i):
    if iea[0] == ".":
        replacement_val = "."
    elif i % 2 == 1:
        replacement_val = "."
    else:
        replacement_val = "#"
    ## First, add a row of "."s to the top and bottom
    ##    and a column of "."s to the left and right
    max_x = len(input_image[0]) + 2
    max_y = len(input_image) + 2
    new_ii = [list(replacement_val * max_x)]
    for row in input_image:
        new_ii.append([replacement_val] + row + [replacement_val])
    new_ii.append(list(replacement_val * max_x))

    output_image = [
        [0] * max_x
        for i in range(max_y)
    ]
    lit_pixels = 0
    for y in range(max_y):
        for x in range(max_x):
            val = get_val(new_ii,x,y,iea,max_x,max_y,i)
            if val == "#":
                lit_pixels += 1
            output_image[y][x] = val
    return output_image,lit_pixels

def get_val(new_ii,x,y,iea,max_x,max_y,i):
    coords = [
        (x-1,y-1),
        (x,y-1),
        (x+1,y-1),
        (x-1,y),
        (x,y),
        (x+1,y),
        (x-1,y+1),
        (x,y+1),
        (x+1,y+1)
    ]
    d = {
        "#" : "1",
        "." : "0"
    }
    binary_str = ""
    if iea[0] == ".":
        out_of_bounds_val = "0"
    elif i % 2 == 1:
        out_of_bounds_val = "0"
    else:
        out_of_bounds_val = "1"
    for coord in coords:
        x1,y1 = coord
        if (x1 < 0) or (y1 < 0) or (x1 >= max_x) or (y1 >= max_y):
            binary_str += out_of_bounds_val
        else:
            binary_str += d[new_ii[y1][x1]]
    binary_num = get_binary_num(binary_str)
    return iea[binary_num]


def get_binary_num(binary_str):
    rm = 0
    mag = 1
    for b in reversed(binary_str):
        rm += int(b) * mag
        mag *= 2
    return int(rm)


def display_image(I):
    print("\n\n")
    for i in I:
        print("".join(i))

# ## Part 1
# for i in range(2):
#     input_image,lit_pixels = get_output_image(input_image,iea,i+1)
# print(lit_pixels)

## Part 2
for i in range(50):
    input_image,lit_pixels = get_output_image(input_image,iea,i+1)
    print(i,lit_pixels)