####################################################################################################################
################################################  TITLE  ###########################################################
#########################---02_Reagents_Transfer_24To96_SC-1000eppendorf---#########################################
####################################################################################################################

"""Protocol that transfers the reagents on the third stock solution rack. In the case of the light reaction, the iridium and nickel pre-catalysts and iridium ligand.
It requires 2 csv files: rack3 and reactions conditions.
How it works:
Each vial of the rack is a dictionary containing the key parameters.
For each reagents a list of the dictionaries containing the same reagents is made
A list grouping these three list is then created

This protocol is more complex because it needs to take into account different reagents in the same csv file and multiple vials for one reagent.
There are many ways of writing the protocol better, but the intention here was to make it work first, and showing that even a beginner in Python could control the robot.
"""
####################################################################################################################
############################################# Libraries and functions ##############################################
####################################################################################################################
#import the libraries
from opentrons import robot, containers, instruments
#set up robot arm movement speed. Max speed: {"x": 20000,  "y": 20000,  "z": 6000, "a": 1200, "b": 1200}
robot.head_speed(x=18000, y=18000, z=5000, a=700, b=700)
#robot.reset() is needed for protocol simulation but needs to be commented in before running the protocol on OT-1
robot.reset()
#class Vector, Dataframe and function read_csv are to be able to read a csv file without using a library that utilises numpy, which was not supported by OT1.
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
    header = lines[0].rstrip().split(",") # get header from csv file by reading the first line, each header is separated by a comma
    out_d = {} # initialise empty dictionary
    for head in header:
        out_d[head] = [] # add headers as keys in dictionary value is initialised as empty lists
    for line in lines[1:]:
        spl_line = line.rstrip().split(",") # create a list per line, whitespaces removed, each item is a string that was separated by a comma
        for i, head in enumerate(header):
            out_d[head].append(spl_line[i]) # items from the list of a given line are appended to each heading list
    df = DataFrame(out_d, len(lines[1:])) # convert dictionary to dataframe
    return df

"""function that needs the number of columns and rows used (number of reactants A and B) as an input.
The output is a list corresponding to the platemap of the destination wells, the reaction wells.
It is a rudimentary function and the code will break if there is more 12/8 reactants A/B and vice versa.
In our case here, a platemap list for 70 reaction is created:
number_cols = 7
number_rows = 10
well_list = ["A1","A2", ..., "F9","F10"]
"""        
def dispensingListGeneration (number_cols,number_rows):
    well_list = []
    for column in range(0,number_cols):
        for row in range (0, number_rows):
            well_list.append(chr(row+65)+str(column+1))
    return(well_list)
"""input for this function is a list of dictionaries that has the same reagent (Reagent 1, 2 or 3).
The function adds the number of reactions that one vial can start as another key in the dictionaries.
In our case, if the volume in the vial is enough to start 70 reaction, then number_reactions will be set at 70
If the volume is not enough then number_reactions is set to the maximum the vial can start, the variable containing the number
of reaction left to start will be updated (initialised at 70). The same happens for the next vial containing the same reagents, and so on until the number
of reaction left to start is 0. All remaining vials for this reagent will have 0 has number of reactions to start"""

def addNumberOfTransferPerVial(dict_list_for_one_reagent, number_reactions):
    number_reaction_left = number_reactions
    for dictionary_per_vial in dict_list_for_one_reagent:
        number_transfer_from_vial = int(float(dictionary_per_vial[volume_max_header]) // float(dictionary_per_vial[volume_to_add])) # max volume // volume of each transfer
        if number_transfer_from_vial > number_reactions:
            dictionary_per_vial[number_transfer] = number_reactions
            continue
        else:
            dictionary_per_vial[number_transfer] = number_transfer_from_vial
            number_reaction_left = number_reaction_left - number_transfer_from_vial
            if number_reaction_left <= 0:
                number_reaction_left = 0
                dictionary_per_vial[number_transfer] = number_reaction_left
    return (dict_list_for_one_reagent)

####################################################################################################################
############################################# Dataframes and Variables #############################################
####################################################################################################################
#Convert CSV files to dataframes using the functions and classes set above
#The path needs updating to each system
reaction_df = read_csv(r"C:\Users\sdi35357\CODING\coding-course\OT1_jmx\Summer_project\test_biorxiv\reaction_conditions.csv")
rack_one_df = read_csv(r"C:\Users\sdi35357\CODING\coding-course\OT1_jmx\Summer_project\test_biorxiv\rack1.csv")
rack_two_df = read_csv(r"C:\Users\sdi35357\CODING\coding-course\OT1_jmx\Summer_project\test_biorxiv\rack2.csv")
rack_three_df = read_csv(r"C:\Users\sdi35357\CODING\coding-course\OT1_jmx\Summer_project\test_biorxiv\rack3.csv")

#variables names. Headings from csv files
id_header = "Reaction parameters type"
rack_id = "Rack ID"
volume_to_add = "Volume to add (uL)"
number_of_columns_header = "Number columns"
number_of_rows_header = "Number rows"
rack_3 = "24_rack3"
location_reactant = "Location"
volume_max_header = "Volume max per vial (ul)"
reagent_one = "Reagent 1"
reagent_two = "Reagent 2"
reagent_three = "Reagent 3"
number_transfer = "Number of transfer per vial"

####################################################################################################################
############################################# OT-1 Protocol ########################################################
####################################################################################################################

# Deck setup
tiprack_1000 = containers.load("tiprack-1000ul-H", "D3")
tiprack_1000_2 = containers.load("tiprack-1000ul-H", "C3")
rack_stock_reactant_3 = containers.load("FluidX_24_5ml_jmx", "B1", "R_3")
reaction_rack = containers.load("Para_dox_96_short", "C1")
trash = containers.load("point", "B3")

# Pipettes SetUp - 1000uL single channel pipette
p1000 = instruments.Pipette(
    name='eppendorf1000',
    axis='b',
    trash_container=trash,
    tip_racks=[tiprack_1000, tiprack_1000_2],
    max_volume=1000,
    min_volume=30,
    channels=1,
)

"""Extract the useful values from the csv file: reactions conditions, the values used in the protocols are:
number_cols
number_rows
volume_to_dispense_reagent_one (per reaction well)
volume_to_dispense_reagent_two (per reaction well)
volume_to_dispense_reagent_three (per reaction well)
"""
for index, value in enumerate(reaction_df[id_header].tolist()):
    if value == number_of_columns_header:
        number_cols = int(reaction_df[details_header].tolist()[index])
    if value == number_of_rows_header:
        number_rows = int(reaction_df[details_header].tolist()[index])
    if value == reagent_one:
        volume_to_dispense_reagent_one = float(reaction_df[volume_to_add].tolist()[index])
    if value == reagent_two:
        volume_to_dispense_reagent_two = float(reaction_df[volume_to_add].tolist()[index])
    if value == reagent_three:
        volume_to_dispense_reagent_three = float(reaction_df[volume_to_add].tolist()[index])

"""We used the function dispensingListGeneration to get the platemap list of all the destination wells needed for setting up the reaction.
The platemap list is then used to create a list that links each destination to its source rack, and also the offset position of the pipette when dispensing using the x,y and z(top) coordinates.
In this example:
number_reactions = 7*10 = 70
list_of_wells_reaction_rack = ["A1","A2", ..., "F9","F10"]
wells_transfer_list = [<Deck><Slot C1><Container Para_dox_96_short><Well A1>,
  (x=3.00, y=3.00, z=34.00)),
 (<Deck><Slot C1><Container Para_dox_96_short><Well B1>,
  (x=3.00, y=3.00, z=34.00)),...]
"""
number_reactions = number_cols * number_rows
list_of_wells_reaction_rack = dispensingListGeneration(number_cols,number_rows)
wells_transfer_list = []
for well in list_of_wells_reaction_rack:
    wells_transfer_list.append(reaction_rack.wells(well).top())

""" Creation of a list containing a dictionary per vial in rack_three, e.g, one dictionary per reagent row in the csv file
Keys per dictionaries are:
id_header -- reagent 1, 2 or 3
rack_id -- rack containing the reagents
volume_max_header -- the volume maximum that can be taken out per vial
location_reagent -- vial location in the rack ("A1", "A2" etc)...
All info is extracted from csv file rack3 """

all_reagents_dict_list = []
#Loop that creates the dictionaries (one per vial). 
for index, value in enumerate(rack_three_df[id_header].tolist()):
    dictionary_per_vial = {}
    dictionary_per_vial[id_header] = value
    dictionary_per_vial[rack_id] = rack_three_df[rack_id].tolist()[index]
    dictionary_per_vial[volume_max_header] = rack_three_df[volume_max_header].tolist()[index]
    dictionary_per_vial[location_reactant] = rack_three_df[location_reactant].tolist()[index]
    all_reagents_dict_list.append(dictionary_per_vial)

""" An entry is appended to each dictionary, the volume to dispense per reaction well, and four list are created.
reagent_one_dict_list, reagent_two_dict_list, reagent_three_dict_list groups the dictionaries per reagent
per_reagent_dict_list contains the three lists created above so it is possible to iterate.
"""
reagent_one_dict_list = []
reagent_two_dict_list = []
reagent_three_dict_list = []
per_reagent_dict_list = []    

#iterate through the list of dictionaries
for dictionary in all_reagents_dict_list:
    if dictionary[id_header] == "Reagent 1":
        dictionary[volume_to_add] = volume_to_dispense_reagent_one
        reagent_one_dict_list.append(dictionary)   
    if dictionary[id_header] == "Reagent 2":
        dictionary[volume_to_add] = volume_to_dispense_reagent_two
        reagent_two_dict_list.append(dictionary)
    if dictionary[id_header] == "Reagent 3":
        dictionary[volume_to_add] = volume_to_dispense_reagent_three
        reagent_three_dict_list.append(dictionary)
# Overall list containing the list of dictionaries per reagent
per_reagent_dict_list = [reagent_one_dict_list,reagent_two_dict_list,reagent_three_dict_list]        

"""Liquid transfer loop. It iterates through each of the dictionaries, uses the addNumberOfTransferPerVial to get the number of reaction that can be
started per vial and then the distribute method transfer the desired volume of reagent, from the source to its destination. """        
for index, dict_list_for_one_reagent in enumerate(per_reagent_dict_list):
    addNumberOfTransferPerVial(dict_list_for_one_reagent, number_reactions)    
    temp_destination_well_list = wells_transfer_list.copy()
    for dictionary in dict_list_for_one_reagent:
        if dictionary[number_transfer] == 0:
            continue
        else:
            p1000.distribute(dictionary[volume_to_add], rack_stock_reactant_3.wells(dictionary[location_reactant]), temp_destination_well_list[:dictionary[number_transfer]],air_gap=10)
            del temp_destination_well_list[:dictionary[number_transfer]]
            
#robot.commands is needed for protocol simulation
#robot.commands()