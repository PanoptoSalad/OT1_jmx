from opentrons import robot, containers, instruments

containers.create(
    'Para_dox_96_short',                    # name of you container
    grid=(12,8),                    # specify amount of (columns, rows)
    spacing=(9.08, 9.08),               # distances (mm) between each (column, row)
    diameter= 3,                     # diameter (mm) of each well on the plate
    depth= 28.0)                       # depth (mm) of each well on the plate
print(containers.list())