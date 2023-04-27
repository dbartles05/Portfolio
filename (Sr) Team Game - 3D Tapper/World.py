# sets up world environment, all map entities should be spawned in here

from ursina import Entity, color, Vec3
from ursina.lights import DirectionalLight
from World_Objects import Tap, Table, Doorway

# floor characteristics (base for room)
FLOOR_CHUNKS = 10
FLOOR_LENGTH = 9
FLOOR_WIDTH = 6
CHUNK_SIZE_X = 10
FLOOR_Y = 0
CHUNK_SIZE_Z = 5

FLOOR_POSITION = (0, FLOOR_Y, 0)

FLOOR_TEXTURE = "Textures/floored.png"

CEILING_TEXTURE = "Textures/roof.png"

# updates to fit floor
WALL_HEIGHT = 3
X_WALL_LENGTH = FLOOR_LENGTH
Z_WALL_LENGTH = FLOOR_WIDTH*2
WALL_THICKNESS = 1

WALL_TEXTURE = "Textures/wall2.png"

base_floor = Entity(model=None, collider=None)
base_ceiling = Entity(model=None, collider=None)

base_wall_x1 = Entity(model=None, collider=None)
base_wall_x2 = Entity(model=None, collider=None)
base_wall_z1 = Entity(model=None, collider=None)
base_wall_z2 = Entity(model=None, collider=None)

base_walls = [base_wall_x1, base_wall_x2, base_wall_z1, base_wall_z2]

for w in range(FLOOR_WIDTH):
    for l in range(FLOOR_LENGTH):
        # floor
        new_floor_chunk = Entity(model='cube', color=color.gray, scale=(CHUNK_SIZE_X, 1, CHUNK_SIZE_Z))
        new_floor_chunk.x = w * CHUNK_SIZE_X + FLOOR_POSITION[0]
        new_floor_chunk.z = l * CHUNK_SIZE_Z + FLOOR_POSITION[2]
        new_floor_chunk.y = FLOOR_Y
        new_floor_chunk.parent = base_floor

        new_ceil_chunk = Entity(model='cube', color=color.blue, scale=(CHUNK_SIZE_X, 1, CHUNK_SIZE_Z))
        new_ceil_chunk.x = w * CHUNK_SIZE_X + FLOOR_POSITION[0]
        new_ceil_chunk.z = l * CHUNK_SIZE_Z + FLOOR_POSITION[2]
        new_ceil_chunk.y = FLOOR_Y + (CHUNK_SIZE_Z * WALL_HEIGHT)
        new_ceil_chunk.parent = base_ceiling

# Z Walls
for h in range(WALL_HEIGHT):
    for w in range(Z_WALL_LENGTH):
        new_zwall_chunk = Entity(model='cube', scale=(CHUNK_SIZE_Z, CHUNK_SIZE_Z, 1))
        new_zwall_chunk.x = w * CHUNK_SIZE_Z + FLOOR_POSITION[0] - 5
        new_zwall_chunk.z = FLOOR_POSITION[2] - CHUNK_SIZE_Z / 2
        new_zwall_chunk.y = CHUNK_SIZE_Z * h + FLOOR_POSITION[1] + CHUNK_SIZE_Z / 2
        new_zwall_chunk.parent = base_wall_z1

        new_zwall_chunk2 = Entity(model='cube', scale=(CHUNK_SIZE_Z, CHUNK_SIZE_Z, 1))
        new_zwall_chunk2.x = w * CHUNK_SIZE_Z + FLOOR_POSITION[0] - 5
        new_zwall_chunk2.z = FLOOR_POSITION[2] + (FLOOR_LENGTH * CHUNK_SIZE_Z) - CHUNK_SIZE_Z / 2 - 4
        new_zwall_chunk2.y = CHUNK_SIZE_Z * h + FLOOR_POSITION[1] + CHUNK_SIZE_Z / 2
        new_zwall_chunk2.parent = base_wall_z2

# X Walls
for h in range(WALL_HEIGHT):
    for w in range(X_WALL_LENGTH):
        new_xwall_chunk = Entity(model='cube', scale=(1, CHUNK_SIZE_Z, CHUNK_SIZE_Z))
        new_xwall_chunk.x = FLOOR_POSITION[0] - CHUNK_SIZE_Z / 2 - 2
        new_xwall_chunk.z = w * CHUNK_SIZE_Z + FLOOR_POSITION[2]
        new_xwall_chunk.y = CHUNK_SIZE_Z * h + FLOOR_POSITION[1] + CHUNK_SIZE_Z / 2
        new_xwall_chunk.parent = base_wall_x1

        new_xwall_chunk2 = Entity(model='cube', scale=(1, CHUNK_SIZE_Z, CHUNK_SIZE_Z))
        new_xwall_chunk2.x = FLOOR_POSITION[0] + (FLOOR_WIDTH * CHUNK_SIZE_X) - CHUNK_SIZE_X / 2 - 6
        new_xwall_chunk2.z = w * CHUNK_SIZE_Z + FLOOR_POSITION[2]
        new_xwall_chunk2.y = CHUNK_SIZE_Z * h + FLOOR_POSITION[1] + CHUNK_SIZE_Z / 2
        new_xwall_chunk2.parent = base_wall_x2


base_floor.combine()
base_floor.collider = 'mesh'

base_ceiling.combine()
base_ceiling.collider = 'mesh'

base_wall_z1.combine()
base_wall_z1.collider = 'mesh'

base_wall_z2.combine()
base_wall_z2.collider = 'mesh'

base_wall_x1.combine()
base_wall_x1.collider = 'mesh'

base_wall_x2.combine()
base_wall_x2.collider = 'mesh'

# taps, tap holder can be used to refernce all taps
tap_holder = Entity()
tap1 = Tap()
tap2 = Tap()
tap3 = Tap()

tap1.parent = tap_holder
tap2.parent = tap_holder
tap3.parent = tap_holder

# positions taps for map
for tap in tap_holder.children:
    tap.rotation_y = 180
    tap.y = 1
    tap.z = 1.7

tap2.x = 20
tap3.x = 40

# tables customers move along and mugs spawn on

table1 = Table(size=7, position=(0, 0, 10))
table2 = Table(size=7, position=(20, 0, 10))
table3 = Table(size=7, position=(40, 0, 10))

# doorway customers enter from
Doorway(position=(1.3, 0, 35.3))
Doorway(position=(21.3, 0, 35.3))
Doorway(position=(41.3, 0, 35.3))

moose_head = Entity(model="3D Models/Decor/head/head/moose head.obj", texture="3D Models/Decor/head/head/texture.png",
                    scale=3, position=(47, 5, 17), rotation=(0, 90, 0))

sign = Entity(model="3D Models/Decor/sign/Sign.obj", texture="3D Models/Decor/sign/texture.png", scale=5,
              position=(21.3, 4.5, 37.5))
