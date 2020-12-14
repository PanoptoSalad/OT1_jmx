####################################################################################################################
################################################  TITLE  ###########################################################
##################################---04_QC_pre-work-up_8C-300DL---##################################################
####################################################################################################################

"""Standard easy to use protocol that does not require external inputs. Only variable to change is the number of rows
that needs to be transfered to a QC plate for LCMS analysis. With a multichannel, 50uL of MeCN will be added in each 
well of a 96-well plate, low profile.Then 10uL of each reaction mixture will be transfered to the QC plate
"""
####################################################################################################################
############################################# Imports and libraries  ###############################################
####################################################################################################################
#libraries
from opentrons import robot, containers, instruments
# for simulation
#robot.reset()
#robot speed settings
robot.head_speed(x=18000,  y=18000,  z=3000, a=400, b=400)

####################################################################################################################
############################################# OT-1 Protocol ########################################################
####################################################################################################################

#Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
source_trough4row = containers.load("trough-12row", "C2")
reaction_rack = containers.load("Para_dox_96_short", "C1")
destination_QC = containers.load("96-PCR-flat", "B1", "QC") # QC plate
trash = containers.load("point", "B3")

#Pipettes SetUp. 8 Channels Dragon Lab, 300uL
p300_multi  = instruments.Pipette(
    name='dlab_300multi_no_min',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300],
    max_volume=300,
    min_volume=0,
    channels=8,
)

#Variables needed, that are obvious enough they can be changed on the go.
volume_to_dispense = 10 # how much reaction mixture to QC
location_QC_solvent = 'A5' # Where on the solvent trough is the solvent
volume_QC_solvent = 50 # how much solvent per QC well to add
number_rows = 10 # how many times the 8 channel pipette has to dispense QC solvent
number_rows = number_rows - 1

#Source and destination lists setup
source_location = [well.bottom(4) for well in reaction_rack.rows(0, to=number_rows)] # where to extract reaction mixture from
destination_location = [well.bottom(1) for well in destination_QC.rows(0, to=number_rows)] # where to dispense reaction mixture to
destination_QC_solvent = [x.top() for x in destination_QC.rows(0,to=number_rows)] # where to dispense the QC solvent to

#Liquid transfer lines.
p300_multi.distribute(volume_QC_solvent, source_trough4row.wells(location_QC_solvent), destination_QC_solvent) # dispense QC solvent
p300_multi.transfer(volume_to_dispense, source_location, destination_location, blow_out=True, new_tip = 'always') # dispense reaction mixture
robot.home()

# for simulation
#robot.commands()