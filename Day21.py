import requests

input_url = "https://adventofcode.com/2021/day/21/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)

input_str = """
Player 1 starting position: 4
Player 2 starting position: 8
"""

input_str = input_req.text

pos1,pos2 = [
    int(x.split(": ")[1])
    for x in input_str.split("\n")
    if x != ""
]


## Part 1
def play1(pos1,pos2):
    score1 = score2 = 0
    roll_count = 0
    last_roll = 0
    turn = 0
    while True:
        # if turn == 15:
        #     b=1
        # c=1
        ## Player 1 turn
        rolls1 = []
        for a in range(1,4):
            v1 = (last_roll + a) % 100
            if v1 == 0:
                v1 = 100
            rolls1.append(v1)
        roll_count += 3
        last_roll = rolls1[-1]
        pos1 = (pos1 + sum(rolls1)) % 10
        if pos1 == 0:
            pos1 = 10
        score1 += pos1
        if score1 >= 1000:
            return roll_count,score2
        ## Player 2 turn
        rolls2 = []
        for a in range(1,4):
            v2 = (last_roll + a) % 100
            if v2 == 0:
                v2 = 100
            rolls2.append(v2)
        
        roll_count += 3
        last_roll = rolls2[-1]
        pos2 = (pos2 + sum(rolls2)) % 10
        if pos2 == 0:
            pos2 = 10
        score2 += pos2
        if score2 >= 1000:
            return roll_count,score1
        turn += 1
        # print(turn,score1,score2)

roll_count,loser_score = play1(pos1,pos2)
print(roll_count * loser_score)

## Part 2
## pos,score,ways_to_get_there
routes = {
    1 : {
            0 : [(pos1,0,1)]
    },
    2 : {
            0 : [(pos2,0,1)]
    }
}

winners = {
    1 : {},
    2 : {}
}
not_winners = {
    1 : {},
    2 : {}
}

possible_results = {
    3 : 1,
    4 : 3,
    5 : 6,
    6 : 7,
    7 : 6,
    8 : 3,
    9 : 1
}
D = {}
for pos_on_board in range(1,11):
    for pos_total,pos_ct in possible_results.items():
        new_pos = (pos_on_board + pos_total) % 10
        if new_pos == 0:
            new_pos = 10
        if pos_on_board not in D:
            D[pos_on_board] = {}
        D[pos_on_board][pos_total] = (new_pos,pos_ct)

## Get all possible ways for Player 1 to get to at least 21 points
max_turn = 1
player = 1
for player in [1,2]:
    turn = 1
    while True:
        ## Get all routes to get to previous turn
        last_turn_routes = routes[player][turn-1]
        if len(last_turn_routes) == 0:
            break
        new_routes_list = []
        for ltr in last_turn_routes:
            pos,score,ways_to_get_there = ltr
            if score < 21:
                for roll_total,(new_pos,multiplier) in D[pos].items():
                    new_routes_list.append((new_pos,score+new_pos,ways_to_get_there*multiplier))
                if (turn - 1) not in not_winners[player]:
                    not_winners[player][turn-1] = []
                not_winners[player][turn-1].append(ways_to_get_there)
            else:
                if (turn - 1) not in winners[player]:
                    winners[player][turn-1] = []
                winners[player][turn-1].append(ways_to_get_there)
        if len(new_routes_list) == 0:
            break
        routes[player][turn] = new_routes_list
        max_turn = max(max_turn,turn)
        turn += 1
    
win_count = {
    1 : 0,
    2 : 0
}
other_one = {
    1 : 2,
    2 : 1
}
for t in range(3,max_turn+1):
    ## Player 1 wins
    multi_sum1 = sum(winners[1][t])
    loser2_from_prev_turn = sum(
        [
            x[2]
            for x in routes[2][t-1]
            if x[1] < 21
        ]
    )
    win_count[1] += multi_sum1 * loser2_from_prev_turn
    ## Player 2 wins
    multi_sum2 = sum(winners[2][t])
    loser1_from_this_turn = sum(
        [
            x[2]
            for x in routes[1][t]
            if x[1] < 21
        ]
    )
    win_count[2] += multi_sum2 * loser1_from_this_turn

# print(win_count)
print(max(win_count.values()))