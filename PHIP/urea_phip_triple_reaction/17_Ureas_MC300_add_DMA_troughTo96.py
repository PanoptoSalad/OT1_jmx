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
reaction_conditions_df = read_csv(
    r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\urea_phip_triple_reaction\csv\reaction_conditions.csv")

# Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
source_trough12row = containers.load('trough-12row', "E2")
reaction_rack = containers.load("Starlab_96_Square_2mL", "C1")
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

def add_base_reagent(reaction_condition):

    id_header = "reaction"
    reaction_to_start = "Coupling_urea_sulpho"
    reagent_trough_location_header = "split 2 location solvent"
    volume_reagent_header = "split 2 volume solvent to add"
    rows_number_header = "split 2 number rows"

    for index, value in enumerate(reaction_conditions_df[id_header].tolist()):
        if value == reaction_to_start:
            volume_reagent = float(reaction_conditions_df[volume_reagent_header].tolist()[index])
            reagent_trough_location = reaction_conditions_df[reagent_trough_location_header].tolist()[index]
            number_rows = int(reaction_conditions_df[rows_number_header].tolist()[index])

    p300_multi.distribute(volume_reagent, source_trough12row.wells(reagent_trough_location),
                          [x.top() for x in reaction_rack.rows(0, to=number_rows-1)])
    robot.home()
add_base_reagent(reaction_conditions_df)