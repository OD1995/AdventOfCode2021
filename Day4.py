import requests

input_url = "https://adventofcode.com/2021/day/4/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)

class BingoBoards:
    def __init__(
        self,
        input_req_text
    ):
        self.boards = {}
        for i,board_text in enumerate(input_req_text.split("\n\n")[1:]):
            self.boards[i] = BingoBoard(i,board_text)
        self.not_won_yet = list(self.boards.keys())

    def cross_off_number(
        self,
        num
    ):
        for board in self.boards.values():
            board.cross_off_number(num)

    def check_for_winners(self):
        for board in self.boards.values():
            if board.check_if_won():
                return board
        return False

    def check_for_last_winner(
        self,
        dn
    ):
        winner_count = 0
        for board_i in self.not_won_yet:
            board = self.boards[board_i]
            if board.check_if_won():
                self.not_won_yet.remove(board_i)
                last_winner = board
        if len(self.not_won_yet) == 0:
            return last_winner
        return False

class BingoBoard:
    def __init__(
        self,
        i,
        board_text
    ):
        self.i = i
        self.rows = [
            [
                v
                for v in row.split(" ")
                if v != ""
            ]
            for row in board_text.split("\n")
        ]
        self.coords = {}
        for y in range(5):
            for x in range(5):
                self.coords[self.rows[y][x]] = [y,x]
        self.drawn = [
            [0]*5
            for i in range(5)
        ]
    
    def cross_off_number(
        self,
        num
    ):
        if num in self.coords:
            y,x = self.coords[num]
            self.drawn[y][x] = 1

    def check_if_won(self):
        return any(
            [
                self.check_if_won_horizontal(),
                self.check_if_won_vertical()
            ]
        )
    
    def check_if_won_horizontal(self):
        for y in range(5):
            if sum(self.drawn[y]) == 5:
                return True
        return False

    def check_if_won_vertical(self):
        for y in range(5):
            if sum(
                [
                    self.drawn[x][y]
                    for x in range(5)
                ]
            ) == 5:
                return True
        return False
    
    def get_score(self):
        score = 0
        for y in range(5):
            for x in range(5):
                if self.drawn[y][x] == 0:
                    score += int(self.rows[y][x])
        return score


IRT = input_req.text
# IRT = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

# 22 13 17 11  0
#  8  2 23  4 24
# 21  9 14 16  7
#  6 10  3 18  5
#  1 12 20 15 19

#  3 15  0  2 22
#  9 18 13 17  5
# 19  8  7 25 23
# 20 11 10 24  4
# 14 21 16 12  6

# 14 21 17 24  4
# 10 16 15  9 19
# 18  8 23 26 20
# 22 11 13  6  5
#  2  0 12  3  7"""

drawn_numbers = IRT.split("\n\n")[0].split(",")

## Part 1
bb = BingoBoards(IRT)

for dn in drawn_numbers:
    bb.cross_off_number(dn)
    winner = bb.check_for_winners()
    if winner:
        break
print(winner.get_score()*int(dn))


## Part 2
bb2 = BingoBoards(IRT)

for dn in drawn_numbers:
    bb.cross_off_number(dn)
    last_winner = bb.check_for_last_winner(dn)
    if last_winner:
        break
print(last_winner.get_score()*int(dn))
a = 1