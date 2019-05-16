from opentrons import robot, containers, instruments

robot.head_speed(x=18000, y=18000, z=5000, a=700, b=700)


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
reactants_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\coupling_sequence_phip - Try2\csv\reactants_list.csv")
reaction_conditions_df = read_csv(
    r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\coupling_sequence_phip - Try2\csv\reaction_conditions.csv")

def reactants_transfer(reactants, reaction):
    # Deck setup

    tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
    tiprack_1000_2 = containers.load("tiprack-1000ul-H", "D3")
    #tiprack_1000_3 = containers.load("tiprack-1000ul-H", "B1")
    source_trough4row = containers.load("trough-12row", "C2")
    rack_stock_reactants_1 = containers.load("FluidX_24_2ml", "A1")
    rack_stock_reactants_2 = containers.load("FluidX_24_2ml", "A2")
    rack_stock_reactants_3 = containers.load("FluidX_24_2ml", "B1")
    rack_stock_reactants_4 = containers.load("FluidX_24_2ml", "B2")
    reaction_rack = containers.load("StarLab_96_tall", "C1")
    trash = containers.load("point", "C3")

    # Pipettes SetUp
    p1000 = instruments.Pipette(
        name='eppendorf1000',
        axis='b',
        trash_container=trash,
        tip_racks=[tiprack_1000, tiprack_1000_2],
        max_volume=1000,
        min_volume=30,
        channels=1,
    )

    id_header = "reaction"
    reaction_to_start = "Coupling_sequence"
    reactant_location_header = "Location"
    reactant_volume_header = "reactant 2 volume to add - per reaction (uL)"
    rack_ID_header = "Rack ID"
    rack_1 = "24_rack1"
    rack_2 = "24_rack2"
    rack_3 = "24_rack3"
    rack_4 = "24_rack4"

    for index, value in enumerate(reaction_conditions_df[id_header].tolist()):
        if value == reaction_to_start:
            volume_per_reaction = float(reaction_conditions_df[reactant_volume_header].tolist()[index])

    #counter = 0
    for i, v in enumerate(reactants_df[rack_ID_header].tolist()):
        source_location = reactants_df[reactant_location_header].tolist()[i]

        if v == "":
            #print('null')
            break
        if v == rack_1:
            p1000.pick_up_tip()
            p1000.transfer(volume_per_reaction, rack_stock_reactants_1.wells(source_location),
                           reaction_rack.wells(i + 2).top(-5), new_tip='never')
            p1000.drop_tip()
        if v == rack_2:
            p1000.pick_up_tip()
            p1000.transfer(volume_per_reaction, rack_stock_reactants_2.wells(source_location),
                           reaction_rack.wells(i + 2).top(-5), new_tip='never')
            p1000.drop_tip()
        if v == rack_3:
            p1000.pick_up_tip()
            p1000.transfer(volume_per_reaction, rack_stock_reactants_3.wells(source_location),
                           reaction_rack.wells(i + 2).top(-5), new_tip='never')
            p1000.drop_tip()
        if v == rack_4:
            p1000.pick_up_tip()
            p1000.transfer(volume_per_reaction, rack_stock_reactants_4.wells(source_location),
                           reaction_rack.wells(i + 2).top(-5), new_tip='never')
            p1000.drop_tip()
        #counter += 1

    #deprecated: counter only if needs to add more solvent to reaction after addition of reactants
    # p1000.pick_up_tip()
    #for i, x in enumerate(solvent_df[id_header].tolist()):
    #    if x == solvent:
    #        vol_to_add = [solvent_df[solvent_volume_header].tolist()[i]]
    #        solvent_loc = [solvent_df[solvent_location_header].tolist()[i]]

    #p1000.distribute(vol_to_add, source_trough4row.wells(solvent_loc),
    #                 [x.top() for x in reaction_rack.wells(0, to=counter + 1)])
    #print(counter)
    robot.home()
reactants_transfer(reactants_df, reaction_conditions_df)