import requests

input_url = "https://adventofcode.com/2021/day/12/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)

INPUT = input("number: ")

if INPUT == "1":
    input_str = """
    start-A
    start-b
    A-c
    A-b
    b-d
    A-end
    b-end
    """
elif INPUT == "2":
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
elif INPUT == "3":
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
elif INPUT == "4":
    input_str = input_req.text

routes = [
    [
        y.strip()
        for y in x.split("-")
    ]
    for x in input_str.split("\n")
    if x.strip() != ""
]

SE = ['start','end']
unique_caves = ['start']
for x in routes:
    for y in x:
        if (y not in unique_caves) & (y not in SE):
            unique_caves.append(y)
unique_caves.append("end")

connections = {}

for cave in unique_caves:
    connected = []
    for route in routes:
        if cave in route:
            connected.append(
                route[0] if route[1] == cave else route[1]
            )
    connections[cave] = connected

# ## Part 1
# def is_allowed(route):
#     character_count = {}
#     for r in route:
#         if r in character_count:
#             character_count[r] += 1
#         else:
#             character_count[r] = 1
#     for k,v in character_count.items():
#         if k.islower() & (v > 1):
#             return False
#     return True


# def fill_remaining_caves(M,connections,unique_caves,both_routes):
#     new_routes_added = 1
#     total_routes = sum(
#         [
#             len(x)
#             for x in M.values()
#         ]
#     )
#     while new_routes_added > 0:
#         new_routes_added = 0
#         for C1 in unique_caves:
#             for C2 in unique_caves:
#                 if (C1 == "b") & (C2 == "A"):
#                     b = 3
#                 if ([C1,C2] in both_routes) & (C2 != 'start'):
#                     if C1 in M:
#                         for route in M[C1]:
#                             new_route = route + [C2]
#                             if is_allowed(new_route):
#                                 if C2 in M:
#                                     if new_route not in M[C2]:
#                                         M[C2].append(new_route)
#                                         new_routes_added += 1
#                                 else:
#                                     M[C2] = [new_route]
#                                     new_routes_added += 1
#         total_routes = sum(
#             [
#                 len(x)
#                 for x in M.values()
#             ]
#         )
#         a = 1
#     return M,total_routes






# def get_routes_to_cave(cave,connections,unique_caves,routes):
#     M = {
#         'start' : [['start']]
#     }
#     both_routes = []
#     for r in routes:
#         both_routes.append(sorted(r,reverse=True))
#         both_routes.append(sorted(r))
#     for c in connections['start']:
#         routes_to_c = [
#             ['start',c]
#         ]
#         M[c] = routes_to_c
#         both_routes.remove(sorted(['start',c]))

#     M,new_route_count = fill_remaining_caves(M,connections,unique_caves,both_routes)

#     return len(M[cave])
        
# a = get_routes_to_cave("end",connections,unique_caves,routes)
# print(a)


## Part 2
# def is_allowed2(route):
#     SE = ['start','end']
#     for se in SE:
#         if route.count(se) > 1:
#             return False
#     character_count = {}
#     small_cave_count = 0
#     for r in route:
#         if r.islower() & (r not in SE):
#             if r in character_count:
#                 character_count[r] += 1
#                 if character_count[r] == 2:
#                     small_cave_count += 1
#                 elif character_count[r] > 2:
#                     return False
#             else:
#                 character_count[r] = 1
#     if small_cave_count > 1:
#         return False
#     return True


# def is_allowed2(route):
#     SE = ['start','end']
#     for se in SE:
#         if route.count(se) > 1:
#             return False
#     character_count = {}
#     small_cave_count = 0
#     for r in route:
#         if r.islower() & (r not in SE):
#             if r in character_count:
#                 character_count[r] += 1
#                 if character_count[r] == 2:
#                     small_cave_count += 1
#                 elif character_count[r] > 2:
#                     return False
#             else:
#                 character_count[r] = 1
#     if small_cave_count > 1:
#         return False
#     ## Return what would cause it to break
#     breakers = []
#     already_small_double_used = small_cave_count == 1
#     for char,cnt in character_count.items():
#         if already_small_double_used:
#             if cnt > 0:
#                 breakers.append(char)
#     return breakers


def is_allowed2(route,ia_dict,SE):
    # if route in [
    #     ['start','A','c','A'],
    #     ['start', 'A', 'b', 'd', 'b']
    # ]:
    #     A = 1
    new_cave = route[-1]
    if tuple(route[:-1]) in ia_dict:
        D = ia_dict[tuple(route[:-1])].copy()
        if (
                (new_cave in D['BREAKERS'])
                or
                (
                    (new_cave.islower())
                    and
                    (new_cave in D)
                    and
                    (D['SMALL_CAVE_DOUBLE_COUNT'] > 0)
                )
        ):
            D['ALLOWED'] = False
            return D
        if (new_cave not in SE) & new_cave.islower():
            if (new_cave in D):
                D[new_cave] += 1
                D['SMALL_CAVE_DOUBLE_COUNT'] += 1
            else:
                D[new_cave] = 1
            if D['SMALL_CAVE_DOUBLE_COUNT'] == 1:
                # D['BREAKERS'].append(new_cave)
                # old_breakers = D['BREAKERS']
                D['BREAKERS'] = [
                    ch
                    for ch in D.keys()
                    if ch.islower()
                ]

            elif D['SMALL_CAVE_DOUBLE_COUNT'] > 1:
                D['ALLOWED'] = False
                return D
        
    else:
        D = {
            'ALLOWED' : True
        }
        small_cave_double_count = 0
        for r in route:
            if r.islower() & (r not in SE):
                if r in D:
                    D[r] += 1
                    if D[r] == 2:
                        small_cave_double_count += 1
                    else:
                        D['ALLOWED'] = False
                        return D
                else:
                    D[r] = 1
        D['SMALL_CAVE_DOUBLE_COUNT'] = small_cave_double_count
        D['BREAKERS'] = []
        # breakers = []
        already_small_double_used = small_cave_double_count == 1
        for char,cnt in D.items():
            if char.islower() & already_small_double_used:
                if cnt > 0:
                    # breakers.append(char)
                    D['BREAKERS'].append(char)
        # D['BREAKERS'] = breakers
        
    return D

def DC(ia_dict):
    T = ('start','A','c','A')
    if T in ia_dict:
        if ia_dict[T]['BREAKERS'] != []:
            return True
    return False

def fill_remaining_caves2(M,unique_caves,both_routes,ia_dict,SE):
    new_routes_added = 1
    iac = 0
    skip = 0
    skip2 = 0
    total_routes = sum(
        [
            len(x)
            for x in M.values()
        ]
    )
    for C1 in unique_caves:
        for C2 in unique_caves:
            # if ("end" in [C1,C2]):
            #     b = 3
            if (
                    ([C1,C2] in both_routes)
                    &
                    (C1 != 'end')
                    &
                    (C2 != 'start')
            ):
                new_combo_routes_added = 0
                if C1 in M:
                    for route in M[C1]:
                        new_route = route + [C2]
                        # if new_route == ['start', 'A', 'c','A','b']:
                        #     a = 1
                        if tuple(new_route) in ia_dict:
                            skip2 += 1
                            continue
                        if tuple(route) in ia_dict:
                            # if DC(ia_dict):
                            #     a = 1
                            IA_old = ia_dict[tuple(route)].copy()
                            if (IA_old['ALLOWED'] == False) or (C2 in IA_old['BREAKERS']):
                                go_ahead = False
                                IA_old['ALLOWED'] = False
                                ia_dict[tuple(new_route)] = IA_old
                                ga1 = False
                                skip += 1
                            else:
                                ga1 = True
                        else:
                            ga1 = True
                        if ga1:
                            # if DC(ia_dict):
                            #     a = 1
                            IA = is_allowed2(new_route,ia_dict,SE)
                            iac += 1
                            ia_dict[tuple(new_route)] = IA
                            # if DC(ia_dict):
                            #     a = 1
                            go_ahead = IA['ALLOWED']
                        if go_ahead:
                            if C2 in M:
                                if new_route not in M[C2]:
                                    M[C2].append(new_route)
                                    new_routes_added += 1
                                    new_combo_routes_added += 1
                            else:
                                M[C2] = [new_route]
                                new_routes_added += 1
                                new_combo_routes_added += 1
                        
    total_routes = sum(
        [
            len(x)
            for x in M.values()
        ]
    )
    if 'end' in M:
        end_count = len(M['end'])
    else:
        end_count = 0
    a = 1
    return M,total_routes,iac,skip,skip2,ia_dict


def get_routes_to_cave2(cave,connections,unique_caves,routes):
    M = {
        'start' : [['start']]
    }
    both_routes = []
    for r in routes:
        both_routes.append(sorted(r,reverse=True))
        both_routes.append(sorted(r))
    for c in connections['start']:
        routes_to_c = [
            ['start',c]
        ]
        M[c] = routes_to_c
        both_routes.remove(sorted(['start',c]))
    unique_caves_rev = list(reversed(unique_caves))
    # M,ct1 = fill_remaining_caves2(M,connections,unique_caves,both_routes)
    # M,ct2 = fill_remaining_caves2(M,connections,unique_caves_rev,both_routes)
    i = 0
    UC = [
        unique_caves,
        unique_caves_rev
    ]
    SE = ['start','end']
    new = 1
    old = 0
    ia_dict = {}
    while new > old:
        old = new
        i += 1
        j = 1 if i % 2 == 0 else 0
        L = UC[j]
        (
            M,new,iac,skip,skip2,ia_dict
        ) = fill_remaining_caves2(M,L,both_routes,ia_dict,SE)
        print(i,iac,skip,skip2,new)
    a = 1
    return len(M[cave])
        
a = get_routes_to_cave2("end",connections,unique_caves,routes)
print(a)
b=1






# 1 65 0 0 67
# 2 505 61 65 572
# 3 2393 719 631 2965
# 4 9222 4198 3743 12187
# 5 22163 14578 17163 34350
# 6 46470 40668 53904 80820
# 7 66462 70538 141042 147282
# 8 84531 126565 278042 231813
# 9 73781 121848 489138 305594
# 10 57610 130064 684767 363204
# 11 29798 76692 872441 393002
# 12 12056 43892 978931 405058
# 13 3358 14322 1034879 408416
# 14 98 3378 1052559 408514
# 15 0 0 1056035 408514
