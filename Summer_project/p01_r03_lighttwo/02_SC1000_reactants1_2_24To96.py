"""Protocol that transfers the aryl halide and N-BOC-amino acid to each well on the photoredox plate
Requires 3 csv: rack1, rack2 and reactions conditions.
How it works:
A column will be assigned to rack 1 or rack 2, and a row will be assigned to the other rack.
The code then iteratively adds the column and row reagents. In this case of 10 columns, 7 rows:
Col reagent: 10 different Aryl halides added, each reagent added 7 times to each well along a row
Row reagent: 7 different N-BOC-amino acid added, each reagent added 10 times to each well along a column

96 photoredox well plate
      
      Aryl Halides (cols)
Nboc1 o o o o o o o o o o x x
Nboc2 o o o o o o o o o o x x
Nboc3 o o o o o o o o o o x x
Nboc4 o o o o o o o o o o x x
Nboc5 o o o o o o o o o o x x
Nboc6 o o o o o o o o o o x x
Nboc7 o o o o o o o o o o x x
rows  x x x x x x x x x x x x

"""

#import the libraries
from opentrons import robot, containers, instruments

robot.head_speed(x=18000, y=18000, z=5000, a=700, b=700)

#class Vector, Dataframe and function read csv arejust there to ba able to read a csv file without having to call numpy, which is not possible with OT1

class Vector(object):
    '''Storing and manipulating two-dimensional data'''
    def tolist(self):
        '''Convert vector object to list'''
        return list(self.input_list)

    def astype(self, input_type):
        '''Cast a vector to a specific type'''
        if input_type == int:
            return Vector([int(float(x)) for x in self.input_list])
        return Vector([input_type(x) for x in self.input_list])

    def __init__(self, input_list):
        self.input_list = input_list


class DataFrame(object):
    '''DataFrame class obtained from a dictionary'''
    def __len__(self):
        '''Get length of dataframe'''
        return self.length

    def __getitem__(self, value):
        '''Get a vector from dataframe based on value input'''
        return Vector(self.dict_input[value])

    def __init__(self, dict_input, length):
        self.dict_input = dict_input
        self.length = length


# Function that reads a csv file correctly without having to import anything. Uses 2 classes, Vector and DataFrame
def read_csv(input_file):
    '''reads a csv file, converts it into a dataframe'''
    lines = open(input_file).readlines()
    header = lines[0].rstrip().split(",") # get header from csv file by removing commas on first line
    out_d = {} # initiliase empty dictionary to add headers
    for head in header:
        out_d[head] = [] # initialise empty list to append values
    for line in lines[1:]:
        spl_line = line.rstrip().split(",") # remove commas from other lines
        for i, head in enumerate(header):
            out_d[head].append(spl_line[i]) # values have been appended to list, as part of dictionary
    df = DataFrame(out_d, len(lines[1:])) # convert dictionary to dataframe
    return df


# CSV file data
reaction_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\Summer_project\p01_r03_lighttwo\csv\050919_JMX_56_reactions\reaction_conditions.csv")
reactant_col_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\Summer_project\p01_r03_lighttwo\csv\050919_JMX_56_reactions\rack1.csv")
reactant_row_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\Summer_project\p01_r03_lighttwo\csv\050919_JMX_56_reactions\rack2.csv")

#reaction_df = read_csv(r"csv\200819_JMX_1_testrun\reaction_conditions.csv")
#reactant_col_df = read_csv(r"csv\200819_JMX_1_testrun\rack1.csv")
#reactant_row_df = read_csv(r"csv\200819_JMX_1_testrun\rack2.csv")

def reactants_transfer(reaction,reactant_col,reactant_row):
    # Deck setup
    tiprack_1000 = containers.load("tiprack-1000ul-H", "D3")
    # tiprack_1000_2 = containers.load("tiprack-1000ul-H", "D3")
    source_trough4row = containers.load("trough-12row", "B2")
    rack_stock_reactant_1 = containers.load("FluidX_24_5ml_jmx", "A1", "R_1")
    rack_stock_reactant_2 = containers.load("FluidX_24_5ml_jmx", "A2", "R_2")
    reaction_rack = containers.load("Para_dox_96_short", "C1")
    trash = containers.load("point", "B3")

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
            number_cols = int(reaction_df[details_header].tolist()[index]) # read no. of cols for reagents

        if value == number_of_rows:
            number_rows = int(reaction_df[details_header].tolist()[index]) # read no. of rows for reagents


        if value == reactant_row:
            volume_to_dispense_row = reaction_df[volume_to_add].tolist()[index]
            if reaction_df[rack_id].tolist()[index] == rack_1: # checks which are the row and column reagents
                rack_stock_row = rack_stock_reactant_1
                rack_stock_col = rack_stock_reactant_2
            else:
                rack_stock_col = rack_stock_reactant_1
                rack_stock_row = rack_stock_reactant_2
        if value == reactant_col:
            volume_to_dispense_col = reaction_df[volume_to_add].tolist()[index]

    for index, location in enumerate (reactant_col_df[location_reactant].tolist()): # distributes to each row for a column reagent
        source_location = location
        volume_to_dispense = [volume_to_dispense_col]
        p1000.distribute(volume_to_dispense, rack_stock_col.wells(source_location), [x.top(-15) for x in reaction_rack.rows(index).wells(0, to=number_rows-1)], air_gap=10)
    #robot.pause()
    for index, location in enumerate (reactant_row_df[location_reactant].tolist()): # distributes to each column for a row reagent
        source_location = location
        volume_to_dispense = [volume_to_dispense_row]
        p1000.distribute(volume_to_dispense, rack_stock_row.wells(source_location), [x.top(-15) for x in reaction_rack.cols(index).wells(0, to=number_cols-1)], air_gap=10)


reactants_transfer(reaction_df,reactant_col_df,reactant_row_df)

for c in robot.commands():
    print(c)
