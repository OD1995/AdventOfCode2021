from numpy import r_
from pyrsistent import b


def move(moves,bedrooms,hallway,starting_b_ix,i):
    if i == 0:
        from_details,to_details = move_out_the_way(bedrooms,hallway,starting_b_ix)
    else:
        ## Check if it's possible to move any amphipod
        ##    from the hallway into their final destination
        result = fill_bedroom_from_hallway(hallway,bedrooms)
        if result:
            from_details,to_details = result
        else:
            ## Check if it's possible to move any amphipod
            ##    from their bedroom into their final destination
            result1 = fill_bedroom_from_bedrooms(hallway,bedrooms)
            if result1:
                from_details,to_details = result1
            else:
                pass
    ## Do the move
    assert not from_details['type'] == to_details['type'] == 'h'

def fill_bedroom_from_hallway(hallway,bedrooms):
    hallway_ixs = []
    hallway_vals = []
    for ix,a in enumerate(hallway):
        if a != '.':
            hallway_ixs.append(ix)
            hallway_vals.append(a)
    ## Loop through all the hallway amphipods
    for hi,hv in zip(hallway_ixs,hallway_vals):
        F = {
            'type' : 'h',
            'h_ix' : hi
        }
        r_ix = get_bedroom(get_other_type(hv),bedrooms,'empty','bottom')
        if r_ix:
            T = {
                'type' : 'b',
                'b_ix' : get_other_type(hv),
                'r_ix' : r_ix
            }
            do_it = False
            if r_ix == 1:
                do_it = True
            else:
                if check_if_in_right_spot(bedrooms,get_other_type(hv),1):
                    do_it = True
            if do_it:
                route,r = get_route(F,T,bedrooms,hallway)
                route_is_valid = validate_route(route,r)
                if route_is_valid:
                    return F,T

def fill_bedroom_from_bedrooms(hallway,bedrooms):
    ## Get top empty bedrooms
    empty_bedrooms = {}
    for i in range(4):
        result1 = get_bedroom(i,bedrooms,'empty','top')
        if result1:
            empty_bedrooms[i] = result1
    ## Get top full bedrooms
    full_bedrooms = {}
    for i in range(4):
        result2 = get_bedroom(i,bedrooms,'full','top')
        if result2:
            full_bedrooms[i] = result2
    ## Loop through top full bedrooms and see if they can fill the empty ones
    for full_bix,full_rix in full_bedrooms.items():
        ## Get letter of amphibod
        amphipod_letter = bedrooms[full_bix][full_rix]
        desired_bix = get_other_type(amphipod_letter)
        ## Check if that bedroom has an empty bedroom
        if desired_bix in empty_bedrooms:
            empty_rix = empty_bedrooms[desired_bix]
            do_it = False
            if empty_rix == 1:
                do_it = True
            ## If r_ix == 0, make sure the amphipod at r_ix == 1 is in the right place
            else:
                if check_if_in_right_spot(bedrooms,desired_bix,1):
                    do_it = True
            if do_it:
                F = {
                    'type' : 'b',
                    'b_ix' : full_bix,
                    'r_ix' : full_rix
                }
                T = {
                    'type' : 'b',
                    'b_ix' : desired_bix,
                    'r_ix' : empty_rix
                }
                route,r = get_route(F,T,bedrooms,hallway)
                route_is_valid = validate_route(route,r)
                if route_is_valid:
                    return F,T

def check_if_in_right_spot(bedrooms,b_ix,r_ix):
    if bedrooms[b_ix][r_ix] == get_other_type(b_ix):
        return True
    return False

def get_other_type(x):
    letter_dict = {0:'A',1:'B',2:'C',3:'D'}
    letter_dict_rev = {'A':0,'B':1,'C':2,'D':3}
    if isinstance(x,int):
        return letter_dict[x]
    else:
        return letter_dict_rev[x]
        

def get_bedroom(i,bedrooms,typ1,typ2):
    ## typ1 - empty or full
    ## typ2 - top or bottom
    if typ1 == "empty":
        A = ["."]
    else:
        A = ["A","B","C","D"]
    if typ2 == "top":
        R = [0,1]
    else:
        R = [1,0]

    for r in R:
        if bedrooms[i][r] in A:
            return r
    return False

def get_route(from_details,to_details,bedrooms,hallway):
    ## Travel the route to ensure it's empty
    route = []
    r = []
    if from_details['type'] == "b":
        if from_details['r_ix'] == 1:
            route.append(bedrooms[from_details['b_ix']][0])
            r.append(f"b-{from_details['b_ix']}-0")
        h_ix = get_hix_from_bix(from_details['b_ix'])
        route.append(hallway[h_ix])
        r.append(f"h{h_ix}")
    else:
        h_ix = from_details['h_ix']
    if to_details['type'] == "b":
        h_ix_dest = get_hix_from_bix(to_details['b_ix'])
    else:
        h_ix_dest = to_details['h_ix']
    if h_ix < h_ix_dest:
        for j in range(h_ix,h_ix_dest+1):
            route.append(hallway[j])
            r.append(f"h{j}")
    elif h_ix > h_ix_dest:
        for j in range(h_ix,h_ix_dest-1,-1):
            route.append(hallway[j])
            r.append(f"h{j}")
    else:
        raise IndexError('this shouldnt happen')
    if to_details['type'] == "b":
        route.append(bedrooms[to_details['b_ix']][0])
        r.append(f"b-{to_details['b_ix']}-0")
        if to_details['r_ix'] == 1:
            route.append(bedrooms[to_details['b_ix']][1])
            r.append(f"b-{to_details['b_ix']}-1")
    return route,r

def get_hix_from_bix(br):
    return ((br + 1) * 2)

def validate_route(route,r):
    for R,RR in zip(route[1:],r[1:]):
        if R != ".":
            # raise ValueError(f"spot `{RR}` taken")
            return False
    return True

def move_out_the_way(bedrooms,hallway,starting_b_ix=None):
    if starting_b_ix:
        if check_if_in_right_spot(bedrooms,starting_b_ix,1):
            ## Get current b_ix of the amphibod who will replace this one
            replacement_bix = get_replacement_bixs(starting_b_ix,bedrooms,True)
            eventual_b_dest = bedrooms[starting_b_ix][0]
            from_details = {
                'type' : 'b',
                'b_ix' : starting_b_ix,
                'r_ix' : 0
            }
            ## Work out how to most efficiently get out the way
            to_details = get_most_efficent_evasion(starting_b_ix,[replacement_bix],eventual_b_dest)
        else:
            if check_if_in_right_spot(bedrooms,starting_b_ix,0):
                ## Top is in the right place, bottom isn't
                ## Top should move 1 spot in the opposite direction to where bottom wants to go
                if get_other_type(bedrooms[starting_b_ix][1]) < get_hix_from_bix(starting_b_ix):
                    ## left
                    to_details = {
                        'type' : 'h',
                        'h_ix' : get_hix_from_bix(starting_b_ix) + 1
                    }
                else:
                    ## right
                    to_details = {
                        'type' : 'h',
                        'h_ix' : get_hix_from_bix(starting_b_ix) - 1
                    }
            else:
                pass

    else:
        raise ValueError('logic needed')
    return from_details,to_details

def get_replacement_bixs(my_ix,bedrooms,single):
    rm = []
    for b in range(4):
        if b != my_ix:
            for r in range(2):
                if bedrooms[b][r] == get_other_type(my_ix):
                    if single:
                        return b
                    else:
                        rm.append(b)
    return rm

def get_most_efficent_evasion(my_b_ix,to_replace_ixs,eventual_b_dest):
    if len(to_replace_ixs) == 2:
        ## If I'm in between them, move to the closest side
        if (to_replace_ixs[0] < my_b_ix) & (my_b_ix < to_replace_ixs[1]):
            quicker_route = choose_quicker_route(
                options=[1,9],
                start_pos=get_hix_from_bix(my_b_ix),
                end_pos=get_hix_from_bix(eventual_b_dest)
            )
            return {
                'type' : 'h',
                'h_ix' : quicker_route
            }
    ## If the blockers are to the left
    elif to_replace_ixs[0] < my_b_ix:
        quicker_route = choose_quicker_route(
            options=[
                get_hix_from_bix(to_replace_ixs[0]) - 1,
                get_hix_from_bix(my_b_ix) + 1
            ],
            start_pos=get_hix_from_bix(my_b_ix),
            end_pos=get_hix_from_bix(eventual_b_dest)
        )
        return {
            'type' : 'h',
            'h_ix' : quicker_route
        }
    else:
        quicker_route = choose_quicker_route(
            options=[
                get_hix_from_bix(to_replace_ixs[0]) + 1,
                get_hix_from_bix(my_b_ix) - 1
            ],
            start_pos=get_hix_from_bix(my_b_ix),
            end_pos=get_hix_from_bix(eventual_b_dest)
        )
        return {
            'type' : 'h',
            'h_ix' : quicker_route
        }

def choose_quicker_route(options,start_pos,end_pos):
    """
    Work out which of the two routes below are shorter
        start_pos -> option1 -> end_pos
        start_pos -> option2 -> end_pos
    All of the above are hallway indexes
    """
    routes = {}
    for option in options:
        routes[option] = abs(option - start_pos) + abs(end_pos - option)
    return min(routes,key=routes.get)