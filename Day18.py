import requests

input_url = "https://adventofcode.com/2021/day/18/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)

input_str = """
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
"""

input_str = """
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""

input_str = input_req.text

nums = [
    eval(x)
    for x in input_str.split("\n")
    if x != ""
]

nums2 = [
    x
    for x in input_str.split("\n")
    if x != ""
]

def check_list(Cr0,accum_left_bracks,i):
    ct = 0
    alb_len = min(i,len(accum_left_bracks))
    for i,c in enumerate(Cr0):
        if i == alb_len:
            return True,1
        if c == "[":
            ct += 1
        elif c == "]":
            ct -= 1
        if ct != accum_left_bracks[i]:
            return False,i
    return True,1

def add_numbers(A,B):
    C =[A] + [B]
    Cr = repr(C).replace(" ","")
    #print(Cr)
    last_A_ix = 0
    last_B_ix = 0
    finished = False
    accum_left_bracks = []
    while not finished:
        (
            Cr,last_A_ix,last_B_ix,
            old_alf,accum_left_bracks
            ,finished,arrows
        ) = evaluate_C(Cr,last_A_ix,last_B_ix,accum_left_bracks)
        #print("".join([str(x) for x in old_alf]))
        #print("".join(arrows))
        #print(Cr)
    return eval(Cr)

def evaluate_C(Cr0,last_A_ix,last_B_ix,accum_left_bracks):
    # if Cr0 == '[[[[[6,7],0],[6,7]],[[5,10],[26,0]]],[[2,[11,10]],[[0,8],[8,5]]]]':
    #     a=1
    ## A - find pairs nested inside 4 pairs
    Cr_len_orig = Cr_len = len(Cr0)
    try:
        sb_count = accum_left_bracks[last_A_ix-1]
    except IndexError:
        sb_count = 0
    sb_4 = False
    last_number_ix = None
    for i,cc in enumerate(Cr0[last_A_ix:],last_A_ix):
        if cc == "[":
            sb_count += 1
        elif cc == "]":
            sb_count -= 1
        elif cc.isnumeric():
            last_number_ix = i
        if sb_count == 5:
            sb_4 = True
            break
        try:
            accum_left_bracks[i] = sb_count
        except IndexError:
            if sb_count < 0:
                a=1
            accum_left_bracks.append(sb_count)
    # x,y = check_list(Cr0,accum_left_bracks,i)
    # assert x, y
    if sb_4:
        ## Find next close bracket
        j = i + 4
        while True:
            if Cr0[j] == "]":
                break
            j += 1
        explode_me = Cr0[i:j+1]
        left_num,right_num = eval(explode_me)
        # print(explode_me)
        ## Add left number to next number to the left
        Cr1,reset_last_B_ix,extra_L,newA = deal_with_left_number(Cr0,last_number_ix,left_num,last_A_ix)
        # j += extra_i2
        Cr_len += extra_L
        if reset_last_B_ix:
            last_B_ix = 0
        ## Add right number to next number to the right
        Cr2,extra_R = deal_with_right_number(Cr1,j+extra_L,right_num,Cr_len)
        Cr_len += extra_R
        ## Replace it with 0
        Cr3 = Cr2[:i+extra_L] + "0" + Cr2[j+1+extra_L:]
        arrows = [
            " " if w not in range(i,j+1) else "^"
            for w in range(Cr_len_orig)
        ]
        if newA:
            newAix = newA
        else:
            newAix = i-1
        return Cr3,max(0,newAix),last_B_ix,accum_left_bracks,accum_left_bracks[:newAix],False,arrows
    ## B - Find a number of 10 or greater
    m = last_B_ix
    double_digit_found = False
    while m < Cr_len:
        n = Cr0[m]
        if n.isnumeric():
            ## Keep going until we find a separator
            mm = m + 1
            while True:
                if Cr0[mm] in ["]",","]:
                    break
                mm += 1
            if mm > m + 1:
                double_digit_found = True
                break
        m += 1
    if double_digit_found:
        replacement_pair = get_replacement_pair(Cr0,m,mm)
        Cr1 = Cr0[:m] + str(replacement_pair).replace(" ","") + Cr0[mm:]
        arrows = [
            " " if i not in range(m,mm) else "^"
            for i in range(Cr_len_orig)
        ]        
        return Cr1,max(0,m-1),mm-1,accum_left_bracks,accum_left_bracks[:m-1],False,arrows

    return Cr0,0,0,[],[],True,""
    
def get_replacement_pair(Cr,m,mm):
    dd = int(Cr[m:mm])
    replacement = [
        int(dd/2),
        int(dd/2) if dd % 2 == 0 else int((dd/2)+0.5)
    ]
    return replacement

def deal_with_left_number(Cr,last_number_ix,left_num,last_A_ix):
    if last_number_ix is not None:
        lni = last_number_ix
        ## First make sure the number is single digit
        while Cr[lni-1] not in [",","["]:
            lni -= 1
        last_number = int(Cr[lni:last_number_ix+1])
        new_last_number = last_number + left_num
        extra_chars = len(str(new_last_number)) - len(str(last_number))
        Cr = Cr[:lni] + str(new_last_number) + Cr[last_number_ix+1:]
        return Cr,True,extra_chars,lni
    elif last_A_ix != 0:
        ## Go backwards from last_A_ix to find last number
        ix = last_A_ix
        end_ix = False
        while ix >= 0:
            v = Cr[ix]
            if not end_ix:
                if v.isnumeric():
                    end_ix = ix
            else:
                if v in [',','[']:
                    break
            ix -= 1
        if end_ix:
            last_number = int(Cr[ix+1:end_ix+1])
            new_last_number = last_number + left_num
            extra_chars = len(str(new_last_number)) - len(str(last_number))
            Cr = Cr[:ix+1] + str(new_last_number) + Cr[end_ix+1:]
            return Cr,True,extra_chars,ix
        else:
            return Cr,False,0,0
    return Cr,False,0,0

def deal_with_right_number(Cr,j,right_num,Cr_len):
    ## Find next number
    k = j + 2
    number_found = False
    seperator_found = False
    extra_chars = 0
    while k < Cr_len:
        S = Cr[k]
        if not number_found:
            if S.isnumeric():
                number_found = True
                ix = k
        else:
            if S in ["]",","]:
                seperator_found = True
                break
        k += 1
    if seperator_found:
        next_number = int(Cr[ix:k])
        new_next_number = next_number + right_num
        extra_chars = len(str(new_next_number)) - len(str(next_number))
        Cr = Cr[:ix] + str(new_next_number) + Cr[k:]
    return Cr,extra_chars

def get_magnitude(R):
    res = 0
    if isinstance(R[0],int):
        res += R[0] * 3
    else:
        res += get_magnitude(R[0]) * 3
    if isinstance(R[1],int):
        res += R[1] * 2
    else:
        res += get_magnitude(R[1]) * 2
    return res

# AA = [
#     ([[1,2],[[3,4],5]] , 143),
#     ([[[[0,7],4],[[7,8],[6,0]]],[8,1]] , 1384),
#     ([[[[1,1],[2,2]],[3,3]],[4,4]] , 445),
#     ([[[[3,0],[5,3]],[4,4]],[5,5]] , 791),
#     ([[[[5,0],[7,4]],[5,5]],[6,6]] , 1137),
#     ([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] , 3488)
# ]
# for a,b in AA:
#     assert get_magnitude(a) == b
# c=1
# Xs = [
#     ['[[[[[9,8],1],2],3],4]','[[[[0,9],2],3],4]'],
#     ['[7,[6,[5,[4,[3,2]]]]]','[7,[6,[5,[7,0]]]]'],
#     ['[[6,[5,[4,[3,2]]]],1]','[[6,[5,[7,0]]],3]'],
#     ['[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]','[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'],
#     ['[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]','[[3,[2,[8,0]]],[9,[5,[7,0]]]]']
# ]

# for X,Y in Xs:
#     a,b = evaluate_C(eval(X),0)
#     print(a==Y)
        
# a=1
if 0:
    ### TEST 1
    A = [[[[4,3],4],4],[7,[[8,4],9]]]
    B = [1,1]
    X = [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
    R = add_numbers(A,B)
    print(R==X)
if 0:
    ### TEST 2
    ANSWERS = [
        [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]],
        [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]
    ]
    R = nums[0]
    for i in range(1,len(nums)):
        if i == 2:
            a=1
        print("\n",i)
        R = add_numbers(R,nums[i])
        # print(R==ANSWERS[i-1])
        # if R != ANSWERS[i-1]:
        #     break
    # X = [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]
    X = [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]
    print(X==R)
    print(get_magnitude(R))
    a=1
if 0:
    ### PART 1
    R = nums[0]
    for i in range(1,len(nums)):
        if i == 2:
            a=1
        print("\n",i)
        R = add_numbers(R,nums[i])
    print(get_magnitude(R))

if 1:
    ### PART 2
    MAX = 0
    for i in nums:
        for j in nums:
            R = add_numbers(i,j)
            M = get_magnitude(R)
            x = "same" if i == j else ""
            print(M,x)
            MAX = max(MAX,M)
    print(MAX)
