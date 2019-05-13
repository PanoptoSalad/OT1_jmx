'''OT1 -Single channel- Making up of main reagent stock solution (2 maximum) using a defined solvent'''

from opentrons import robot, containers, instruments

robot.head_speed(x=21000, y=21000, z=5000, a=700, b=700)


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


# Function that reads a csv file correctly without having to import anything (issues with molport). Uses 2 classes, Vector and DataFrame
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


# CSV file data
reaction_conditions_df = read_csv(
    r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\coupling_sequence_phip - Try2\csv\reaction_conditions.csv")
reactant_df = read_csv(
    r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\coupling_sequence_phip - Try2\csv\main_reactant.csv")
# solvent_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\coupling_phip\csv\05-19_rd2\solvents.csv")

"""Function that does one liquid handling transfers. Dilute a solid reagent in a big trough to the right concentration.
It requires 1 csv files, the custom made stock reagent csv."""


def stock_solution_main(reaction_conditions, reactants):
    # Deck setup
    tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
    source_trough4row = containers.load("trough-12row", "C2")
    trash = containers.load("point", "C3")
    # Pipettes SetUp
    p1000 = instruments.Pipette(
        name='eppendorf1000',
        axis='b',
        trash_container=trash,
        tip_racks=[tiprack_1000],
        max_volume=1000,
        min_volume=30,
        channels=1,
    )

    id_header = "reaction"
    reaction_to_start = "Coupling_sequence"
    solvent_trough_location_header = "main reactant solvent Location"
    volume_stock_header = "main reactant volume to add - stock (uL)"
    destination_header = "main reactant location"
    additional_base_header = "Additional solvent to add (uL)"
    additional_base_location_header = "additional solvent location"

    for index, value in enumerate(reaction_conditions_df[id_header].tolist()):
        if value == reaction_to_start:
            solvent_location = reaction_conditions_df[solvent_trough_location_header].tolist()[index]
            solvent_volume = reaction_conditions_df[volume_stock_header].tolist()[index]
            destination_location = reaction_conditions_df[destination_header].tolist()[index]
            base_to_add = reaction_conditions_df[additional_base_header].tolist()[index]
            base_location = reaction_conditions_df[additional_base_location_header].tolist()[index]

    p1000.pick_up_tip()
    p1000.transfer([solvent_volume], source_trough4row.wells(solvent_location),
                   source_trough4row.wells(destination_location).top(-5), new_tip='never')
    p1000.drop_tip()
    p1000.pick_up_tip()
    p1000.transfer([base_to_add], source_trough4row.wells(base_location),
                   source_trough4row.wells(destination_location).top(-5), new_tip='never')
    p1000.drop_tip()
    robot.home()


stock_solution_main(reaction_conditions_df, reactant_df)
