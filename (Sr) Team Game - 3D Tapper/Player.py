# stores all classes/functions pertaining to the player and inventory (includes display mug)

from ursina import Entity, camera, color,\
    mouse, Vec2, Vec3, raycast, held_keys, time, curve, invoke, FrameAnimation3d, Animator, Text, Sprite, clamp


# modified first person controller from prefabs
import End_menu


class FirstPersonController(Entity):
    def __init__(self, inventory, **kwargs):
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.pink, scale=.008, rotation_z=45)

        Text.size = .04
        Text.default_resolution = 1080 * Text.size

        # score
        self.old_score = 0
        self.score = 0
        self.scoretext = Text(text=self.score, font='other/OldePixel.ttf', color=color.rgb(210,180,140),
                              x=-0.75, y=0.3)
        self.rootbeericon = Sprite("Sprites n GUI/root beer.png", parent=camera.ui, scale=.047, x=-.8, y=.28)

        # lives
        self.old_lives = 3
        self.lives = 3
        self.livestext = Text(text=self.lives, font='other/OldePixel.ttf', color=color.rgb(255,51,51),
                              x=-0.75, y=0.42)
        self.hearticon = Sprite("Sprites n GUI/full.png", parent=camera.ui, x=-.8, y=.4, scale=.7)

        super().__init__()
        self.collider = 'box'
        self.inventory = inventory
        self.speed = 5
        self.height = 2.5
        self.camera_pivot = Entity(parent=self, y=self.height)

        camera.parent = self.camera_pivot
        camera.position = (0,0,0)
        camera.rotation = (0,0,0)
        camera.fov = 90
        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 1
        self.grounded = False
        self.air_time = 0

        self.dashing = False
        self.x_dash = 0
        self.dash_distance = 5
        self.dash_duration = .2
        self.dash_cooldown = .8

        self.controls = ["WASD", "Arrow Keys"]
        self.control_num = 0

        for key, value in kwargs.items():
            setattr(self, key ,value)

        # make sure we don't fall through the ground if we start inside it
        if self.gravity:
            ray = raycast(self.world_position+(0,self.height,0), self.down, ignore=(self,))
            if ray.hit:
                self.y = ray.world_point.y

    def update(self):
        # display new score value
        if self.old_score != self.score:
            self.scoretext.text = self.score
            self.scoretext.appear(speed=0, delay=0)
        self.old_score = self.score


        # display new life count
        if self.old_lives != self.lives:
            self.livestext.text = self.lives
            self.scoretext.appear(speed=0, delay=0)
        self.old_lives = self.lives

        if self.lives > 1:
            End_menu

        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]

        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -90, 90)

        if self.controls[self.control_num] == "WASD":
            self.direction = Vec3(
                self.forward * (held_keys['w'] - held_keys['s'])
                + self.right * (held_keys['d'] - held_keys['a'])
                ).normalized()

        if self.controls[self.control_num] == "Arrow Keys":
            self.direction = Vec3(
                self.forward * (held_keys['up arrow'] - held_keys['down arrow'])
                + self.right * (held_keys['right arrow'] - held_keys['left arrow'])
                ).normalized()

        # adds dash velocity
        self.direction += Vec3(self.forward * self.x_dash)

        feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, ignore=(self,), distance=1, debug=False)
        head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, ignore=(self,), distance=1, debug=False)
        if not feet_ray.hit and not head_ray.hit:
            move_amount = self.direction * time.dt * self.speed

            if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, ignore=(self,)).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, ignore=(self,)).hit:
                move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, ignore=(self,)).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, ignore=(self,)).hit:
                move_amount[2] = max(move_amount[2], 0)
            self.position += move_amount
        else:
            self.end_dash()
            self.end_dash_movement()
            # self.position += self.direction * self.speed * time.dt

        if self.gravity:
            # gravity
            ray = raycast(self.world_position+(0,self.height,0), self.down, ignore=(self,))
            # ray = boxcast(self.world_position+(0,2,0), self.down, ignore=(self,))

            if ray.distance <= self.height+.1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                # make sure it's not a wall and that the point is not too far up
                if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
                    self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            # if not on ground and not on way up in jump, fall
            self.y -= min(self.air_time, ray.distance-.05) * time.dt * 100
            self.air_time += time.dt * .25 * self.gravity

    def input(self, key):
        if self.controls[self.control_num] == "WASD":
            if key == 'space':
                self.dash()

        if self.controls[self.control_num] == "Arrow Keys":
            if key == "control":
                self.dash()

    def start_fall(self):
        self.y_animator.pause()

    def dash(self):
        if self.dashing:
            return

        self.dashing = True

        self.x_dash = self.dash_distance

        invoke(self.end_dash_movement, delay=self.dash_duration)

    def end_dash_movement(self):
        self.x_dash = 0

        invoke(self.end_dash, delay=self.dash_cooldown)

    def end_dash(self):
        self.dashing = False

    def view_bobbing(self):
        camera.animate_y()

    def land(self):
        # print('land')
        self.air_time = 0
        self.grounded = True


    def on_enable(self):
        mouse.locked = True
        self.cursor.enabled = True


    def on_disable(self):
        mouse.locked = False
        self.cursor.enabled = False


# inventory (determines display mug state)
class Inventory:
    def __init__(self):
        self.mug = 0
        self.mug_fill_time = 1

    def delete_mug(self):
        self.mug = 0

    def empty_mug(self):
        self.mug = 1

    def fill_mug(self):
        if self.mug == 1:
            self.mug = 2
            invoke(self.full_mug, delay=self.mug_fill_time)

    def full_mug(self):
        if self.mug == 2:
            self.mug = 3


# updates mug model based on inventory value
class MugCon(Animator):
    def __init__(self, parent, inventory):
        # used when no mug is held
        self.no_mug = Entity(model="3D Models/othermug/mug.obj", texture="3d Models/othermug/mugtexture.png",
                             z=1.5, x=.9, y=1.2, rotation=(0, 150, 0), scale=4, parent=parent, enabled=False,
                             visible=False)
        # used when empty mug is held
        self.empty_mug = Entity(model="3D Models/othermug/mug.obj", texture="3d Models/othermug/mugtexture.png",
                                z=1.5, x=.9, y=1.2, rotation=(0, 150, 0), scale=4, parent=parent)
        # used when mug is being filled
        self.filling_mug = FrameAnimation3d("3D Models/mug/mug_fill_anim/mug_", z=1.5, x=.9, y=1.2, rotation=(0, 150, 0),
                                            parent=parent, texture="3D Models/mug/mug_fill_anim/texture_02.png",
                                            fps=17, autoplay=True, loop=False, enabled=False)
        # used when mug is full
        self.full_mug = Entity(model="3D Models/mug/mug_fill_anim/mug_10.obj", texture="3d Models/mug/mug_fill_anim/texture_02.png",
                               z=1.5, x=.9, y=1.2, rotation=(0, 150, 0), scale=1, parent=parent)

        self.inventory = inventory

        super().__init__(animations={
            "none": self.no_mug,
            "empty": self.empty_mug,
            "filling": self.filling_mug,
            "full": self.full_mug
        })
        self.start_state = "none"

    def update(self):
        if self.inventory.mug == 0:
            self.clear()
        if self.inventory.mug == 1:
            self.empty()
        if self.inventory.mug == 2:
            self.fill()
        if self.inventory.mug == 3:
            self.full()

    def empty(self):
        self.state = "empty"

    def clear(self):
        self.state = "none"

    def fill(self):
        self.state = "filling"

    def full(self):
        self.state = "full"
