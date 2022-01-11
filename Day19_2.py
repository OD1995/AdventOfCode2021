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

        if scannerID == 0:
            self.get_coord_diffs()

    def change_d_or_d(self):
        if self.next_change == 'direction':
            result1 = self.change_direction()
            print('dir change')
            if not result1:
                # print('fail')
                result2 = self.change_dimension()
                print('dim change')
                self.next_change = 'direction'
                if not result2:
                    raise ValueError('this should never happen')
            if self.direction_ix == 7:
                self.next_change = 'dimension'
        else:
            result1 = self.change_direction()
            result2 = self.change_dimension()
            print('dim change')
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
                if j != i:
                    diff = [
                        x[k] + (self.direction_options[self.direction_ix][k] * y[k])
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
            if j != i:
                diff = [
                    x[k] + (scanner.direction_options[scanner.direction_ix][k] * y[k])
                    for k in scanner.dimension_options[scanner.dimension_ix]
                ]
                if tuple(diff) in scanner0_cd:
                    matches.append([(i,j),scanner0_cd[tuple(diff)]])
    return matches

def get_d_and_d(scanners,i,scanner0_cd):
    scanner = scanners[i]
    matches = []
    i = 1
    while len(matches) == 0:
        print(i,scanner.dimension_ix,scanner.direction_ix,scanner.next_change)
        matches = get_coord_diff_matches(scanner,scanner0_cd)
        scanner.change_d_or_d()
        i += 1
    a=1


scanners = {
    ik : Scanner(ik,iv)
    for ik,iv in I.items()
}

scanner0_cd = scanners[0].coord_diffs

for i in range(1,len(scanners)):
    direction_ix,dimension_ix = get_d_and_d(scanners,i,scanner0_cd)
