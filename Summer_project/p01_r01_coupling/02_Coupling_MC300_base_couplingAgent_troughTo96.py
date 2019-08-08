"""Protocol that uses the multichannel to add base and coupling agent to the desired number of rows in the plate."""

from opentrons import robot, containers, instruments
robot.head_speed(x=16000, y=16000, z=3000, a=400, b=400)

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

reaction_df = read_csv(r"C:\Users\sdi35357\CODING\github_repo\OT1-coding\Summer_project\csv\p01_r01\reaction_conditions.csv")

# Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
source_trough12row = containers.load('trough-12row', "E2")
reaction_rack = containers.load("StarLab_96_tall", "D1")
trash = containers.load("point", "B3")

# Pipettes SetUp
p300_multi = instruments.Pipette(
    name='dlab_300multi',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300],
    max_volume=300,
    min_volume=30,
    channels=8,
)

def add_base_and_couplingAgent(reaction_condition):
    id_header = "Reaction parameters type"
    details_header = "Reaction details"
    base = "Reagent 1"
    coupling = "Reagent 2"
    location_heading = "Location_trough"
    volume_to_add = "Volume to add (uL)"
    number_of_columns = "Number columns"
    
    
    for index, value in enumerate(reaction_df[id_header].tolist()):
        if value == base:
            base_location = reaction_df[location_heading].tolist()[index]
            base_volume = float(reaction_df[volume_to_add].tolist()[index])
        if value == coupling:
            coupling_location = reaction_df[location_heading].tolist()[index]
            coupling_volume = float(reaction_df[volume_to_add].tolist()[index])
        if value == number_of_columns:
            #number_cols = float(reaction_df[details_header].tolist()[index])
            number_cols = reaction_df[details_header].tolist()[index]

            

    #print(base_location, type(base_location), base_volume, type(base_volume), number_cols, type(number_cols))


    p300_multi.distribute(base_volume, source_trough12row.wells(base_location),
                                  [x.top() for x in reaction_rack.rows(0, to=number_cols)], air_gap=10)
    p300_multi.distribute(coupling_volume, source_trough12row.wells(coupling_location),
                                  [x.top() for x in reaction_rack.rows(0, to=number_cols)], air_gap=10)
    robot.home()

add_base_and_couplingAgent(reaction_df)