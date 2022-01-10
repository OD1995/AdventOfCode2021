import requests

input_url = "https://adventofcode.com/2021/day/8/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)

num_dict = {
    0 : 6,
    1 : 2,
    2 : 5,
    3 : 5,
    4 : 4,
    5 : 5,
    6 : 6,
    7 : 3,
    8 : 7,
    9 : 6
}

dict_num = {}
for k,v in num_dict.items():
    if v not in dict_num:
        dict_num[v] = k
    # else:
    #     dict_num[v] = dict_num[v] + [k]

D = {
    0 : ['a','b','c','e','f','g'],
    1 : ['c','f'],
    2 : ['a','c','d','e','g'],
    3 : ['a','c','d','f','g'],
    4 : ['b','c','d','f'],
    5 : ['a','b','d','f','g'],
    6 : ['a','b','d','e','f','g'],
    7 : ['a','c','f'],
    8 : ['a','b','c','d','e','f','g'],
    9 : ['a','b','c','d','f','g']
}

input_str = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

input_str = input_req.text
rows = input_str.split("\n")


## Part 1
count = 0
for row in rows:
    if row == "":
        continue
    words = row.split(" | ")[1].split(" ")
    word_lens = [
        len(x)
        for x in words
    ]
    for L in word_lens:
        if L in [2,4,3,7]:
            count += 1
print(count)

## Part 2
def overlap(A,B,known):
    rm = []
    for a in A:
        if (a in B) & (a not in known):
            rm.append(a)
    if len(rm) == 1:
        return rm[0],known+rm
    else:
        return rm,known
total_answer = 0
for row in rows:
    if row == "":
        continue
    A,B = row.split(" | ")
    answers = {}
    known = []
    len_dict = {}
    for W in A.split(" "):
        if len(W) not in len_dict:
            len_dict[len(W)] = [W]
        else:
            len_dict[len(W)].append(W)
    ## a = 7[3] - 1[2]
    a_answer = (set(len_dict[3][0]) - set(len_dict[2][0])).pop()
    # answers[a_answer] = 'a'
    answers['a'] = a_answer
    known.append(a_answer)


    for W in A.split(" "):
        if len(W) in [2,4,3,7]:
            for L in D[dict_num[len(W)]]:
                if L not in answers:
                    answers[L] = list(W)
                else:
                    if isinstance(answers[L],list):
                        answers[L],known = overlap(answers[L],list(W),known)
    ## Diff between 8[7] and 0,6,9 (all [6]) is one of d,c,e
    new_letters = [
        (set(len_dict[7][0]) - set(X)).pop()
        for X in len_dict[6]
    ]
    for _L_ in ['d','c','e']:
        answers[_L_],known = overlap(answers[_L_],new_letters,known)
    while True:
        old_known_len = len(known)
        for N in D[8]:
            if isinstance(answers[N],list):
                answers[N],known = overlap(answers[N],D[8],known)
        if len(known) == old_known_len:
            break
    answers_rev = {x:y for y,x in answers.items()}
    this_D = {
        tuple(
            sorted(
                [
                    answers[v]
                    for v in val
                ]
            )
        ) : key
        for key,val in D.items()
    }
    answer = ""
    for b in B.split(" "):
        answer += str(this_D[tuple(sorted(b))])
    total_answer += int(answer)

print(total_answer)