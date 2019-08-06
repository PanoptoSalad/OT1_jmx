"""Protocol that used the multichannel to add base and coupling agent to the desired number of rows in the plate."""

from opentrons import robot, containers, instruments
robot.head_speed(x=20000, y=20000, z=3000, a=400, b=400)

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
#Function that reads a csv file correctly without having to import anything (issues with molport). Uses 2 classes, Vector and DataFrame
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
#CSV file data
reaction_conditions_df = read_csv(
    r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\coupling_sequence_phip - Try2\csv\forMeIAddition\reaction_conditions.csv")

# Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
tiprack_300_2 = containers.load("tiprack-300ul", "B1")
tiprack_300_3 = containers.load("tiprack-300ul", "A1")

source_trough12row = containers.load('trough-12row', "E2")
reaction_rack = containers.load("StarLab_96_tall", "D1")
destination_rack1 = containers.load("StarLab_96_tall", "D2")
destination_rack2 = containers.load("StarLab_96_tall", "B1")
destination_rack3 = containers.load("StarLab_96_tall", "B2")

trash = containers.load("point", "C3")


#Pipettes SetUp
p300_multi  = instruments.Pipette(
    name='dlab_300multi_no_min',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300,tiprack_300_2,tiprack_300_3],
    max_volume=300,
    min_volume=0,
    channels=8,
)

def add_base_reagent(reaction_condition):

    id_header = "reaction"
    reaction_to_start = "Coupling_sequence"
    split_volume_header = "split volume to take out per reaction"
    number_rows_header = "Number rows"

    for index, value in enumerate(reaction_conditions_df[id_header].tolist()):
        if value == reaction_to_start:
            volume_per_reaction = float(reaction_conditions_df[split_volume_header].tolist()[index])
            number_rows = int(reaction_conditions_df[number_rows_header].tolist()[index])

    #source_location1 = [well.bottom(4) for well in reaction_rack.rows(0, to=number_rows-1)]

    #source_location2 = [reaction_rack.rows(1).bottom(2)]
    #source_location3 = [reaction_rack.rows(2).bottom(2)]

            for i in range (0, 9):
                #p300_multi.pick_up_tip()
                source_location = reaction_rack.rows(i).bottom(5)
                destination_1 = destination_rack1.rows(i).top()
                #destination_2 = destination_rack2.rows(i).top()
                #destination_3 = destination_rack3.rows(i).top()
                p300_multi.distribute(volume_per_reaction, source_location,destination_1, air_gap=10,blow_out= True)
                #p300_multi.distribute(volume_per_reaction, source_location,destination_2, air_gap=10, new_tip='never')
                #p300_multi.distribute(volume_per_reaction, source_location,destination_3, air_gap=10, new_tip='never')
                #p300_multi.drop_tip()



            #p300_multi.distribute(volume_per_reaction, source_location,destination_2, air_gap=10,change_tip = "never")
        #p300_multi.distribute(volume_per_reaction, source_location,destination_3, air_gap=10,change_tip = "never")

    robot.home()
add_base_reagent(reaction_conditions_df)