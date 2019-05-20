from opentrons import robot, containers, instruments
robot.head_speed(x=20000,  y=20000,  z=5000, a=100, b=700)

#Deck setup
tiprack_300 = containers.load("tiprack-300ul", "D3")
source_trough12row = containers.load('trough-12row', "E2")
pwup_rack = containers.load("FluidX_96_small", "D1", "pwup rack")
trash = containers.load("point", "B3")

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
source_location = 'A11'
volume_to_dispense = 189
number_rows = 10

p300_multi.distribute(volume_to_dispense, source_trough12row.wells(source_location), [x.top(1) for x in pwup_rack.rows(0,to=number_rows)], air_gap=10)
robot.home()
