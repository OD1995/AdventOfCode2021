import requests

input_url = "https://adventofcode.com/2021/day/22/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)

input_str = """
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
"""
input_str = """
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
"""
# input_str = input_req.text

def get_to_from(k,part):
    if part == 1:
        f,t = [
            int(x)
            for x in k.split("..")
        ]
        if f > 50:
            return 0,-1
        else:
            _from_ = max(-50,f)
        if t < -50:
            return 0,-1
        else:
            _to_ = min(50,t)
        return _from_,_to_
    else:
        return [
            int(x)
            for x in k.split("..")
        ]


instructions = []
for i in input_str.split("\n"):
    if i != "":
        d = {
            'on' : i.split(" ")[0] == "on"
        }
        for j in i.split(" ")[1].split(","):
            dim,k = j.split("=")
            _from_,_to_ = [
                int(x)
                for x in k.split("..")
            ]
            _from_,_to_ = get_to_from(k,part=1)
            d[dim] = (_from_,_to_)
        instructions.append(d)
print('INSTRUCTIONS')
for i,x in enumerate(instructions):
    print(i,x)
print("\n\n")
# ## Part 1
# def get_coord_list(i):
#     rm = []
#     for x in range(i['x'][0],i['x'][1]+1):
#         for y in range(i['y'][0],i['y'][1]+1):
#             for z in range(i['z'][0],i['z'][1]+1):
#                 rm.append((x,y,z))
#     return rm

# ons = {}

# for I in instructions:
#     # print(I)
#     coord_list = get_coord_list(I)
#     if I['on']:
#         for c in coord_list:
#             ons[c] = 1
#     else:
#         for c in coord_list:
#             ons[c] = 0
#     # print(sum(ons.values()))
# print(sum(ons.values()))

## Part 2
def get_area(i):
    area = 1
    for L in ['x','y','z']:
        area *= (i[L][1] - i[L][0] + 1)
    return area

def check_overlap(cube,I):
    A = {}
    for L in ['x','y','z']:
        cube_from,cube_to = cube[L]
        this_from,this_to = I[L]
        # if ((cube_from <= this_from) and (this_from <= cube_to)):
        #     A[L] = (this_from,min(cube_to,this_to))
        # elif ((cube_from <= this_to) and (this_to <= cube_to)):
        #     A[L] = (max(cube_from,this_from),this_to)
        if (this_from <= cube_to) or (this_to >= cube_from):
            A[L] = (max(this_from,cube_from),min(this_to,cube_to))
        else:
            A[L] = False
    return A

def do_it(instructions,OUTER):
    PRINT = False
    if PRINT:
        print('do_it',instructions)
    if len(instructions) == 1:
        if 'area' in instructions[0]:
            return instructions[0]['area']
    on_cubes = []
    off_cubes = []
    on_overlaps = {}
    for i,I in enumerate(instructions):
        # if I['on']:
        ## Check if any overlap between this and others
        for cube in on_cubes:
            A = check_overlap(cube,I)
            if all(A.values()):
                area1 = get_area(A)
                A['area'] = area1
                A['on'] = True
                # if I['on']:
                if i in on_overlaps:
                    if not I['on']:
                        A['on'] = False
                    on_overlaps[i].append(A)
                else:
                    on_overlaps[i] = [A]
        if I['on']:
            area2 = get_area(I)
            I['area'] = area2
            on_cubes.append(I)
    S = sum([x['area'] for x in on_cubes])
    if PRINT:
        print('S',S,OUTER)
    # print('on_overlaps')
    for k1,v1 in on_overlaps.items():
        V = do_it(v1,False)
        # V = get_unique(v1)
        if PRINT:
            print(k1,v1,V,OUTER)
        #print(V)
        S -= V
        # print('S',S)
    return S
# print('on_overlaps')
# for x,y in on_overlaps.items():
#     print(x,y)
# print('off_overlaps')
# for x,y in off_overlaps.items():
#     print(x,y)
def F(listo):
    off_off_cubes = {0 : listo}
    k = 1
    while True:
        P = []
        for i,x in enumerate(off_off_cubes[k-1]):
            for j,y in enumerate(off_off_cubes[k-1]):
                if j > i:
                    B = check_overlap(x,y)
                    if all(B.values()):
                        area3 = get_area(B)
                        B['area'] = area3
                        P.append(B)
        if len(P) == 0:
            break
        Q = []
        R = {}
        for p in P:
            try:
                ix = Q.index(p)
                if ix not in R:
                    R[ix] = p['area'] * 2
                else:
                    R[ix] += p['area']
            except ValueError:
                Q.append(p)
        for k2,v2 in R.items():
            Q[k2]['area'] = v2
        off_off_cubes[k] = Q
        # print(k,len(Q))
        k += 1
    # print('on_cubes')
    # print(on_cubes)
    # print('off_off_cubes')
    # for k,v in off_off_cubes.items():
    #     print(k)
    #     print(v)
    # on_sum = sum([x['area'] for x in on_cubes])
    total_sum = 0
    # print('on_sum:',on_sum)
    for i,j in off_off_cubes.items():
        this_sum = sum([x['area'] for x in j])
        if i > 0:
            this_sum *= 2
        # print(this_sum)
        if i % 2 == 1:
            total_sum += this_sum
        else:
            total_sum -= this_sum
    # print(total_sum)
    return total_sum

def F(X):
    D = {}
    for d in ['x','y','z']:
        f = min([x[d][0] for x in X])
        t = max([x[d][1] for x in X])
        D[d] = (f,t)
    return -1 * get_area(D)

print(do_it(instructions[:3],True))
