import math
import requests

input_url = "https://adventofcode.com/2021/day/14/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)

input_str = """
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""
input_str = input_req.text

def normal_round(n, decimals=0):
    expoN = n * 10 ** decimals
    if abs(expoN) - abs(math.floor(expoN)) < 0.5:
        return math.floor(expoN) / 10 ** decimals
    return int(math.ceil(expoN) / 10 ** decimals)

def create_converter(input_str):
    converter = {}
    for line in input_str.split("\n\n")[1].split("\n"):
        if line.strip() != "":
            i,o = line.split(" -> ")
            converter[i] = [i[0]+o,o+i[1]]
    return converter

def create_initial_pair_count(input_str,converter,_input_=None):
    if _input_ is None:
        _input_ = input_str.split("\n\n")[0].strip()
    pairs = [
        _input_[i-1:i+1]
        for i in range(1,len(_input_))
    ]
    pair_count = {
        x : 0
        for x in converter.keys()
    }
    for p in pairs:
        pair_count[p] += 1
    return pair_count


def convert_pair_count(pair_count,converter):
    new_pair_count = {
        x : 0
        for x in converter.keys()
    }
    for p,ct in pair_count.items():
        for op in converter[p]:
            new_pair_count[op] += ct
    return new_pair_count

def count_letters(pair_count):
    initial_letter_count = {}
    for p,ct in pair_count.items():
        for L in p:
            if L in initial_letter_count:
                initial_letter_count[L] += ct
            else:
                initial_letter_count[L] = ct
    letter_count = {}
    for k,v in initial_letter_count.items():
        letter_count[k] = normal_round(v/2)
    return letter_count

converter = create_converter(input_str)
pair_count = create_initial_pair_count(input_str,converter)
for i in range(40):
    pair_count = convert_pair_count(pair_count,converter)
letter_count = count_letters(pair_count)
print(int(max(letter_count.values()) - min(letter_count.values())))