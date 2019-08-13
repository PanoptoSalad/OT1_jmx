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


# Function that reads a csv file correctly without having to import anything. Uses 2 classes, Vector and DataFrame
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
reaction_df = read_csv(r"C:\Users\sdi35357\CODING\github_repo\OT1-coding\Summer_project\p01_r01_coupling\csv\reaction_conditions.csv")
reactant_col_df = read_csv(r"C:\Users\sdi35357\CODING\github_repo\OT1-coding\Summer_project\p01_r01_coupling\csv\SM_AcOH.csv")
reactant_row_df = read_csv(r"C:\Users\sdi35357\CODING\github_repo\OT1-coding\Summer_project\p01_r01_coupling\csv\SM_Amine.csv")

def reactants_transfer(reaction,reactant_col,reactant_row):
    
    # Deck setup
    tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
    tiprack_1000_2 = containers.load("tiprack-1000ul-H", "D3")
    source_trough4row = containers.load("trough-12row", "C2")
    rack_stock_reactant_1 = containers.load("FluidX_24_5ml", "A1", "R_1")
    rack_stock_reactant_2 = containers.load("FluidX_24_5ml", "A2", "R_2")
    reaction_rack = containers.load("StarLab_96_tall", "C1")
    trash = containers.load("point", "B3")

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
    
    
    id_header = "Reaction parameters type"
    rack_id = "Rack ID"
    reactant_row = "Reactant row"
    reactant_col = "Reactant col"
    details_header = "Reaction details"
    location_heading = "Location_trough"
    volume_to_add = "Volume to add (uL)"
    number_of_columns = "Number columns"
    number_of_rows = "Number rows"
    rack_1 = "24_rack1"
    rack_2 = "24_rack2"
    location_reactant = "Location"
    
    
    for index, value in enumerate(reaction_df[id_header].tolist()):
        if value == number_of_columns:
            number_cols = int(reaction_df[details_header].tolist()[index])
                
        if value == number_of_rows:
            number_rows = int(reaction_df[details_header].tolist()[index])
                   

        if value == reactant_row:
            volume_to_dispense_row = reaction_df[volume_to_add].tolist()[index]
            if reaction_df[rack_id].tolist()[index] == rack_1:
                rack_stock_row = rack_stock_reactant_1
                rack_stock_col = rack_stock_reactant_2
            else:
                rack_stock_col = rack_stock_reactant_1
                rack_stock_row = rack_stock_reactant_2          
        if value == reactant_col:
            volume_to_dispense_col = reaction_df[volume_to_add].tolist()[index]
            
    for index, location in enumerate (reactant_col_df[location_reactant].tolist()):
        source_location = location
        volume_to_dispense = [volume_to_dispense_col]
        p1000.distribute(volume_to_dispense, rack_stock_col.wells(source_location), [x.top(-15) for x in reaction_rack.rows(index).wells(0, to=number_rows-1)], air_gap=10)
    robot.pause()
    for index, location in enumerate (reactant_row_df[location_reactant].tolist()):
        source_location = location
        volume_to_dispense = [volume_to_dispense_row]
        p1000.distribute(volume_to_dispense, rack_stock_row.wells(source_location), [x.top(-15) for x in reaction_rack.cols(index).wells(0, to=number_cols-1)], air_gap=10)

    robot.home()

reactants_transfer(reaction_df,reactant_col_df,reactant_row_df)
