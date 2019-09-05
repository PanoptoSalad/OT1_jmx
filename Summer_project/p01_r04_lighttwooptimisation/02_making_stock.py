class Vector(object):
    def tolist(self):
        return list(self.input_list)

    def astype(self, input_type):
        if input_type == int:
            return Vector([int(float(x)) for x in self.input_list])
        return Vector([input_type(x) for x in self.input_list])

    def __init__(self, input_list):
        self.input_list = input_list


class DataFrame(object):
    def __len__(self):
        return self.length

    def __getitem__(self, value):
        return Vector(self.dict_input[value])

    def __init__(self, dict_input, length):
        self.dict_input = dict_input
        self.length = length


# Function that reads a csv file correctly without having to <span class="girk">import anything. Us</span>es 2 classes, Vector and DataFrame
def read_csv(input_file):
    lines = open(input_file).readlines()
    header = lines[0].rstrip().split(",")
    out_d = {}
    for head in header:
        out_d[head] = []
    for line in lines[1:]:
        spl_line = line.rstrip().split(",")
        for i, head in enumerate(header):
            out_d[head].append(spl_line[i])
    df = DataFrame(out_d, len(lines[1:]))
    return df

stock_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\Summer_project\p01_r04_lighttwooptimisation\csv\250819_JMX_Base_evaluation\Stock.csv")

from opentrons import robot, containers, instruments

tiprack_1000 = containers.load("tiprack-1000ul-H", "D3")
source_trough4row = containers.load("trough-12row", "B2")
rack_beforemix = containers.load("FluidX_24_5ml_jmx", "A1")
rack_aftermix = containers.load("jMX_big_vial_holder", "B1")

robot.head_speed(x=18000, y=18000, z=5000, a=700, b=700)

trash = containers.load("point", "B3")

#Pipettes SetUp
p1000 = instruments.Pipette(
        name='eppendorf1000',
        axis='b',
        trash_container=trash,
        tip_racks=[tiprack_1000],
        max_volume=1000,
        min_volume=30,
        channels=1,
    )

location = 'Location'
volume = 'Volume to dispense (exp) at 0.8M'

vol_total = 0
for i in stock_df[volume].tolist():
    vol_total += float(i)
number_iterations = vol_total // 22000

if number_iterations < 1:
    for index, value in enumerate(stock_df[location].tolist()):
        p1000.pick_up_tip()
        vol = float(stock_df[volume].tolist()[index])
        p1000.transfer(vol, rack_beforemix(value), rack_aftermix.wells('A1'), new_tip='always', air_gap=10)
        #p1000.drop_tip()

if number_iterations >= 1:
    for index, value in enumerate(stock_df[location].tolist()):
        p1000.pick_up_tip()
        vol = float(stock_df[volume].tolist()[index])*22000/vol_total
        vol2 = float(stock_df[volume].tolist()[index]) * (vol_total - 22000) / vol_total
        p1000.distribute(vol, rack_beforemix(value), rack_aftermix.wells('A1'), air_gap=10)
        p1000.transfer(vol2, rack_beforemix(value), rack_aftermix.wells('A2'), air_gap=10)
        #p1000.drop_tip()

# improve this code with distribute + transfer in the future