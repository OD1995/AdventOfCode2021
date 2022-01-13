# from Day19 import I
import requests

input_url = "https://adventofcode.com/2021/day/19/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)
input_str = input_req.text
I = {}
for s in input_str.split("\n\n"):
    if s[0] == "\n":
        s = s[1:]
    lines = s.split("\n")
    key = int(lines[0].replace("--- scanner ","").replace(" ---",""))
    value = []
    for line in lines[1:]:
        if line != "":
            value.append(
                [
                    int(x)
                    for x in line.split(",")
                ]
            )
    I[key] = value


# with open(r"C:\Users\Oli\Documents\Python\AdventOfCode\answer.txt", 'r') as file:
#     data = file.read()
# ANSWERS = [
#     list(map(int, x.split(",")))
#     for x in data.split("\n")
# ]

class Scanner:

    def __init__(self,scannerID,beacon_list):
        self.scannerID = scannerID
        ## Direction relative to scanner 0
        ##    1 is same direction, -1 is opposite direction
        self.direction_ix = 0
        self.direction_final = True if scannerID == 0 else False
        self.direction_options = [
            [1,1,1],
            [-1,1,1],
            [1,-1,-1],
            [-1,1,-1],
            [-1,-1,1],
            [1,1,-1],
            [1,-1,1],
            [-1,-1,-1],
        ]
        ## Dimension relative to scanner 0
        ##    [0,1,2] -> same dimensions as scanner 0
        ##    [2,1,0] -> x & z dimensions swapped comapred to scanner 0
        self.dimension_ix = 0
        self.dimension_final = True if scannerID == 0 else False
        self.dimension_options = [
            [0,1,2],
            [0,2,1],
            [1,0,2],
            [1,2,0],
            [2,0,1],
            [2,1,0]
        ]
        self.beacon_list = beacon_list
        self.coord_diffs = {}
        self.cd_final = True if scannerID == 0 else False
        self.next_change = 'direction'
        ## Offset from scanner 0
        self.offset = [0,0,0]
        self.done = True if scannerID == 0 else False
        if scannerID == 0:
            self.get_coord_diffs()

    def change_d_or_d(self):
        if self.next_change == 'direction':
            result1 = self.change_direction()
            # print('dir change')
            if not result1:
                # print('fail')
                result2 = self.change_dimension()
                # print('dim change')
                self.next_change = 'direction'
                if not result2:
                    raise ValueError('this should never happen')
            if self.direction_ix == len(self.direction_options) - 1:
                self.next_change = 'dimension'
        else:
            result1 = self.change_direction()
            result2 = self.change_dimension()
            # print('dim change')
            self.next_change = 'direction'
            if not result2:
                raise ValueError('this should never happen')
    
    def change_direction(self):
        if self.direction_final or (self.direction_ix == len(self.direction_options) - 1):
            if self.direction_ix == len(self.direction_options) - 1:
                self.direction_ix = 0
            return False
        else:
            self.direction_ix += 1
            return True

    def change_dimension(self):
        if self.dimension_final or (self.dimension_ix == len(self.dimension_options) - 1):
            if self.dimension_ix == len(self.dimension_options) - 1:
                self.dimension_ix = 0
            return False
        else:
            self.dimension_ix += 1
            return True

    def get_coord_diffs(self):
        for i,x in enumerate(self.beacon_list):
            for j,y in enumerate(self.beacon_list):
                if j != i:
                    diff = [
                        (x[k] - y[k]) * self.get_direction(k)
                        # x[k] - (self.direction_options[self.direction_ix][k] * y[k])
                        for k in self.get_dimension()
                    ]
                    if tuple(diff) not in self.coord_diffs:
                        self.coord_diffs[tuple(diff)] = [(i,j)]
                    else:
                        self.coord_diffs[tuple(diff)].append((i,j))
    
    def get_dimension(self,ix=None):
        if ix is None:
            return self.dimension_options[self.dimension_ix]
        else:
            return self.dimension_options[self.dimension_ix][ix]

    def get_direction(self,ix=None):
        if ix is None:
            return self.direction_options[self.direction_ix]
        else:
            return self.direction_options[self.direction_ix][ix]
    
    def set_offset(self,new_offset):
        self.offset = new_offset
        self.done = True
        self.get_coord_diffs()

    def reset_ixs(self):
        self.dimension_ix = 0
        self.direction_ix = 0

    def add_beacons(self,scanner):#,ANSWERS):
        dimensions = scanner.get_dimension()
        # directions = scanner.get_direction()
        for b in scanner.beacon_list:
            nb = []
            for ix in range(3):
                # dim = dimensions.index(ix)
                dim = scanner.get_dimension(ix)
                dir = scanner.get_direction(dim)
                # val = (b[dim] * dir) + scanner.offset[dim]
                # val = (b[dim] - scanner.offset[ix]) * dir
                val = (b[dim] * dir) + scanner.offset[ix]
                nb.append(val)
            if nb not in self.beacon_list:
                self.beacon_list.append(nb)
                # if nb in ANSWERS:
                #     self.beacon_list.append(nb)
                # else:
                #     a=1
        self.get_coord_diffs()

def get_coord_diff_matches(scanner,scanner0_cd):
    matches = []
    for i,x in enumerate(scanner.beacon_list):
        for j,y in enumerate(scanner.beacon_list):
            if j != i:
                # if (i==5)&(j==16)&(scanner.direction_ix==1)&(scanner.dimension_ix==3)&(scanner.scannerID==4):
                #     a=1
                diff = []
                for k in scanner.get_dimension():
                    val = (x[k] - y[k]) * scanner.get_direction(k)
                    diff.append(val)
                if tuple(diff) in scanner0_cd:
                    matches.append([(i,j),scanner0_cd[tuple(diff)]])
    return matches

def flatten(x):
    rm = []
    for sublist in x:
        for item in sublist:
            rm.append(item)
    return rm

def get_d_and_d(scanners,i,scanner0_cd,base_scanner_ix):
    scanner = scanners[i]
    scanner.reset_ixs()
    matches = []
    j = 1
    matchups = {}
    if i == 4:
        a=1
    while True:
        # print(i,scanner.dimension_ix,scanner.direction_ix,scanner.next_change)
        matches = get_coord_diff_matches(scanner,scanner0_cd)
        if len(matches) == 0:
            scanner.change_d_or_d()
            continue
        j += 1
        matchups = {}
        for match in matches:
            for beacon_ix in match[0]:
                if beacon_ix not in matchups:
                    matchups[beacon_ix] = flatten(match[1])
                else:
                    matchups[beacon_ix].extend(flatten(match[1]))
        if len(matchups) < 12:
            scanner.change_d_or_d()
            continue
        # assert len(matchups) >= 12
        answers = {
            # k : max(set(v),key=v.count)
            # for k,v in matchups.items()
        }
        offsets = []
        dimensions = scanner.get_dimension()
        directions = scanner.get_direction()
        A=[]
        B=[]
        for this_scanner_beacon_ix,scanner0_beacon_ix_list in matchups.items():
            most_common_scanner0_ix = max(
                set(scanner0_beacon_ix_list),
                key=scanner0_beacon_ix_list.count
            )
            answers[this_scanner_beacon_ix] = most_common_scanner0_ix
            sc0_beacon = scanners[0].beacon_list[most_common_scanner0_ix]
            A.append(sc0_beacon)
            sc_beacon = scanner.beacon_list[this_scanner_beacon_ix]
            B.append(sc_beacon)
            offset = []
            for ixx,(d0,d1) in enumerate(zip(scanners[0].get_dimension(),dimensions)):
                # ofs = sc_beacon[d] - (directions[d] * sc0_beacon[d])
                # ofs = sc0_beacon[d0] + (directions[d0] * sc_beacon[d1])
                iyy = scanner.get_dimension(ixx)
                ofs = sc0_beacon[d0] - (scanner.get_direction(iyy) * sc_beacon[d1])
                # if directions[d1] == -1:
                #     ofs = sc0_beacon[d0] + sc_beacon[d1]
                # elif directions[d1] == 1:
                #     ofs = sc0_beacon[d0] - sc_beacon[d1]
                offset.append(ofs)
            offsets.append(tuple(offset))
        offsets_set = set(offsets)
        # if i in [2,4]:
        #     a=1
        if len(offsets_set) != 1:
            scanner.change_d_or_d()
            continue
        scanner_offset = [
            x+y
            for x,y in zip(scanners[base_scanner_ix].offset,offsets_set.pop())
        ]
        scanner.set_offset(scanner_offset)
        return scanner
    raise ValueError('nope, this didn''t work')


scanners = {
    ik : Scanner(ik,iv)
    for ik,iv in I.items()
}

# for base_scanner_ix in range(len(scanners)-1):
#     base_scanner = scanners[base_scanner_ix]
#     if not base_scanner.done:
#         continue

#     scanner0_cd = base_scanner.coord_diffs

#     for i in range(base_scanner_ix+1,len(scanners)):
#         if scanners[i].done:
#             continue
#         try:
#             scanner = get_d_and_d(scanners,i,scanner0_cd,base_scanner_ix)
#             scanners[i] = scanner
#             print(base_scanner_ix,'->',i,'done')
#         except ValueError:
#             print(base_scanner_ix,'->',i,'not done')
def do_it(scanners):#,ANSWERS):
    base_scanner_ix = 0
    for i in range(1,len(scanners)):
        base_scanner = scanners[base_scanner_ix]
        scanner0_cd = base_scanner.coord_diffs
        if scanners[i].done:
            continue
        try:
            scanner = get_d_and_d(scanners,i,scanner0_cd,base_scanner_ix)
            scanners[i] = scanner
            scanners[base_scanner_ix].add_beacons(scanner)#,ANSWERS)
            print(base_scanner_ix,'->',i,'done')
            print(len(scanners[base_scanner_ix].beacon_list))
        except ValueError:
            print(base_scanner_ix,'->',i,'not done')
    return scanners
not_all_done = True
ct = 0
while not_all_done:
    scanners = do_it(scanners)#,ANSWERS)
    not_all_done = all(
        [
            x.done
            for x in scanners.values()
        ]
    ) == False
    ct += 1
    # if ct > 5:
    #     break
a=1

def measure_distance(sc1,sc2):
    rm = 0
    for o1,o2 in zip(sc1.offset,sc2.offset):
        rm += abs(o1 - o2)
    return rm
## 12370 is too low
max_dist = 0
for i,sc1 in scanners.items():
    for j,sc2 in scanners.items():
        if j > i:
            dist = measure_distance(sc1,sc2)
            max_dist = max(dist,max_dist)
print('dist:',max_dist)