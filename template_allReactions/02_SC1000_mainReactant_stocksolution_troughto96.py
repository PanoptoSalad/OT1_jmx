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
stock_reagent_df = read_csv(r"C:\Users\sdi35357\CODING\github_repo\OT1-coding\template_allReactions\csv\main_reactant.csv")
reaction_conditions_df = read_csv(
    r"C:\Users\sdi35357\CODING\github_repo\OT1-coding\template_allReactions\csv\reaction_conditions.csv")

def transfer_storageVial(condition, reactant):
    # Deck setup
    tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
    source_trough4row = containers.load("trough-12row", "C2")
    #destination_stock = containers.load("Starlab_96_Square_2mL", "A1", "2mL_rack")
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

    id_header = "reaction"
    reaction_to_start = "Coupling_standard"
    solvent_trough_location_header = "main reactant solvent Location"
    reactant_trough_location_header = "main reactant location"
    storage_vial_location_header = "Location 24 vial rack"
    volume_per_vial_header = "Volume to dispense"

    for index, value in enumerate(reaction_conditions_df[id_header].tolist()):
        if value == reaction_to_start:
            reactant_trough_location = reaction_conditions_df[reactant_trough_location_header].tolist()[index]

    # Reactant 1 is transfered to the 24 Fluidx storage vial rack.
    p1000.pick_up_tip()
    for i, v in enumerate(stock_reagent_df[storage_vial_location_header].tolist()):
        vial_location = v
        volume_to_dispense = [stock_reagent_df[volume_per_vial_header].tolist()[i]]
        if volume_to_dispense != 0:
            p1000.transfer(volume_to_dispense, source_trough4row.wells(reactant_trough_location),
                           destination_stock.wells(vial_location).top(-5), new_tip='never')
    p1000.drop_tip()
    robot.home()
transfer_storageVial(stock_reagent_df, reaction_conditions_df)