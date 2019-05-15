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
reaction_conditions_df = read_csv(
    r"C:\Users\sdi35357\CODING\github_repo\OT1-coding\coupling_sequence_phip - Try2\csv\forMeIAddition\reaction_conditions.csv")

def reactants_transfer(reactants):
    # Deck setup

    tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
    tiprack_1000_2 = containers.load("tiprack-1000ul-H", "D3")
    #tiprack_1000_3 = containers.load("tiprack-1000ul-H", "B1")
    storage_rack = containers.load("FluidX_24_2ml", "D1")
    destination_rack1 = containers.load("StarLab_96_tall", "A1")
    trash = containers.load("point", "C3")


    # Pipettes SetUp
    p1000 = instruments.Pipette(
        name='eppendorf1000_no_min',
        axis='b',
        trash_container=trash,
        tip_racks=[tiprack_1000, tiprack_1000_2],
        max_volume=1000,
        min_volume=0,
        channels=1,
    )
    id_header = "reaction"
    reaction_to_start = "Coupling_sequence"
    split_volume_header = "volume amine to add"
    transfer_number_header = "number of transfer per vial"

    for index, value in enumerate(reaction_conditions_df[id_header].tolist()):
        if value == reaction_to_start:
            volume_per_reaction = float(reaction_conditions_df[split_volume_header].tolist()[index])
            transfer_number = int(reaction_conditions_df[transfer_number_header].tolist()[index])
            source_location_1 = [storage_rack.wells(0).bottom()]
            source_location_2 = [storage_rack.wells(1).bottom()]
            source_location_3 = [storage_rack.wells(3).bottom()]

            destination_1 = [x.top() for x in destination_rack1.wells(0, to=transfer_number-1)]
            destination_2 = [x.top() for x in destination_rack1.wells(transfer_number, to=transfer_number*2-1)]
            destination_3 = [x.top() for x in destination_rack1.wells(transfer_number*2, to=transfer_number*3-1)]

            p300_multi.distribute(volume_per_reaction, source_location_1,destination_1, air_gap=10)
            p300_multi.distribute(volume_per_reaction, source_location_2,destination_2, air_gap=10)
            p300_multi.distribute(volume_per_reaction, source_location_3,destination_3, air_gap=10)
reactants_transfer(reaction_conditions_df)
