"""This protocol transfers the main reactant onto the 96 reaction rack. It takes information from 1 csv, stock_reagents. It takes sequentially the reactant from the 24 fluidx racks to the 96 plate"""

from opentrons import robot, containers, instruments
robot.head_speed(x=18000, y=18000, z=5000, a=250, b=250)

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
reaction_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\coupling_sequence_phip - Try2\csv\main_reactant.csv")
reaction_conditions_df = read_csv(
    r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\coupling_sequence_phip - Try2\csv\reaction_conditions.csv")
def mainReactant_transfer(reactant, reaction):
    # Deck setup
    tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
    #source_trough12row = containers.load("trough-12row", "C1")
    location_stock = containers.load("FluidX_24_2ml", "A1")
    reaction_rack = containers.load("StarLab_96_tall", "D1")
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
    main_reactant_volume_header = "main reactant volume to add - per reaction (uL)"
    main_reactant_location_header = "Location 24 vial rack"
    volume_max_header = "Volume max per vial"
    nb_reaction_header = "Number reaction"


    for index, value in enumerate(reaction_conditions_df[id_header].tolist()):
        if value == reaction_to_start:
            volume_per_reaction = float(reaction_conditions_df[main_reactant_volume_header].tolist()[index])
            nb_reactions = int(reaction_conditions_df[nb_reaction_header].tolist()[index])

    reaction_counter = 0

    """In each well, the volume per reaction of reaction is dispensed, successively in the logical order ("A1", "A2"...). When the maximum amount of reactant in one vial is taken out, the following
    vial in the fluidx rack is used. The transfer stops when the reactant is dispensed in all the wells of the 96 plate or all the wells used for the batch."""
    for index, value in enumerate(reaction_df[main_reactant_location_header].tolist()):
        if reaction_counter < nb_reactions:
            nb_reaction_per_vial = int(float(reaction_df[volume_max_header].tolist()[index]) // volume_per_reaction)
            source_location = value
            if nb_reactions - reaction_counter < nb_reaction_per_vial:
                if nb_reactions - reaction_counter == 1:
                    p1000.distribute(volume_per_reaction, location_stock.wells(source_location),
                                     reaction_rack.wells(reaction_counter).top())
                    nb_reaction_per_vial =1
                else:
                    p1000.distribute(volume_per_reaction, location_stock.wells(source_location),
                                     [x.top() for x in reaction_rack.wells(reaction_counter, to=nb_reactions)])
            else:
                p1000.distribute(volume_per_reaction, location_stock.wells(source_location), [x.top() for x in
                                                                                              reaction_rack.wells(
                                                                                                  reaction_counter,
                                                                                                  to=reaction_counter + nb_reaction_per_vial - 1)])
            reaction_counter = reaction_counter + nb_reaction_per_vial
    robot.home()
mainReactant_transfer(reaction_df, reaction_conditions_df)