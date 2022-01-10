import requests
import math

input_url = "https://adventofcode.com/2021/day/17/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)



def get_answers():
    STRING = """
    23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
    25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
    8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
    26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
    20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
    25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
    25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
    8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
    24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
    7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
    23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
    27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
    8,-2    27,-8   30,-5   24,-7
    """
    A = STRING.split("\n")
    B = []
    for a in A:
        if a != "":
            a1 = a.replace("  ","&")
            a2 = a1.replace(" ","&")
            a3 = a2.replace("&&","&")
            a4 = a3.split("&")
            for aa in a4:
                if aa != "":
                    xxx,yyy = [
                        int(z)
                        for z in aa.split(",")
                    ]
                    B.append((xxx,yyy))
    return B

input_str = """
target area: x=20..30, y=-10..-5
"""
input_str = input_req.text

X,Y = input_str.replace("target area: ","").split(", ")

x_min,x_max = [
    int(x)
    for x in X.replace("x=","").split("..")
]
y_min,y_max = [
    int(x)
    for x in Y.replace("y=","").split("..")
]

def check_if_in_target_area(cx,cy,x_min,x_max,y_min,y_max,dy):
    yes_X = (cx >= x_min) & (cx <= x_max)
    yes_Y = (cy >= y_min) & (cy <= y_max)
    if yes_X & yes_Y:
        return 1 #'yes'
    elif (cy < y_min) & (dy <= 0):
        return -1 #'no'
    else:
        return 0 #'continue'

"""
<Y>
S = y + 1 + y + y_distance = 2y + y_distance + 1
=> y = 0.5 * (S - y_distance - 1)

<X>
x_distance =< (x**2 + x)/2
"""

def get_biggest_y(y_min,y_max):
    if y_max < 0:
        return -1 * (y_min + 1)
    else:
        return y_max - 1

def steps_to_get_to_max_height(vy):
    cy = 0
    s = 0
    while vy > 0:
        cy += vy
        vy -= 1
        s += 1
    return cy,s

def get_smallest_x(mx):
    a = 0.5
    b = 0.5
    c = -1 * mx
    result1 = (-b + math.sqrt(b**2 - 4*a*c)) / (2 * a)
    result2 = (-b - math.sqrt(b**2 - 4*a*c)) / (2 * a)
    return max(math.ceil(result1),math.ceil(result2))
    # return math.ceil(result1),math.ceil(result2)



def check_v(x,y,x_min,x_max,y_min,y_max,P=False,P2=False):
    ix = vx = x
    iy = vy = y
    cx = cy = 0
    step = 1
    max_x = 0
    while True:
        cx += vx
        max_x = max(cx,max_x)
        cy += vy
        result = check_if_in_target_area(cx,cy,x_min,x_max,y_min,y_max,vy)
        if P2:        
            print(step,cx,cy)
        if result == 1:
            if P:
                print(f"{ix},{iy} works")
            return True
        elif result == -1:
            if P:
                print(f"{ix},{iy} doesn't work")
            return False
        vx = max(0,vx-1)
        vy -= 1
        step += 1


## Part 1
smallest_x = get_smallest_x(x_min)
biggest_y = get_biggest_y(y_min,y_max)
result = steps_to_get_to_max_height(biggest_y)
print(result[0])


# def get_possible_x_vals(x_min,x_max):
#     rm = []
#     non_movers = []
#     for mx in range(x_min,x_max+1):
#         v0 = get_smallest_x(mx)
#         non_movers.append(v0)
#         for v in range(v0,mx+1):
#             rm.append(v)
#     return list(set(rm)),list(set(non_movers))

def get_smallest_x2(mx,last=False):
    a = 0.5
    b = 0.5
    c = -1 * mx
    result1 = (-b + math.sqrt(b**2 - 4*a*c)) / (2 * a)
    result2 = (-b - math.sqrt(b**2 - 4*a*c)) / (2 * a)
    if last:
        return max(math.floor(result1),math.floor(result2))
    else:
        return max(math.ceil(result1),math.ceil(result2))

def get_finishing_position(x):
    return 0.5 * ((x**2) + x)

def get_non_movers(mino,x_min,x_max):
    X = mino
    non_movers = []
    while True:
        res = get_finishing_position(X)
        if (x_min <= res) & (res <= x_max):
            non_movers.append(X)
        elif res > x_max:
            break
        X += 1
    return non_movers

def get_possible_x_vals(x_min,x_max):
    ## Get min value
    mino = get_smallest_x(x_min)
    non_movers = get_non_movers(mino,x_min,x_max)
    rm = non_movers.copy()
    for xx in range(x_min,x_max+1):
        rm.append(xx)
    for xx in range(rm[0]+1,x_min):
        gets_in_zone = does_get_in_zone(xx,x_min,x_max)
        if gets_in_zone:
            rm.append(xx)
    return list(set(rm)),list(set(non_movers))

def does_get_in_zone(xx,x_min,x_max):
    if xx == 0:
        return False
    cx = 0
    vx = xx
    while vx != 0:
        cx += vx
        vx = max(0,vx-1)
        if (x_min <= cx) & (cx <= x_max):
            return True
        if cx > x_max:
            return False

def get_steps(x,x_min,x_max,non_movers):
    is_non_mover = x in non_movers
    vx = x
    cx = 0
    step = 0
    steps = []
    while True:
        step += 1
        cx += vx
        if is_non_mover:
            if step >= x:
                break
        if (x_min <= cx) & (cx <= x_max):
            steps.append(step)
        elif cx > x_max:
            break
        vx -= 1
    return steps

def get_starting_y(x,y_min,y_max,M3):
    X = 0
    while True:
        current_height,M3 = get_height_at_step(x,X,M3)
        if current_height >= y_min:
            X -= 1
        else:
            return X,M3
    return 0,M3

def does_get_in_zone_y(yy,y_min,y_max,M3):
    ## For this starting_y, cy hits 0 at step `height0step`
    height0step = max(0,(2 * yy) + 1)
    cy,vy,M3 = get_height_at_step(height0step,yy,M3,cv=True)
    step = height0step
    while cy >= y_min:
        step += 1
        cy += vy
        vy -= 1
        M3[(step,yy)] = (cy,vy)
        if (y_min <= cy) & (cy <= y_max):
            return True,M3
        
    return False,M3

def do_non_movers(x,y_min,y_max,M3):
    ## If at step x (when x velocity == 0), heights > y_min
    # if x == 15:
    #     a=1
    R = []
    # if y_max < 0:
    #     x_limit = -1 * (y_min + 1)
    # else:
    #     starting_x = y_max - 1
    x_limit = -1 * (y_min + 1)
    y_dist = y_max - y_min + 1
    starting_y,M3 = get_starting_y(x,y_min,y_max,M3)
    while starting_y <= x_limit:
        # if starting_y == 80:
        #     a=1
        if ((y_max * -1) <= starting_y) & (starting_y <= (y_min * -1)):
            R.append(starting_y)
        else:
            # current_height,current_velocity,M3 = get_height_at_step(x-1,starting_y,M3,cv=True)
            # max_height_drop = current_height - y_min + 1
            # if (current_height >= y_min) & (current_velocity <= max_height_drop):
            #     R.append(starting_y)
            does_get_in,M3 = does_get_in_zone_y(starting_y,y_min,y_max,M3)
            if does_get_in:
                R.append(starting_y)

        # else:
        #     break
        starting_y += 1
    return R,M3


def get_all_ys(S,x,y_min,y_max,M2,M3):
    C = []
    if x == 7:
        a=1
    if S == []:
        # if y_max < 0:
        #     for yy in range(y_min,y_max+1):
        #         C.append(-1 * (yy + 1))
        # else:
        #     for yy in range(y_min,y_max+1):
        #         C.append(yy - 1)
        R,M3 = do_non_movers(x,y_min,y_max,M3)
        C.extend(R)
    else:
        for ss in S:
            if ss not in M2:
                if ss == 2:
                    a=1
                yL,M3 = get_ys(ss,y_min,y_max,M3)
                M2[ss] = yL
            else:
                yL = M2[ss]
            C.extend(yL)

    return C,M2,M3

def get_ys(ss,y_min,y_max,M3):
    A = []
    v = 1
    while True:
        res,M3 = get_height_at_step(ss,v,M3)
        if (y_min <= res) & (res <= y_max):
            A.append(v)
        elif res > y_max:
            break
        v += 1
    v = 0
    while True:
        res,M3 = get_height_at_step(ss,v,M3)
        if (y_min <= res) & (res <= y_max):
            A.append(v)
        elif res < y_max:
            break
        v -= 1
    return A,M3

def get_height_at_step(ss,v,M3,cv=False):
    if (ss,v) in M3:
        if cv:
            m = M3[(ss,v)]
            return m[0],m[1],M3
        else:
            return M3[(ss,v)][0],M3
    elif (ss-1,v) in M3:
        last_height,last_velocity = M3[(ss-1,v)]
        new_height = last_height + last_velocity
        new_velocity = last_velocity - 1
        M3[(ss,v)] = (new_height,new_velocity)
        if cv:
            return new_height,new_velocity,M3
        else:
            return new_height,M3
    else:
        cx = 0
        velo = v
        for step in range(1,ss+1):
            cx += velo
            velo -= 1
            M3[(step,v)] = (cx,velo)
        if cv:
            return cx,velo,M3
        else:
            return cx,M3



def get_combos_for_x_vals(xv,non_movers,x_min,x_max,y_min,y_max):
    L = []
    M = {}
    M2 = {}
    M3 = {}
    for x in xv:
        ## For which step(s) is x in the target area
        if x in non_movers:
            S = []
            # Sk = x
            S2 = get_steps(x,x_min,x_max,non_movers)
            # S2k = 
            y_list = []
            for SS in [S,S2]:
                y_list0,M2,M3 = get_all_ys(SS,x,y_min,y_max,M2,M3)
                y_list.extend(y_list0)
            
        else:
            if x == 76:
                a=1
            S = get_steps(x,x_min,x_max,non_movers)
            if S == [2]:
                a=1
            Sk = tuple(S)
            if Sk not in M:
                y_list,M2,M3 = get_all_ys(S,x,y_min,y_max,M2,M3)
                M[Sk] = y_list
            else:
                y_list = M[Sk]
        for y in y_list:
            L.append((x,y))
    return set(L)

xv,non_movers = get_possible_x_vals(x_min,x_max)
C = get_combos_for_x_vals(xv,non_movers,x_min,x_max,y_min,y_max)
print(len(C))
a=1

B = get_answers()

# my_extra = [
#     x
#     for x in C
#     if x not in B
# ]
# my_forgotten = [
#     x
#     for x in B
#     if x not in C
# ]

my_extra2 = [
    (x,y)
    for x,y in C
    if not check_v(x,y,x_min,x_max,y_min,y_max,P=False)
]

## bigger than 5058
## M3[(step,initial_y_velocity)] = (new_height,new_velocity)

b=1


for xxx in xv:
    for yyy in range(-30,160):
        works = check_v(xxx,yyy,x_min,x_max,y_min,y_max)
        recorded = (xxx,yyy) in C
        if works != recorded:
            print(xxx,yyy)
a=1