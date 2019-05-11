'''OT1 -Single channel- Making up of main reagent stock solution (2 maximum) using a defined solvent and transfer onto 3mL fluidx vials'''

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
stock_reagent_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\urea_phip_triple_reaction\csv\stock_reagents.csv")
solvent_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\urea_phip_triple_reaction\csv\solvents.csv")

"""Function that does two liquid handling transfers. First it will dilute a solid reagent in a big trough to the right concentration.
(Up to 2 reagents). Second, it will transfer the reagent from the big trough to the Fluix 24 vial rack, using the volume from the csv file
It requires 2 csv files. The first is the solvent csv, the second the custom made stock reagent csv."""


def stock_solution(amine, solvent):
    # Deck setup
    tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
    source_trough4row = containers.load("trough-12row", "C2")
    destination_stock = containers.load("FluidX_24_5ml", "A1", "stock")
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

    id_header = "CPD ID"
    solvent = "DMA"
    stock_sol1 = "stock reagent 2"
    location_header = "Location_trough"
    destination_location_header = "Location"
    volume_stock_header = "Volume to dispense (uL)"
    volume_per_vial = "Volume to dispense"

    for i, x in enumerate(solvent_df[id_header].tolist()):
        if x == solvent:
            solvent_location = solvent_df[location_header].tolist()[i]
        if x == stock_sol1:
            stock_sol1_loc = solvent_df[location_header].tolist()[i]
            stock_sol1_volume = solvent_df[volume_stock_header].tolist()[i]
    # Using the desired solvent, dilution of reagents 1 and/or 2 to the desired conc, in the big trough
    p1000.pick_up_tip()
    p1000.transfer([stock_sol1_volume], source_trough4row.wells(solvent_location),
                   source_trough4row.wells(stock_sol1_loc).top(-5), new_tip='never')
    p1000.drop_tip()
    robot.home()
stock_solution(stock_reagent_df, solvent_df)