import random
import string
import requests

input_url = "https://adventofcode.com/2021/day/16/input"
session_id = "53616c7465645f5f64fad645943322b17c0e835504cd0c16c1d75b618f8a779116374784d0374c261cf68fabbb5e30ec"

input_req = requests.get(
    url=input_url,
    cookies={"session":session_id}
)

input_str = """
0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
A = 1010
B = 1011
C = 1100
D = 1101
E = 1110
F = 1111
"""

lookup = {
    x.split(" = ")[0] : x.split(" = ")[1]
    for x in input_str.split("\n")
    if x.strip() != ""
}

def get_binary_from_message(M,lookup):
    rm = ""
    for e in M:
        rm += lookup[e]
    return rm

class PacketManager:
    def __init__(self,message,lookup):
        self.message = message
        self.lookup = lookup
        self.pz = 0
        self.packet_list = []
        self.packet_str = self.get_binary_from_message()
        self.initial_packet = Packet(self,self.packet_str)
        # self.packet_list.append(self.initial_packet)
        self.add_packet_to_packet_list(self.initial_packet)
    
    def get_binary_from_message(self):
        rm = ""
        for e in self.message:
            rm += self.lookup[e]
        return rm

    def add_packet_to_packet_list(self,packet):
        # self.packet_list.append(packet)
        # if packet.key not in self.packet_list:
        # self.packet_list[packet.key] = packet
        self.packet_list.append(packet)

    def increment_pz(self,PZ):
        self.pz += PZ

    def get_packet_versions(self):
        return [x.packet_version for x in self.packet_list]

    # def get_pl_keys(self):
    #     return self.packet_list.keys()

    def print_info(self):
        for k,v in self.packet_list:
            print(v.packet_version,k)

    def analyse_packet_list(self):
        ## Get longest key
        PL = [
            x.key2.split("&")[0]
            for x in self.packet_list
        ]
        # assert len(PL) == len(set(PL))
        parent_list = [
            x.split("-")
            for x in PL
        ]
        D = {
            tuple(k) : i
            for i,k in enumerate(parent_list)
        }
        for i,p in enumerate(parent_list):
            ## Get/set parent
            p_tree = p[:-1]
            p_obj = self.packet_list[i]
            # p_tree_len = len(p_tree)
            if len(p) > 1:
                possible_parents = [
                    x
                    for x in parent_list
                    if p_tree == x
                ]
                assert len(possible_parents) == 1
                p_obj.set_parent(self.packet_list[D[tuple(possible_parents[0])]])
            ## Get/set children
            possible_children = [
                x
                for x in parent_list
                if (len(x) > len(p)) & (x[:-1] == p)
            ]
            for c in possible_children:
                p_obj.add_child(self.packet_list[D[tuple(c)]])
            
            self.packet_list[D[tuple(p)]].set_generation(len(p))

        a = 1

        sorted_by_generation = sorted(
            [
                (i,x.generation)
                for i,x in enumerate(self.packet_list)
            ],
            key=lambda x: x[1],
            reverse=True
        )

        for i,x in sorted_by_generation:
            packet = self.packet_list[i]
            children_vals = [
                x.literal_value
                for x in packet.children
            ]
            assert None not in children_vals
            if packet.packet_type_id == 4:
                pass
            else:
                if packet.packet_type_id == 0:
                    v = sum(children_vals)
                elif packet.packet_type_id == 1:
                    v = 1
                    for cv in children_vals:
                        v *= cv
                elif packet.packet_type_id == 2:
                    v = min(children_vals)
                elif packet.packet_type_id == 3:
                    v = max(children_vals)
                elif packet.packet_type_id == 5:
                    assert len(children_vals) == 2
                    v = 1 if children_vals[0] > children_vals[1] else 0
                elif packet.packet_type_id == 6:
                    assert len(children_vals) == 2
                    v = 1 if children_vals[0] < children_vals[1] else 0
                elif packet.packet_type_id == 7:
                    assert len(children_vals) == 2
                    v = 1 if children_vals[0] == children_vals[1] else 0
                self.packet_list[i].set_literal_value(v)

        return self.packet_list[sorted_by_generation[-1][0]].literal_value

class Packet:
    def __init__(
        self,
        pm,
        packet_str,
        padded_zeros=0,
        packet_version=None,
        packet_type_id=None,
        length_type_id=None,
        literal_value=None,
        pvti="(N)",
        odID=None
    ):
        self.packet_manager = pm
        self.children = []
        self.parent = None
        self.padded_zeros = padded_zeros
        self.packet = packet_str
        self.pvti = pvti
        self.odID = odID
        self.literal_value = None
        self.is_valid = True
        self.generation = None
        are_sets = []
        for V in [
            packet_version,
            packet_type_id,
            # length_type_id,
        ]:
            are_sets.append(V is not None)
        if all(are_sets):
            self.packet_version = packet_version
            self.packet_type_id = packet_type_id
            self.length_type_id = length_type_id
            self.literal_value = literal_value
        else:
            self.parse_properly()
        self.key = f"{self.pvti}&{self.packet}"
        self.me = "({},{},{},{})".format(
                self.packet_version,
                self.packet_type_id,
                self.length_type_id if self.length_type_id is not None else "X",
                self.odID
        )
        self.key2 = self.me if self.pvti == "(N)" else f"{self.pvti}-{self.me}"

    def parse_properly(self):
        self.packet_version = self.get_num_from_binary(self.packet[:3])
        self.packet_type_id = self.get_num_from_binary(self.packet[3:6])
        self.odID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        if self.packet_type_id == 4:
            binary_list = self.get_binary_list()
            if binary_list == False:
                self.is_valid = False
            else:
                res = self.get_num_from_binary("".join(binary_list))
                if res == False:
                    self.is_valid = False
                else:
                    self.literal_value = res
        else:
            self.length_type_id = int(self.packet[6])
            if self.length_type_id == 0:
                self.subpackets_total_length = self.get_num_from_binary(self.packet[7:22])
                ps = PacketSplitter(self.packet_manager,self.packet[22:],length=self.subpackets_total_length)
            elif self.length_type_id == 1:
                self.subpacket_count = self.get_num_from_binary(self.packet[7:18])
                ps = PacketSplitter(self.packet_manager,self.packet[18:],count=self.subpacket_count)
            ## Parent packet's version, packet type ID, length type ID
            pvti = "({},{},{},{})".format(
                self.packet_version,
                self.packet_type_id,
                self.length_type_id,
                self.odID
            )
            self.subpackets_list = ps.split_into_packets(pvti)
            # for sp in self.subpackets_list:
            #     self.packet_manager.add_packet_to_packet_list(sp)
            # if overflow_str:
            #     overflow_packet = Packet(self.packet_manager,overflow_str)
            #     self.packet_manager.add_packet_to_packet_list(overflow_packet)
   
    @staticmethod
    def get_num_from_binary(S):
        rm = 0
        mag = 1
        for val in reversed(S):
            rm += mag * int(val)
            mag *= 2
        return rm

    def add_child(self,child):
        self.children.append(child)

    def set_parent(self,parent):
        self.parent = parent

    def set_generation(self,generation):
        self.generation = generation

    def set_literal_value(self,lv):
        assert self.literal_value is None
        self.literal_value = lv

    def get_binary_list(self):
        p = self.packet[6:]
        if p[-5:] == "00000":
            p = p[:-5]
        r = len(p) // 5
        bl = []
        for i in range(r):
            v = p[i*5:(i*5)+5]
            set_v = set(v[1:])
            all_zeros = set_v == set("0")
            if (
                    ((v[0] == "0") & (i != r - 1))
                    or
                    ((v[0] == "1") & all_zeros)
            ):
                return False
            elif not all_zeros:
                bl.append(v[1:])
        return bl



class PacketSplitter:
    def __init__(self,pm,string,length=None,count=None):
        self.packet_manager = pm
        self.string = string
        self.length = length
        self.count = count

    def split_into_packets(self,pvti):
        # if pvti == "(7,0,0)-(3,1,1)-(7,6,1)-(0,2,1)-(3,1,1)-(6,1,0)-(0,6,1)":
        #     a=1
        P = self.string
        if self.length is not None:
            if set(P[self.length:]) == set("0"):
                PZ = len(P[self.length:])
                self.packet_manager.increment_pz(PZ)
            P = P[:self.length]
        # else:
        #     PZ = 0
        P_len = len(P)
        packet_ixs = []
        packets_created_within = []
        packet_start = 0
        packet_end = 0
        add_on_extra = 0
        split_count = 0
        while True:
            split_count += 1
            if set(P[packet_start:]) == set("0"):
                break
            padded_zeros = 0
            add_ons = 0
            p_version = Packet.get_num_from_binary(P[packet_start:packet_start+3])
            p_type_id = Packet.get_num_from_binary(P[packet_start+3:packet_start+6])
            odID = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            packet_end += 6
            if p_type_id == 4:
                l_type_id = None
                len_values,binary_list,pz2 = self.get_binary_list_len(P[packet_start+6:])
                self.packet_manager.increment_pz(pz2)
                literal_value = Packet.get_num_from_binary("".join(binary_list))
                packet_end += len_values + pz2
                np = Packet(
                    pm=self.packet_manager,
                    packet_str=P[packet_start:packet_end],
                    packet_version=p_version,
                    packet_type_id=p_type_id,
                    length_type_id=l_type_id,
                    literal_value=literal_value,
                    pvti=pvti,
                    odID=odID
                )
                self.packet_manager.add_packet_to_packet_list(np)
                add_on_extra += len(np.packet)
            else:
                literal_value = None
                packet_end += 1
                l_type_id = P[packet_start+6]
                if l_type_id == "0":
                    subpackets_total_length = Packet.get_num_from_binary(P[packet_start+7:packet_start+22])
                    packet_end += 15
                    ps = PacketSplitter(self.packet_manager,P[packet_start+22:],length=subpackets_total_length)
                elif l_type_id == "1":
                    subpacket_count = Packet.get_num_from_binary(P[packet_start+7:packet_start+18])
                    packet_end += 11
                    ps = PacketSplitter(self.packet_manager,P[packet_start+18:],count=subpacket_count)
                pvti2 = pvti + "-" + "({},{},{},{})".format(
                    p_version,
                    p_type_id,
                    l_type_id,
                    odID
                )
                subpackets_list,add_on_extra = ps.split_into_packets(pvti2)
                packets_created_within.extend(subpackets_list)
                # add_ons = self.packet_manager.pz + add_on_extra
                packet_end += add_on_extra
                for sp in subpackets_list:
                    add_ons += len(sp.packet) # + max(PZ,sp.padded_zeros)
                packet_ixs.append((packet_start,packet_end,p_version,p_type_id,l_type_id,literal_value,odID))
            packet_start = packet_end
            # if packet_end + add_ons >= P_len:
            if packet_end + self.packet_manager.pz >= P_len:
                break
            if self.count is not None:
                if split_count >= self.count:
                    break
        # new_packets = [
        #     Packet(self.packet_manager,P[s:e],ptID,plID)#,max(PZ,pz))
        #     for s,e,pv,ptID,plID in packet_ixs
        # ]
        new_packets = []
        for s,e,pv,ptID,ltID,lv,o in packet_ixs:
            np = Packet(self.packet_manager,P[s:e],packet_version=pv,
                        packet_type_id=ptID,length_type_id=ltID,
                        literal_value=lv,pvti=pvti,odID=o)
            # new_packets.append(np)
            self.packet_manager.add_packet_to_packet_list(np)
        rm = new_packets + packets_created_within
        return rm,packet_end+add_ons

    def get_binary_list_len(self,p):
        # if p == '1110100000':
        #     a=1
        r = len(p) // 5
        last_began_with_zero = False
        chars_covered = 0
        # padded_zeros = 0
        bl = []
        for i in range(r):
            v = p[i*5:(i*5)+5]
            all_zeros = set(v) == set("0")
            if v[0] == "1":
                chars_covered += 5
                bl.append(v[1:])
            elif not all_zeros:
                chars_covered += 5
                bl.append(v[1:])
                break
            elif last_began_with_zero & all_zeros:
                chars_covered += len(v)
                # padded_zeros += len(v)
                break
            if set(v) == set("0"):
                if len(v) == 5:
                    chars_covered += len(v)
                    bl.append(v[1:])
                    break
                else:
                    raise ValueError('this shouldnt happen')
        remaining_str = p[(i*5)+5:]
        if set(remaining_str) == set("0"):
            padded_zeros = len(remaining_str)
        else:
            padded_zeros = 0
        return chars_covered,bl,padded_zeros

# tests = [
#     ('C200B40A82',3),
#     ('04005AC33890',54),
#     ('880086C3E88112',7),
#     ('CE00C43D881120',9),
#     ('D8005AC2A8F0',1),
#     ('F600BC2D8F',0),
#     ('9C005AC2F8F0',0),
#     ('9C0141080250320F1802104A08',1)
#     # ('8A004A801A8002F478',0)
# ]

# for M,N in tests:
#     PM = PacketManager(message=M,lookup=lookup)
#     answer = PM.analyse_packet_list()
#     print(M,N==answer)
#     a = 1

_input_ = input_req.text.strip()

# M = [
#     x.strip()
#     for x in _input_.split("\n")
# ]

# T = 0

PM = PacketManager(message=_input_,lookup=lookup)
answer = PM.analyse_packet_list()
print(answer)