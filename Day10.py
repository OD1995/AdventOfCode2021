import requests

input_url = "https://adventofcode.com/2021/day/10/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)


input_str = """
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""

input_str = input_req.text

lines = [
    # list(x)
    x
    for x in input_str.split("\n")
    if x != ""
]

def get_type(line,opens,closes):
    char_pairs = [
        opens[i] + closes[i]
        for i in range(4)
    ]
    after_len = 0
    before_len = 1
    # print(line)
    while after_len < before_len:
        before_len = len(line)
        for cp in char_pairs:
            line = line.replace(cp,"")
        after_len = len(line)
        # print(line)
    if len(line) == 0:
        return "ok",line
    closes_counts = 0
    for c in closes:
        closes_counts += line.count(c)
    if closes_counts == 0:
        return "incomplete",line
    return "corrupted",line

opens = ["[","(","{","<"]
closes = ["]",")","}",">"]
both = [
    L[i]
    for i in range(4)
    for L in [opens,closes]
]

points =  {
    ")" : 3,
    "]" : 57,
    "}" : 1197,
    ">" : 25137
}

score = 0
    
## Part 1
for i,line in enumerate(lines):
    
    _type_,line = get_type(line,opens,closes)
    # print(i,_type_)
    
    if _type_ == "corrupted":
        
        ## Find index of first close
        min_idx = min(
            [
                line.index(c)
                for c in closes
                if c in line
            ]
        )
        oL = line[min_idx]
        ## Get value of letter before it
        eL = line[min_idx-1]
        hL = closes[opens.index(eL)]
        
        # print(f"Expected {hL} but found {oL} instead")
        score += points[oL]
    
print(score)
    
    
## Part 2

def calc_score(S):
    points =  {
        ")" : 1,
        "]" : 2,
        "}" : 3,
        ">" : 4
    }
    score = 0
    for s in S:
        score *= 5
        score += points[s]
    return score
scores_list = []
rev_dict = dict(zip(opens,closes))

for i, line in enumerate(lines):
    
    _type_,line = get_type(line,opens,closes)
    
    if _type_ == "incomplete":
        print(line)
        S = ""
        for c in reversed(line):
            S += rev_dict[c]
        scores_list.append(calc_score(S))
    
sorted_scores = sorted(scores_list)
middle_idx = int((len(scores_list) + 1) / 2) - 1
print(sorted_scores[middle_idx])