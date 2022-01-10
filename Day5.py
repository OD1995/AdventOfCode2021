import requests

input_url = "https://adventofcode.com/2021/day/5/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)


input_str = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
input_str = input_req.text

## Part 1
diagram = {}
rows = input_str.split("\n")
for row in rows:
    if row == "":
        continue
    x1,y1,x2,y2 = [
        int(coord)
        for part in row.split(" -> ")
        for coord in part.split(",")
        if coord != ""
    ]
    if x1 == x2:
        for y in range(min(y1,y2),max(y1,y2)+1):
            if (y,x1) not in diagram:
                diagram[(y,x1)] = 1
            else:
                diagram[(y,x1)] += 1
    elif y1 == y2:
        for x in range(min(x1,x2),max(x1,x2)+1):
            if (y1,x) not in diagram:
                diagram[(y1,x)] = 1
            else:
                diagram[(y1,x)] += 1

result = 0
for val in diagram.values():
    if val > 1:
        result += 1
print(result)

## Part 2
diagram2 = {}
rows = input_str.split("\n")
for row in rows:
    if row == "":
        continue
    x1,y1,x2,y2 = [
        int(coord)
        for part in row.split(" -> ")
        for coord in part.split(",")
        if coord != ""
    ]
    min_x = min(x1,x2)
    max_x = max(x1,x2)
    min_y = min(y1,y2)
    max_y = max(y1,y2)
    if x1 == x2:
        for y in range(min_y,max_y+1):
            if (y,x1) not in diagram2:
                diagram2[(y,x1)] = 1
            else:
                diagram2[(y,x1)] += 1
    elif y1 == y2:
        for x in range(min_x,max_x+1):
            if (y1,x) not in diagram2:
                diagram2[(y1,x)] = 1
            else:
                diagram2[(y1,x)] += 1
    else:
        #print(row)
        # /
        if (
            ((x1 > x2) & (y1 < y2))
            or
            ((x1 < x2) & (y1 > y2))
        ):
            #print("/")
            for x in range(min_x,max_x+1):
                y = max_y - x + min_x
                #print(x,"-",y)
                if (y,x) not in diagram2:
                    diagram2[(y,x)] = 1
                else:
                    diagram2[(y,x)] += 1
        # \
        elif (
            ((x1 < x2) & (y1 < y2))
            or
            ((x1 > x2) & (y1 > y2))
        ):
            #print("\\")
            for x in range(min_x,max_x+1):
                y = min_y + x - min_x
                #print(x,"-",y)
                if (y,x) not in diagram2:
                    diagram2[(y,x)] = 1
                else:
                    diagram2[(y,x)] += 1

result2 = 0
for val in diagram2.values():
    if val > 1:
        result2 += 1
print(result2)