from opentrons import robot, containers, instruments
robot.head_speed(x=16000,  y=16000,  z=4000, a=700, b=700)

#Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
tiprack_300_2 = containers.load("tiprack-300ul", "E2")
source_trough4row = containers.load("trough-12row", "C2")
reaction_rack = containers.load("StarLab_96_tall", "D1")
trash = containers.load("point", "C3")

#Pipettes SetUp
p300_multi  = instruments.Pipette(
    name='dlab_300multi',
    axis="a",
    trash_container=trash,
    tip_racks=[tiprack_300, tiprack_300_2],
    max_volume=300,
    min_volume=30,
    channels=8,
)
source_solvent = 'A8'
volume_solvent = 300
source_aqueous = 'A11'
volume_aqueous = 300
number_rows = 7

for i in range(0, number_rows):
    p300_multi.pick_up_tip()
    p300_multi.mix(10, 300, reaction_rack.rows(i).bottom(10))
    p300_multi.drop_tip()
robot.home()

#robot.commands()

