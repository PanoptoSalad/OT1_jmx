#!/usr/bin/env python
# coding: utf-8

from opentrons import robot, containers, instruments
robot.head_speed(x=21000,  y=21000,  z=5000, a=700, b=700)

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
solvent_df = read_csv(r"C:\Users\opentrons\protocols\PHIP_Feb2019\Solvents.csv")
robot.reset()

def stock_solution (intermediate, solvent):
    
    #Deck setup
    tiprack_1000 = containers.load("tiprack-1000ul-H", "B3")
    source_trough4row = containers.load("trough-12row", "C2")
    destination_int = containers.load("FluidX_24_5ml", "A1", "int")
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
    
    id_header = "CPD ID"    
    solvent = "MeCN"
    stock_sol1 = "Intermediate1"
    stock_sol2 = "Intermediate2"
    location_header = "Location_trough"
    destination_location_header = "Location"
    volume_stock_header = "Volume to dispense (uL)"
    volume_per_vial = "Volume to dispense"
    stock1 = "ImidInt-1"
    stock2 = "ImidInt-2"
    code_header = "Code"
    
    for i, x in enumerate(solvent_df[id_header].tolist()):
        if x == solvent:
            solvent_location = solvent_df[location_header].tolist()[i]
        if x == stock_sol1:
            stock_sol1_loc = solvent_df[location_header].tolist()[i]
            stock_sol1_volume = solvent_df[volume_stock_header].tolist()[i]
        if x == stock_sol2:
            stock_sol2_loc = solvent_df[location_header].tolist()[i]
            stock_sol2_volume = solvent_df[volume_stock_header].tolist()[i]
    #p1000.pick_up_tip()
    #p1000.transfer([stock_sol1_volume], source_trough4row.wells(solvent_location), source_trough4row.wells(stock_sol1_loc).top(-5), new_tip = 'never')
    #p1000.drop_tip()
    #p1000.pick_up_tip()
    #p1000.transfer([stock_sol2_volume], source_trough4row.wells(solvent_location), source_trough4row.wells(stock_sol2_loc).top(-5), new_tip = 'never')
    #p1000.drop_tip()
    #print(solvent_location, stock_sol1_loc, stock_sol2_loc, stock_sol1_volume, stock_sol2_volume)

    #robot.pause()
    for i, x in enumerate(intermediate_df[destination_location_header].tolist()):
        destination_location = x
        vol_to_dispense = [intermediate_df[volume_per_vial].tolist()[i]]
        intermediate_id = intermediate_df[code_header].tolist()[i]
        p1000.pick_up_tip()
        if intermediate_id == stock1:
            #print ('correct')
            if vol_to_dispense != 0:
                p1000.transfer(vol_to_dispense, source_trough4row.wells(stock_sol1_loc), destination_int.wells(destination_location).top(-5), new_tip = 'never')   
        if intermediate_id == stock2:
            #print ('incorrect')
            p1000.drop_tip()
            p1000.pick_up_tip()
            if vol_to_dispense != 0:
                p1000.transfer(vol_to_dispense, source_trough4row.wells(stock_sol2_loc), destination_int.wells(destination_location).top(-5), new_tip = 'never')   

        p1000.drop_tip()
        #else:
         #   print ("error")
          #  break

        print(destination_location,vol_to_dispense,intermediate_id, stock1)
    robot.home()
stock_solution(intermediate_df, solvent_df)
#robot.commands()
