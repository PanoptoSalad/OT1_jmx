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
    r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\urea_phip_triple_reaction\csv\reaction_conditions.csv")


def reactants_transfer(reactants):
    # Deck setup

    tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
    tiprack_1000_2 = containers.load("tiprack-1000ul-H", "D3")
    # tiprack_1000_3 = containers.load("tiprack-1000ul-H", "B1")
    reaction_rack = containers.load("Starlab_96_Square_2mL", "A1")
    destination_rack1 = containers.load("StarLab_96_tall", "B1")
    destination_rack2 = containers.load("StarLab_96_tall", "C1")
    destination_rack3 = containers.load("StarLab_96_tall", "D1")
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
    reaction_to_start = "Coupling_urea_sulpho"
    split_volume_header = "split 2 volume to add per vial"
    rows_number_header = "Number rows"

    for index, value in enumerate(reaction_conditions_df[id_header].tolist()):
        if value == reaction_to_start:
            volume_per_vial = float(reaction_conditions_df[split_volume_header].tolist()[index])
            rows_number = int(reaction_conditions_df[rows_number_header].tolist()[index])
            for i in range(0, rows_number):
                source_location = reaction_rack.wells(i+2).bottom(1)
                # destination_1 = [x.top(-15) for x in destination_rack1.cols(0, to=number_vials - 1)]
                # pipette.transfer(100, plate.wells('A1'), plate.rows('2'))

                # p1000.distribute(volume_per_vial, source_location, destination_1)
                # p1000.distribute(volume_per_vial, source_location, [x.top(-15) for x in destination_rack1.wells(3 to=10)])
                p1000.pick_up_tip()
                p1000.distribute(volume_per_vial, source_location,
                                 [x.top(-15) for x in destination_rack1.rows(i).wells(2, to=7)], new_tip="never", air_gap = 10)
                p1000.distribute(volume_per_vial, source_location,
                                 [x.top(-15) for x in destination_rack2.rows(i).wells(0, to=7)], new_tip="never",air_gap = 10)
                p1000.distribute(volume_per_vial, source_location,
                                 [x.top(-15) for x in destination_rack3.rows(i).wells(0, to=5)], new_tip="never",air_gap = 10)
                p1000.drop_tip()


reactants_transfer(reaction_conditions_df)