from multiprocessing.sharedctypes import Value
from operator import ixor


input_str = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""

energy_usage = {
    'A' : 1,
    'B' : 10,
    'C' : 100,
    'D' : 1000
}


slots = []
for line in input_str.split("\n"):
    a = line.replace("#","").replace(".","").replace(" ","")
    if a != "":
        slots.append(list(a))


hallway = ["."]*11
bedrooms = {
    ix : [slots[0][ix],slots[1][ix]]
    for ix in range(4)
}

def display(hallway,bedrooms):
    print("#"*13)
    print("#" + "".join(hallway) + "#")
    b1 = [
        x[0]
        for x in bedrooms.values()
    ]
    print("###" + "#".join(b1) + "###")
    b2 = [
        x[1]
        for x in bedrooms.values()
    ]
    print("  #" + "#".join(b2) + "#")
    print("  " + "#"*9)
    print("\n\n")

def get_outside_br_ix(br):
    return ((br + 1) * 2)

def flatten(L):
    return [x for y in L for x in y]

def get_empty_bedroom_ixs(bedrooms,rev=False):
    R = [1,0] if rev else [0,1]
    for b in range(4):
        for r in R:
            if bedrooms[b][r] == ".":
                return {
                    'type' : 'b',
                    'b_ix' : b,
                    'r_ix' : r
                }
    return False



def check_bedrooms(bedrooms):
    a = flatten(
        [
            [bedrooms[b][x] for b in range(4)]
            for x in range(2)
        ]
    )
    return "".join(a) != 'ABCDABCD'

def move(from_details,hallway,bedrooms,moves,starting_b_ix,i):
    if i == 5:
        a=1
    letter_dict = {
        0 : 'A',
        1 : 'B',
        2 : 'C',
        3 : 'D'
    }
    letter_dict_rev = {
        'A' : 0,
        'B' : 1,
        'C' : 2,
        'D' : 3
    }
    ## If any of the beds are empty, I'm probably moving into it
    result = get_empty_bedroom_ixs(bedrooms,True)
    if result:
        if from_details['type'] == 'b':
            from_letter = bedrooms[from_details['b_ix']][from_details['r_ix']]
        else:
            from_letter = hallway[from_details['h_ix']]
        to_letter = letter_dict[result['b_ix']]
    # else:
    #     from_letter = to_letter = True
    if (result):
        if (from_letter == to_letter):
            if from_details['type'] == 'b':
                ## Unless the bed is the one above the one I'm supposed to be moving
                if (result['b_ix'] == from_details['b_ix']) & (result['r_ix'] == from_details['r_ix'] - 1):
                    move_out_the_way = True
                else:
                    move_out_the_way = False
            else:
                move_out_the_way = False
        else:
            move_out_the_way = True
    else:
        move_out_the_way = True
    if move_out_the_way:
        ## Get ixs of the amphipods that I'm getting out the way for
        to_replace_ixs = get_replace_ixs(from_details['b_ix'],bedrooms,letter_dict)
        ## If the list is empty, the amphipod referenced in from_details is
        ##    moving out of the way for the amphipod below it
        if to_replace_ixs == []:
            if from_details['r_ix'] == 1:
                raise ValueError('this shouldnt happen')
            to_details = get_most_efficient_unblocking(from_details,bedrooms,hallway)
        else:
            ## Work out where to go most efficiently, to not get in the way of their route
            mover = bedrooms[from_details['b_ix']][from_details['r_ix']]
            eventual_b_dest = letter_dict_rev[mover]
            to_details = get_most_efficent_evasion(from_details['b_ix'],to_replace_ixs,eventual_b_dest)
    else:
        to_details = result
    ## Do the move
    hallway,bedrooms,moves = do_move(from_details,to_details,hallway,bedrooms,moves)
    ## Work out the next move
    if move_out_the_way:
        ## First check if there are any empty beds that can be filled by hallway lurkers
        empty_to_be_filled = get_empty_to_be_filled(bedrooms,hallway,letter_dict)
        if empty_to_be_filled:
            from_details = empty_to_be_filled
        else:
            # if len(to_replace_ixs) == 1:
            r_ix = get_r_ix(bedrooms,from_details['b_ix'],letter_dict,to_replace_ixs[0])
            ## If the one we want to move is blocked, move the blocker instead
            if (r_ix == 1) & (bedrooms[to_replace_ixs[0]][0] != "."):
                from_details = {
                    'type' : 'b',
                    'b_ix' : to_replace_ixs[0],
                    'r_ix' : 0,
                    'source' : 'A'
                }
            else:
                from_details = {
                    'type' : 'b',
                    'b_ix' : to_replace_ixs[0],
                    'r_ix' : r_ix,
                    'source' : 'B'
                }
        # else:
        #     ## Decide which one to do next
        #     pass
    else:
        ## First, check if we're done
        not_done = check_bedrooms(bedrooms)
        if not_done:
            result2 = get_from_details(bedrooms,starting_b_ix,hallway)
            if result2:
                from_details = result2
            else:
                ## Letter is blocked in and needs getting out
                from_details = get_blocker_out(bedrooms)
        else:
            from_details = {}

    return from_details,moves,hallway,bedrooms

def get_most_efficient_unblocking(from_details,bedrooms,hallway):
    ## Get letter we're unblocking for and work out where it needs to go
    u = bedrooms[from_details['b_ix']][1]
    ## Some logic for when they're all to the left
    
    ## Don't write logic for when they're on either side until we have an example
    ## Raise error to catch that example

def get_blocker_out(bedrooms):
    # row0 = [bedrooms[b][0] for b in range(4)]
    row1 = [bedrooms[b][1] for b in range(4)]
    for i,L in enumerate(['A','B','C','D']):
        if row1[i] != L:
            return {
                'type' : 'b',
                'b_ix' : i,
                'r_ix' : 0,
                'source' : 'get_blocker_out'
            }
    raise ValueError('this shouldnt happen')

def get_empty_to_be_filled(bedrooms,hallway,letter_dict):
    mts = []
    for b in range(4):
        for r in [1,0]:
            if bedrooms[b][r] == ".":
                mts.append(letter_dict[b])
    move_ix = False
    for ix,c in enumerate(hallway):
        if c in mts:
            move_ix = ix
    if move_ix == False:
        return False
    else:
        return {
            'type' : 'h',
            'h_ix' : move_ix,
            'source' : 'get_empty_to_be_filled'
        }

def get_from_details(bedrooms,starting_b_ix,hallway):
    xp = [
        ['A','A'],
        ['B','B'],
        ['C','C'],
        ['D','D']
    ]
    D = {
        0 : [0,1,2,3],
        1 : [1,2,3,0],
        2 : [2,3,0,1],
        3 : [3,0,1,2]
    }
    hallway_ixs = [
        ix
        for ix,v in enumerate(hallway)
        if v != "."
    ]
    for b in D[starting_b_ix]:
        allowed_letters = get_allowed_letters(b,hallway_ixs)
        for r in range(2):
            if (bedrooms[b][r] not in [".",xp[b][r]]) & (bedrooms[b][r] in allowed_letters):
                a=1
                return {
                    'type' : 'b',
                    'b_ix' : b,
                    'r_ix' : r,
                    'source' : 'get_from_details'
                }
    # raise ValueError('this shouldnt happen')
    return False

def get_allowed_letters(b,hallway_ixs):
    letter_dict = {
        0 : 'A',
        1 : 'B',
        2 : 'C',
        3 : 'D'
    }
    letter_dict2 = {
        'A' : 2,
        'B' : 4,
        'C' : 6,
        'D' : 8
    }
    allowed_letters = []
    min_hallway_ixs = min(hallway_ixs)
    max_hallway_ixs = max(hallway_ixs)
    if b == 0:
        for k,v in letter_dict2.items():
            if min_hallway_ixs > v:
                allowed_letters.append(k)
    elif b in [1,2]:
        b_ix = get_outside_br_ix(b)
        ## Left
        left_ixs = [x for x in hallway_ixs if x < b_ix]
        if len(left_ixs) == 0:
            for i in range(b):
                allowed_letters.append(letter_dict[i])
        else:
            for i in range(b):
                if max(left_ixs) < get_outside_br_ix(i):
                    allowed_letters.append(letter_dict[i])
        ## Right
        right_ixs = [x for x in hallway_ixs if x > b_ix]
        if len(right_ixs) == 0:
            for j in range(b,4):
                allowed_letters.append(letter_dict[j])
        else:
            for j in range(b,4):
                if min(right_ixs) > get_outside_br_ix(i):
                    allowed_letters.append(letter_dict[j])
    elif b == 3:
        for k,v in letter_dict2.items():
            if max_hallway_ixs < v:
                allowed_letters.append(k)
    return allowed_letters

def get_r_ix(bedrooms,my_ix,letter_dict,iix):
    for r in [1,0]:
        if bedrooms[iix][r] == letter_dict[my_ix]:
            return r
    raise ValueError('this shouldnt happen')

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

def get_most_efficent_evasion(my_b_ix,to_replace_ixs,eventual_b_dest):
    # if eventual_b_dest is not None:
    #     eventual_direction = "left" if my_b_ix > eventual_b_dest else "right"
    # else:
    #     eventual_direction = 'n/a'
    if len(to_replace_ixs) == 2:
        ## If I'm in between them, move to the closest side
        if (to_replace_ixs[0] < my_b_ix) & (my_b_ix < to_replace_ixs[1]):
            # if my_b_ix < 2:
            #     R = 'far left'
            # else:
            #     R = 'far right'
            quicker_route = choose_quicker_route(
                options=[1,9],
                start_pos=get_outside_br_ix(my_b_ix),
                end_pos=get_outside_br_ix(eventual_b_dest)
            )
            return {
                'type' : 'h',
                'h_ix' : quicker_route
            }
    ## If the blockers are to the left
    elif to_replace_ixs[0] < my_b_ix:
        # if eventual_direction == "left":
        #     return {
        #     'type' : 'h',
        #     'h_ix' : get_outside_br_ix(to_replace_ixs[0]) - 1
        # }
        # else:
        #     R = 'just right'
        quicker_route = choose_quicker_route(
            options=[
                get_outside_br_ix(to_replace_ixs[0]) - 1,
                get_outside_br_ix(my_b_ix) + 1
            ],
            start_pos=get_outside_br_ix(my_b_ix),
            end_pos=get_outside_br_ix(eventual_b_dest)
        )
        return {
            'type' : 'h',
            'h_ix' : quicker_route
        }
    else:
        # if eventual_direction == 'right':
        #     return {
        #     'type' : 'h',
        #     'h_ix' : get_outside_br_ix(to_replace_ixs[0]) + 1
        # }
        # else:
        #     R = 'just left'
        quicker_route = choose_quicker_route(
            options=[
                get_outside_br_ix(to_replace_ixs[0]) + 1,
                get_outside_br_ix(my_b_ix) - 1
            ],
            start_pos=get_outside_br_ix(my_b_ix),
            end_pos=get_outside_br_ix(eventual_b_dest)
        )
        return {
            'type' : 'h',
            'h_ix' : quicker_route
        }

    # if R == 'far left':
    #     return {
    #         'type' : 'h',
    #         'h_ix' : 1
    #     }
    # if R == 'far right':
    #     return {
    #         'type' : 'h',
    #         'h_ix' : 9
    #     }
    # if R == 'just left':
    #     return {
    #         'type' : 'h',
    #         'h_ix' : get_outside_br_ix(my_b_ix) - 1
    #     }
    # if R == 'just right':
    #     return {
    #         'type' : 'h',
    #         'h_ix' : get_outside_br_ix(my_b_ix) + 1
    #     }

def get_replace_ixs(my_ix,bedrooms,letter_dict):
    rm = []
    for b in range(4):
        if b != my_ix:
            for r in range(2):
                if bedrooms[b][r] == letter_dict[my_ix]:
                    rm.append(b)
    return rm

def do_move(from_details,to_details,hallway,bedrooms,moves):
    FD = {'type': 'b', 'b_ix': 3, 'r_ix': 0, 'source': 'get_blocker_out'}
    TD = {'type': 'b', 'b_ix': 0, 'r_ix': 0}
    if (from_details == FD) & (to_details == TD):
        a=1
    ##### 'b',bedroom_ix,0/1
    ##### 'h',hallway_ix
    route,r = get_route(from_details,to_details)
    ## Remove the mover from the map
    if from_details['type'] == "b":
        mover = bedrooms[from_details['b_ix']][from_details['r_ix']]
        bedrooms[from_details['b_ix']][from_details['r_ix']] = "."
    elif from_details['type'] == "h":
        mover = hallway[from_details['h_ix']]
        hallway[from_details['h_ix']] = "."
    ## Move mover into it's destination
    if to_details['type'] == "h":
        hallway[to_details['h_ix']] = mover
    else:
        bedrooms[to_details['b_ix']][to_details['r_ix']] = mover
    moves[mover] += len(route)
    return hallway,bedrooms,moves

def get_route(from_details,to_details):
    ## Travel the route to ensure it's empty
    route = []
    r = []
    if from_details['type'] == "b":
        if from_details['r_ix'] == 1:
            route.append(bedrooms[from_details['b_ix']][0])
            r.append(f"b-{from_details['b_ix']}-0")
        h_ix = get_outside_br_ix(from_details['b_ix'])
        route.append(hallway[h_ix])
        r.append(f"h{h_ix}")
    else:
        h_ix = from_details['h_ix']
    if to_details['type'] == "b":
        h_ix_dest = get_outside_br_ix(to_details['b_ix'])
    else:
        h_ix_dest = to_details['h_ix']
    if h_ix < h_ix_dest:
        A = h_ix
        B = h_ix_dest + 1
    elif h_ix > h_ix_dest:
        A = h_ix_dest
        B = h_ix + 1
    else:
        raise IndexError('this shouldnt happen')
    for j in range(A,B):
        route.append(hallway[j])
        r.append(f"h{j}")
    if to_details['type'] == "b":
        route.append(bedrooms[to_details['b_ix']][0])
        r.append(f"b-{to_details['b_ix']}-0")
        if to_details['r_ix'] == 1:
            route.append(bedrooms[to_details['b_ix']][1])
            r.append(f"b-{to_details['b_ix']}-1")
    # for R,RR in zip(route,r):
    #     if R != ".":
    #         raise ValueError(f"spot `{RR}` taken")
    return route,r

starting_moves = [
    [0,0],
    # [0,1],
    [1,0],
    # [1,1],
    [2,0],
    # [2,1],
    [3,0],
    # [3,1],
]
def manage_movement(starting_move,hallway,bedrooms):
    moves = {
        'A' : 0,
        'B' : 0,
        'C' : 0,
        'D' : 0
    }
    from_details = {
        'type' : 'b',
        'b_ix' : starting_move[0],
        'r_ix' : starting_move[1]
    }
    starting_b_ix = starting_move[0]
    steps = [(hallway,bedrooms)]
    i = 0
    while check_bedrooms(bedrooms):
        (
            from_details,moves,
            hallway,bedrooms
        ) = move(from_details,hallway,bedrooms,moves,starting_b_ix,i)
        print(i)
        display(hallway,bedrooms)
        steps.append((hallway,bedrooms))
        i += 1
        if i > 10:
            break
    a=1
    return moves

moves = manage_movement(starting_moves[2],hallway,bedrooms)