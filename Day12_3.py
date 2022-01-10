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




def checker1():
    pass

def checker2():
    pass

def fill_M_with_routes(M,cave_list,both_routes,ia_dict,SE,checker):
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
    for C1 in cave_list:
        for C2 in cave_list:
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
                            IA = checker(new_route,ia_dict,SE)
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


def get_routes_to_cave(cave,input_str,checker):
    SE = ['start','end']
    routes = [
        [
            y.strip()
            for y in x.split("-")
        ]
        for x in input_str.split("\n")
        if x.strip() != ""
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

    single_linked_caves = []
    multi_linked_caves = []
    for k,v in connections.items():
        if k not in SE:
            if len(v) == 1:
                single_linked_caves.append(k)
            elif len(v) > 1:
                multi_linked_caves.append(k)

    both_routes = []
    for r in routes:
        both_routes.append(sorted(r,reverse=True))
        both_routes.append(sorted(r))
        
    M = {
        'start' : [['start']]
    }
    for c in connections['start']:
        M[c] = [['start',c]]
        # both_routes.remove(sorted(['start',c]))
    i = 0
    new = 1
    old = 0
    ia_dict = {}
    L = ['start'] + multi_linked_caves
    while new > old:
        old = new
        i += 1
        j = 1 if i % 2 == 0 else 0
        # L = UC[j]
        (
            M,new,iac,skip,skip2,ia_dict
        ) = fill_M_with_routes(M,L,both_routes,ia_dict,SE,checker)
        print(i,iac,skip,skip2,new)
    a = 1
    return len(M[cave])