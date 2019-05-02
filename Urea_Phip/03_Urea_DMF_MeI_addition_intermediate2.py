#!/usr/bin/env python
# coding: utf-8

# In[6]:


from opentrons import robot, containers, instruments
robot.head_speed(x=18000,  y=18000,  z=5000, a=700, b=700)

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
intermediate_df = read_csv(r"C:\Users\opentrons\protocols\PHIP_Feb2019\Intermediates.csv")
solvent_df = read_csv(r"C:\Users\opentrons\protocols\PHIP_Feb2019\Solvents2.csv")

def dmf_iodomethane_multi (solvent):

    # Deck setup
    tiprack_300 = containers.load("tiprack-300ul", "D3")
    source_trough12row = containers.load('trough-12row', "E2")
    reaction_rack = containers.load("StarLab_96_tall", "D1")
    trash = containers.load("point", 'C3')

    # Pipettes SetUp
    p300_multi = instruments.Pipette(
        name='dlab_300multi',
        axis="a",
        trash_container=trash,
        tip_racks=[tiprack_300],
        max_volume=300,
        min_volume=30,
        channels=8,
    )
    # The protocol
    id_header = "CPD ID"
    solvent = "MeCN2"
    reagent = "MeI"
    solvent_location_header = "Location_trough"
    volume_to_dispense_header = "Volume to dispense (uL)"
    nb_rows_header = "nb_rows"

    
    for i, x in enumerate(solvent_df[id_header].tolist()):
        if x == solvent:
            solvent_location = solvent_df[solvent_location_header].tolist()[i]
            solvent_volume = int(solvent_df[volume_to_dispense_header].tolist()[i])
            nb_rows = solvent_df[nb_rows_header].tolist()[i]
            
        if x == reagent:
            reagent_location = solvent_df[solvent_location_header].tolist()[i]
            reagent_volume = int(solvent_df[volume_to_dispense_header].tolist()[i])

    p300_multi.distribute(solvent_volume, source_trough12row.wells(solvent_location), [x.top(-5) for x in reaction_rack.rows(0,to=nb_rows)])
    p300_multi.distribute(reagent_volume, source_trough12row.wells(reagent_location), [x.top(-5) for x in reaction_rack.rows(0,to=nb_rows)])
    robot.home()


dmf_iodomethane_multi (solvent_df)
