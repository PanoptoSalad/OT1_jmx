from opentrons import robot, containers, instruments
robot.head_speed(x=18000,  y=18000,  z=5000, a=700, b=700)
#Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
source_trough4row = containers.load("trough-12row", "C2")
reaction_rack = containers.load("Starlab_96_Square_2mL", "D1")
destination_wup = containers.load("Starlab_96_Square_2mL", "B1")
trash = containers.load("point", "C3")

#Pipettes SetUp
p300_multi  = instruments.Pipette(
    name='dlab_300multi',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300],
    max_volume=300,
    min_volume=30,
    channels=8,
)
source_solvent = 'A8'
volume_to_dispense = 450
number_rows = 2

for i in range(0, number_rows):
    p300_multi.pick_up_tip()
    p300_multi.aspirate (150, source_trough4row.wells(source_solvent))
    p300_multi.dispense (source_trough4row.wells(source_solvent))
    p300_multi.transfer(volume_to_dispense, reaction_rack.rows(i).bottom(), destination_wup.rows(i).top(-5), blow_out = True, air_gap=5)
robot.home()
