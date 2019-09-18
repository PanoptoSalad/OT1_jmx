"""Protocol that transfers the reagents which are on the third stock solution rack. In the case of the light reactions,
it can be the iridium catalyst, the ligand and the base.
It requires 2 csv files: rack3 and reactions conditions.
How it works:
Each vial of the rack is a dictionary containing the key parameters.
For each reagents a list of the dictionaries containing the same reagents is made
A list grouping these three list is then created

"""
#import the libraries
from opentrons import robot, containers, instruments
#set up robot arm movement speed. Max speed: {"x": 20000,  "y": 20000,  "z": 6000, "a": 1200, "b": 1200}

robot.head_speed(x=18000, y=18000, z=5000, a=700, b=700)

#class Vector, Dataframe and function read csv arejust there to ba able to read a csv file without having to call numpy, which is not possible with OT1

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

#Import of csv files


reaction_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\Summer_project\p01_r03_lighttwo_2.0\csv\050919_JMX_56_reactions\reaction_conditions.csv")
rack_three_df = read_csv(r"C:\Users\opentrons\protocols\GitHub_repos\OT1-coding\Summer_project\p01_r03_lighttwo_2.0\csv\050919_JMX_56_reactions\Nirack.csv")

#reaction_df = read_csv(r"csv\050919_JMX_56_reactions\reaction_conditions.csv")
#rack_three_df = read_csv(r"csv\050919_JMX_56_reactions\Nirack.csv")

# Deck setup
tiprack_1000 = containers.load("tiprack-1000ul-H", "D3")
tiprack_1000_2 = containers.load("tiprack-1000ul-H", "C3")
source_trough4row = containers.load("trough-12row", "C2")
rack_stock_reactant_1 = containers.load("FluidX_24_5ml_jmx", "A1", "R_1")
rack_stock_reactant_2 = containers.load("FluidX_24_5ml_jmx", "A2", "R_2")
rack_stock_reactant_3 = containers.load("FluidX_24_5ml_jmx", "B1", "R_3")
reaction_rack = containers.load("Para_dox_96_short", "C1")
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

#variables names, for quicker typing. Mostly headings from csv files

id_header = "Reaction parameters type"
rack_id = "Rack ID"
reactant_row = "Reactant row"
reactant_col = "Reactant col"
details_header = "Reaction details"
location_heading = "Location_trough"
volume_to_add = "Volume to add (uL)"
number_of_columns_header = "Number columns"
number_of_rows_header = "Number rows"
rack_1 = "24_rack1"
rack_2 = "24_rack2"
rack_3 = "24_rack3"
location_reactant = "Location"
volume_max_header = "Volume max per vial (ul)"
reagent_two = "Reagent 2"
number_transfer = "Number of transfer per vial"

# This reads the main parameters from the csv: reaction conditions and get the useful values
for index, value in enumerate(reaction_df[id_header].tolist()):
        if value == number_of_columns_header:
            number_cols = int(reaction_df[details_header].tolist()[index])
        if value == number_of_rows_header:
            number_rows = int(reaction_df[details_header].tolist()[index])
        if value == reagent_two:
            volume_to_dispense_reagent_two = float(reaction_df[volume_to_add].tolist()[index])

#function that needs the number of columns and rows used (number of Reactants A and B) and will give as an output the platmap of the wells
#that the robot will dispense to. This is necesseary when using a combinatorial mode. 
            
def dispensingListGeneration (number_cols,number_rows):
    well_list = []
    for column in range(0,number_cols):
        for row in range (0, number_rows):
            well_list.append(chr(row+65)+str(column+1))
    return(well_list)

#variables, number of reactions and list of wells used in the reaction plate. wells_transfer_list is a list of the exact location of the destination, and robot position

number_reactions = number_cols * number_rows
list_of_wells_reaction_rack = dispensingListGeneration(number_cols,number_rows)
wells_transfer_list = []
for well in list_of_wells_reaction_rack:
    wells_transfer_list.append(reaction_rack.wells(well).top(-4))


#creation of a list that will contain dictionaries. Each dictionary is a vial from the rack of reagents. and contains the useful values.
list_dictionary = []
#Loop that creates the dictionaries (one per vial). It manily uses the csv rack3
for index, value in enumerate(rack_three_df[id_header].tolist()):
    dictionary_loop = {}
    dictionary_loop[id_header] = value
    dictionary_loop[rack_id] = rack_three_df[rack_id].tolist()[index]
    dictionary_loop[volume_max_header] = rack_three_df[volume_max_header].tolist()[index]
    dictionary_loop[location_reactant] = rack_three_df[location_reactant].tolist()[index]
    list_dictionary.append(dictionary_loop)


#Probably not very smart; creation of 4 lists: 3 lists that contains dictionaries containing the same reagent and the global one that contain the 3 lists, one after another.
reagent_one_list = []
reagent_two_list = []
reagent_three_list = []
list_dict_per_reagent = []    

#Assign each dictionary with a reagent to its corresponding list.
# Also adds  a key to each dictionary, the volume to dispense per reaction 
for dictionary in list_dictionary:
    if dictionary[id_header] == "Reagent 2":
        dictionary[volume_to_add] = volume_to_dispense_reagent_two
        reagent_two_list.append(dictionary)
# Overall list containing the list of dictionaries per reagent
list_dict_per_reagent = [reagent_two_list]

# Function that takes as input a list of dictionary (same reagent) and the number of reactions. The output is another key to the dictionary, which is the number of transfer that will be executed for this vial
#If no transfers are needed for this vial then no key is created

def numbertransferPerVial(reagent_one_list, number_reactions):
    reaction_counter = 0
    nb_reaction_left = None
    for dictionary in reagent_one_list:
        nb_reaction_per_vial = int(float(dictionary[volume_max_header]) // float(dictionary[volume_to_add]))
        reaction_counter = reaction_counter + nb_reaction_per_vial        
        if reaction_counter < number_reactions:
            dictionary[number_transfer] = nb_reaction_per_vial
            nb_reaction_left = number_reactions - reaction_counter
            continue
        else:
            if nb_reaction_left is None:
                dictionary[number_transfer] = number_reactions
                return (reagent_one_list)
            else:
                dictionary[number_transfer] = nb_reaction_left
                return (reagent_one_list)

#Main transfer loop, around the list containing the 3 lists of dictionaries per reagents

for index, list_of_dictionaries in enumerate(list_dict_per_reagent):
    temp_container = wells_transfer_list.copy()
    #print(list_of_dictionaries)
    list_of_dictionaries = numbertransferPerVial(list_of_dictionaries, number_reactions)
    for dictionary in list_of_dictionaries:
        if number_transfer not in dictionary:
            continue
        else:
            p1000.distribute(dictionary[volume_to_add], rack_stock_reactant_3.wells(dictionary[location_reactant]), temp_container[:dictionary[number_transfer]],air_gap=10)
            del temp_container[:dictionary[number_transfer]]
            
for c in robot.commands():
    print(c)

