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
# off x=0..0,y=0..0,z=0..0
input_str = """
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
off x=0..1,y=0..1,z=0..1
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
input_str = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507
"""
# input_str = """
# on x=-20..-1,y=-11..6,z=-10..1
# on x=-20..5,y=-27..6,z=-14..1
# on x=-5..34,y=-31..6,z=-19..1
# """

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
# print('INSTRUCTIONS')
# for i,x in enumerate(instructions):
#     print(i,x)
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
        area *= max(0,i[L][1] - i[L][0] + 1)
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
        # if (this_from <= cube_to) or (this_to >= cube_from):
        if (
            ((cube_from <= this_from) and (this_from <= cube_to))
            or
             ((cube_from <= this_to) and (this_to <= cube_to))
        ):
            A[L] = (max(this_from,cube_from),min(this_to,cube_to))
        else:
            A[L] = False
    return A

def do_it(instructions,OUTER,PRINT):
    # PRINT = True
    if PRINT:
        print('do_it',instructions)
    if len(instructions) == 1:
        if 'area' in instructions[0]:
            return instructions[0]['area']
    on_cubes = []
    off_cubes = []
    on_overlaps = {}
    off_overlaps = {}
    for i,I in enumerate(instructions):
        # if I['on']:
        ## Check if any overlap between this and others
        for cube in on_cubes:
            A = check_overlap(cube,I)
            if all(A.values()):
                area1 = get_area(A)
                A['area'] = area1
                A['on'] = True
                if I['on']:
                    if i in on_overlaps:
                        # if not I['on']:
                            # A['on'] = False
                        on_overlaps[i].append(A)
                    else:
                        on_overlaps[i] = [A]
                else:
                    if i in off_overlaps:
                        A['on'] = False
                        off_overlaps[i].append(A)
                    else:
                        off_overlaps[i] = [A]
        for cube2 in off_cubes:
            B = check_overlap(cube2,I)
            if all(B.values()):
                area3 = get_area(B)
                B['area'] = area3
                B['on'] = True
                if not I['on']:
                    if i in off_overlaps:
                        B['on'] = False
                        off_overlaps[i].append(B)
                    else:
                        off_overlaps[i] = [B]

        area2 = get_area(I)
        I['area'] = area2
        if I['on']:
            on_cubes.append(I)
        else:
            off_cubes.append(I)
    on_sum = sum([x['area'] for x in on_cubes])
    # off_sum = sum([x['area'] for x in off_cubes])
    S = on_sum #- off_sum
    if PRINT:
        print('S',S,OUTER)
    # print('on_overlaps')
    for k1,v1 in on_overlaps.items():
        V = do_it(v1,False,PRINT)
        # V = get_unique(v1)
        if PRINT:
            print(k1,v1,V,OUTER)
        #print(V)
        S -= V
        # print('S',S)
    # print('off_overlaps')
    for k2,v2 in off_overlaps.items():
        V2 = do_it(v2,False,PRINT)
        # V = get_unique(v1)
        if PRINT:
            print(k2,v2,V2,OUTER)
        #print(V)
        S -= V2
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
# for ii in range(1,5):
#     print(ii,do_it(instructions[:ii],True,False))
print(do_it(instructions,True,False))