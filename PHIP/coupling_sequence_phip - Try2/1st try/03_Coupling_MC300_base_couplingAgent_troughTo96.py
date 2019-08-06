"""Protocol that used the multichannel to add base and coupling agent to the desired number of rows in the plate."""

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
reaction_conditions_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\coupling_sequence_phip\csv\05-19_double\reaction_conditions.csv")
solvent_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\coupling_sequence_phip\csv\05-19_double\solvents.csv")

# Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
source_trough12row = containers.load('trough-12row', "E2")
reaction_rack = containers.load("StarLab_96_tall", "D1")
trash = containers.load("point", "C3")

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

def add_base_coupling(reaction_condition, solvent):
    cpd_id_heading = "CPD ID"
    base = "DIPEA"
    coupling = "T3P"
    location_heading = "Location_trough"
    reaction_heading = "reaction"
    volume_coupling_heading = "Volume to dispense Coupling agent"
    volume_base_heading = "Volume to dispense Base"
    number_rows_heading = "Number rows"
    for index, value in enumerate(solvent_df[cpd_id_heading].tolist()):
        if value == base:
            base_location = solvent_df[location_heading].tolist()[index]
        if value == coupling:
            coupling_location = solvent_df[location_heading].tolist()[index]
    for index, value in enumerate(reaction_conditions_df[reaction_heading].tolist()):
        if value == "Coupling_standard":
            base_volume = float(reaction_conditions_df[volume_base_heading].tolist()[index])
            coupling_volume = float(reaction_conditions_df[volume_coupling_heading].tolist()[index])
            number_rows = int(reaction_conditions_df[number_rows_heading].tolist()[index])
    print(base_location, type(base_location), base_volume, type(base_volume))
    p300_multi.distribute(base_volume, source_trough12row.wells(base_location),
                                  [x.top() for x in reaction_rack.rows(0, to=number_rows)])
    p300_multi.distribute(coupling_volume, source_trough12row.wells(coupling_location),
                                  [x.top() for x in reaction_rack.rows(0, to=number_rows)])
    robot.home()

add_base_coupling(reaction_conditions_df, solvent_df)