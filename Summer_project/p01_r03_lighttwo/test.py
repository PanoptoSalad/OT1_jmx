from opentrons import robot, containers, instruments

containers.create(
    'jMX_big_vial_holder',                    # name of you container
    grid=(3,4),                    # specify amount of (columns, rows)
    spacing=(23, 23),               # distances (mm) between each (column, row)
    diameter= 1.3,                     # diameter (mm) of each well on the plate
    depth= 68.0)                       # depth (mm) of each well on the plate
print(containers.list())