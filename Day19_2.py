from Day19 import I

class Scanner:

    def __init__(self,scannerID,beacon_list):
        self.scannerID = scannerID
        ## Direction relative to scanner 0
        ##    1 is same direction, -1 is opposite direction
        self.direction_ix = 0
        self.direction_final = True if scannerID == 0 else False
        self.direction_options = [
            [1,1,1],
            [1,-1,-1],
            [-1,1,-1],
            [-1,-1,1],
            [1,1,-1],
            [1,-1,1],
            [-1,1,1],
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
            if self.direction_ix == 7:
                self.next_change = 'dimension'
        else:
            result1 = self.change_direction()
            result2 = self.change_dimension()
            # print('dim change')
            self.next_change = 'direction'
            if not result2:
                raise ValueError('this should never happen')
    
    def change_direction(self):
        if self.direction_final or self.direction_ix == 7:
            if self.direction_ix == 7:
                self.direction_ix = 0
            return False
        else:
            self.direction_ix += 1
            return True

    def change_dimension(self):
        if self.dimension_final or self.dimension_ix == 5:
            if self.dimension_ix == 5:
                self.dimension_ix = 0
            return False
        else:
            self.dimension_ix += 1
            return True

    def get_coord_diffs(self):
        for i,x in enumerate(self.beacon_list):
            for j,y in enumerate(self.beacon_list):
                if j > i:
                    diff = [
                        (x[k] - y[k]) * self.direction_options[self.direction_ix][k]
                        # x[k] - (self.direction_options[self.direction_ix][k] * y[k])
                        for k in self.dimension_options[self.dimension_ix]
                    ]
                    if tuple(diff) not in self.coord_diffs:
                        self.coord_diffs[tuple(diff)] = [(i,j)]
                    else:
                        self.coord_diffs[tuple(diff)].append((i,j))

def get_coord_diff_matches(scanner,scanner0_cd):
    matches = []
    for i,x in enumerate(scanner.beacon_list):
        for j,y in enumerate(scanner.beacon_list):
            if j > i:
                # if (i==0)&(j==1)&(scanner.direction_ix==5):
                #     a=1
                diff = [
                    (x[k] - y[k]) * scanner.direction_options[scanner.direction_ix][k]
                    # x[k] - (scanner.direction_options[scanner.direction_ix][k] * y[k])
                    for k in scanner.dimension_options[scanner.dimension_ix]
                ]
                # if (1 in diff) or (-1 in diff):
                #     a=1
                #     print(diff)
                if tuple(diff) in scanner0_cd:
                    matches.append([(i,j),scanner0_cd[tuple(diff)]])
    return matches

def flatten(x):
    rm = []
    for sublist in x:
        for item in sublist:
            rm.append(item)
    return rm

def get_d_and_d(scanners,i,scanner0_cd):
    scanner = scanners[i]
    matches = []
    j = 1
    matchups = {}
    while len(matchups) == 0:
        # print(i,scanner.dimension_ix,scanner.direction_ix,scanner.next_change)
        matches = get_coord_diff_matches(scanner,scanner0_cd)
        j += 1
        matchups = {}
        for match in matches:
            for beacon_ix in match[0]:
                if beacon_ix not in matchups:
                    matchups[beacon_ix] = flatten(match[1])
                else:
                    matchups[beacon_ix].extend(flatten(match[1]))
        if len(matchups) == 0:
            scanner.change_d_or_d()
    # assert len(matchups) >= 12
    answers = {
        # k : max(set(v),key=v.count)
        # for k,v in matchups.items()
    }
    offsets = []
    dimensions = scanner.dimension_options[scanner.dimension_ix]
    directions = scanner.direction_options[scanner.direction_ix]
    for this_scanner_beacon_ix,scanner0_beacon_ix_list in matchups.items():
        most_common_scanner0_ix = max(
            set(scanner0_beacon_ix_list),
            key=scanner0_beacon_ix_list.count
        )
        answers[this_scanner_beacon_ix] = most_common_scanner0_ix
        sc0_beacon = scanners[0].beacon_list[most_common_scanner0_ix]
        sc_beacon = scanner.beacon_list[this_scanner_beacon_ix]
        offset = []
        for d in dimensions:
            # ofs = sc_beacon[d] - (directions[d] * sc0_beacon[d])
            ofs = sc0_beacon[d] - (directions[d] * sc_beacon[d])
            offset.append(ofs)
        offsets.append(tuple(offset))
    offsets_set = set(offsets)
    a=1
    assert len(offsets_set) == 1
    scanner.offset = offsets_set.pop()
    return scanner


scanners = {
    ik : Scanner(ik,iv)
    for ik,iv in I.items()
}

scanner0_cd = scanners[0].coord_diffs

for i in range(1,len(scanners)):
    try:
        scanner = get_d_and_d(scanners,i,scanner0_cd)
        scanners[i] = scanner
        print(i,'done')
    except ValueError:
        print(i,'not done')
a=1