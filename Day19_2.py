from Day19 import input_str

class Scanner:

    def __init__(self,scannerID,beacon_list):
        self.scannerID = scannerID
        self.direction = [1,1,1]
        self.direction_final = True if scannerID == 0 else False
        self.dimension = [0,1,2]
        self.dimension_final = True if scannerID == 0 else False
        self.beacon_list = beacon_list
    
    def set_direction(self,new_direction):
        if self.dimension_final:
            raise ValueError('`direction` is already final')
        self.direction = new_direction
