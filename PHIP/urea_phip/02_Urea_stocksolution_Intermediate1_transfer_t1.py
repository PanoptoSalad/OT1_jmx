#!/usr/bin/env python
# coding: utf-8

# In[22]:


from opentrons import robot, containers, instruments
robot.head_speed(x=18000,  y=18000,  z=5000, a=250, b=250)

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
#Function that reads a csv file correctly without having to import anything (issues with molport). Uses 2 classes, Vector and DataFrame
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

#CSV file data
reaction_df = read_csv(r"C:\Users\opentrons\protocols\PHIP_Feb2019\reaction_step1_MeI.csv")
solvent_df = read_csv(r"C:\Users\opentrons\protocols\PHIP_Feb2019\Solvents.csv")
robot.reset()

def intermediate_transfer (reaction, solvent):
    #Deck setup
    tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
    source_trough12row = containers.load("trough-12row", "C1")
    location_int = containers.load("FluidX_24_5ml", "A1", "int")
    reaction_rack = containers.load("StarLab_96_tall", "D1")
    trash = containers.load("point", "C3")
    #Pipettes SetUp
    p1000 = instruments.Pipette(
        name= 'eppendorf1000',
        axis='b',
        trash_container=trash,
        tip_racks=[tiprack_1000],
        max_volume=1000,
        min_volume=30,
        channels=1,
    )
    
    location_header = "Location"
    #stock1 = "ImidInt-1"
    #stock2 = "ImidInt-2"
    #code_header = "Code"
    nb_reaction_header = "number of reaction"
    volume_per_reaction_header = "Volume_stock per reaction"
    
    n=0
    for i, x in enumerate(reaction_df[location_header].tolist()):
        
        nb_reaction = int(reaction_df[nb_reaction_header].tolist()[i])
        volume_per_reaction = int(reaction_df[volume_per_reaction_header].tolist()[i])
        source_location = reaction_df[location_header].tolist()[i]
        volume_list = []
        destination_list = []
        #for i in range (n+0, n+nb_reaction):
            #destination_list.append(i)
            #volume_list.append(volume_per_reaction)
        p1000.distribute(volume_per_reaction, location_int.wells(source_location), [x.top() for x in reaction_rack.wells(n+0, to=n + nb_reaction-1)])
        n = nb_reaction + n

intermediate_transfer(reaction_df, solvent_df)
