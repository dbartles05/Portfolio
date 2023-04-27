# used to store entity classes used in the world

from random import choice
from ursina import Entity, invoke, Text, destroy, Animator, FrameAnimation3d, color

# text used in entity tooltips
Text.default_resolution = 1080 * Text.size


# tap to get root beer from
class Tap(Entity):
    def __init__(self):
        # sets up basic attributes
        super().__init__(
            model="3D Models/tap/tap.obj",
            texture="3D Models/tap/texture.png",
            collider='mesh',
            scale=.5,
        )
        self.tooltip = Text(text='Hold Left Click To Fill', wordwrap=30, enabled=False)


# creates a full table
class Table(Entity):
    def __init__(self, size=3, position=(0, 0, 0), parent=None):
        super().__init__(parent=parent)

        self.tooltip = Text(text='Right Click To Send Drink', wordwrap=30, enabled=False)

        for i in range(size):
            # spawns the end of the table
            if i == 0:
                Entity(model="3D Models/tableend/tableend.obj", texture="3D Models/tableend/texture.png",
                       collider='box', parent=self, y=(.6 + position[1]), z=position[2], x=position[0],
                       scale=(.7, .9, 1))
            # spawns in all subsequent pieces of the table
            else:
                Entity(model="3D Models/tablemid/tablemid.obj", texture="3D Models/tablemid/texture.png",
                       collider='box', parent=self, y=(.6 + position[1]), z=((4.1*i) + position[2]), x=position[0],
                       scale=(.7, .9, 1))


class Doorway(Entity):
    def __init__(self, position):
        super().__init__(model="3D Models/door/Door.obj", texture="3D Models/door/texture.png", position=position,
                         rotation=(0, 180, 0))


class Customer(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(position=position, model='cube', scale=2, visible_self=False)
        self.choices = ["F1"]
        self.customer = choice(self.choices)

        self.display_model = CustomerAnimator(self, self.customer)
        # hand is used to detect a mug
        self.hand = Entity(model='cube', parent=self, scale=(1.1, 1, 1), collider='box', visible_self=False)
        self.hand.x -= 1.5
        self.hand.y += 1.3

        self.direction = 1

        # display model stuff
        self.drinking = False
        self.angry = False
        self.drink_time = 1

    def update(self):
        # moves toward end of table
        self.z -= .05 * self.direction

        # display model updates
        if self.angry:
            self.display_model.state = "mad"
        elif self.direction == 0 and not self.drinking:
            self.display_model.state = "idle"
        elif self.direction == 0 and self.drinking:
            self.display_model.state = "drink"
        elif self.direction == 1:
            self.display_model.state = "walk forward"
        elif self.direction == -1:
            self.display_model.state = "walk backward"

    def turn_around(self):
        if self.direction == 0:
            self.direction = 1
            self.drinking = False
        self.direction *= -1

    def walk_forward(self):
        self.direction = 1
        self.drinking = False

    def walk_backward(self):
        self.direction = -1
        self.drinking = False

    def idle(self):
        self.direction = 0
        self.drinking = False

    def drink(self):
        self.direction = 0
        self.drinking = True
        invoke(self.walk_backward, delay=self.drink_time)

    def mad(self):
        self.direction = 0
        self.angry = True
        destroy(self, 1)


class CustomerAnimator(Animator):
    def __init__(self, parent, skin):
        cust_path = f"3D Models/customers/{skin}/"
        walk = cust_path + "walk/cust_"
        mad = cust_path + "mad/cust_"
        drink = cust_path + "drink/dri_"
        texture = cust_path + "texture.png"
        mad_texture = cust_path + "mad/texture.png"
        drink_texture = cust_path + "drink/texture.png"

        self.idle = Entity(model='cube', scale=(1, 1, 1), parent=parent)
        self.walk_forward = FrameAnimation3d(walk, texture=texture, scale=(1, 1, 1), parent=parent, loop=True)
        self.walk_backward = FrameAnimation3d(walk, texture=texture, scale=(1, 1, 1), parent=parent, loop=True, rotation=(0, 180, 0))
        self.drink = FrameAnimation3d(drink, texture=drink_texture, scale=(1, 1, 1), parent=parent, loop=True)
        self.mad = FrameAnimation3d(mad, texture=mad_texture, scale=(1, 1, 1), parent=parent, loop=True)

        super().__init__(animations={
            "idle": self.idle,
            "walk forward": self.walk_forward,
            "walk backward": self.walk_backward,
            "drink": self.drink,
            "mad": self.mad
        })

        self.state = "walk forward"


# sent mug entities
class TableMug(Entity):
    def __init__(self, position):
        super().__init__(model="3D Models/mug/mug_fill_anim/mug_10.obj", texture="3d Models/mug/mug_fill_anim/texture_02.png", scale=1,
                         position=position, rotation=(0, 180, 0), collider='box')

    def update(self):
        # moves toward customer spawn at tables
        self.z += .3


# handles mug-customer collisions and deletions
class MugCustomerHandler:
    def __init__(self, mugs, customers, player):
        # lists of sent mugs and customers
        self.mugs = mugs
        self.customers = customers
        self.player = player

    def update(self):
        # prevents customers from moving past the table
        for customer in self.customers:
            if customer.z <= 10:
                customer.mad()
                self.customers.remove(customer)
                self.player.lives -= 1

        for customer in self.customers:
            if customer.z > 40:
                self.customers.remove(customer)
                destroy(customer)

        # prevents mugs from moving past the table
        for mug in self.mugs:
            if mug.z >= 40:
                destroy(mug)
                self.mugs.remove(mug)

        for mug in self.mugs:
            # gets entities intersecting the mugs
            mug_collider = mug.intersects()
            ent_collide = mug_collider.entity

            # kills mug and customer if they collide
            for customer in self.customers:
                if ent_collide == customer.hand and ent_collide.parent.direction == 1:
                    self.player.score += 100
                    self.mugs.remove(mug)
                    destroy(mug)
                    ent_collide.parent.drink()


class TooltipHandler:
    def __init__(self, tables, taps):
        self.tables = tables
        self.taps = taps

    def update(self):
        for t in self.tables:
            hover_list = []
            for e in t.children:
                hover_list.append(e.hovered)
            if True in hover_list and not t.tooltip.enabled:
                t.tooltip.enabled = True
            elif True not in hover_list and t.tooltip.enabled:
                t.tooltip.enabled = False

        for t in self.taps.children:
            if t.hovered:
                t.tooltip.enabled = True
            elif not t.hovered and t.tooltip.enabled:
                t.tooltip.enabled = False
