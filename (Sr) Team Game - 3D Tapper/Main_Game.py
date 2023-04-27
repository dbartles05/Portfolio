# 3D Root-Beer Tapper
# this file is currently being used to handle all base game needs, and the entire game,
# it should be made into a separate file at some point to enable menu support


from ursina import Ursina, window, Entity, EditorCamera, mouse, application, Vec3, held_keys, raycast, camera, destroy, \
    invoke, Audio, scene
from Player import FirstPersonController, Inventory, MugCon
from random import choice
from World_Objects import Customer, TableMug, MugCustomerHandler, TooltipHandler


class MainGame(Entity):
    def __init__(self, end_fun, **kwargs):
        super().__init__()
        self.end_fun = end_fun

        Entity.default_shader = None

        # world stuff
        from World import base_floor, FLOOR_TEXTURE, tap_holder, table1, table2, table3, WALL_TEXTURE, base_walls, \
            base_ceiling, CEILING_TEXTURE

        self.tap_holder = tap_holder
        # bar tables which customers move along and mugs spawn on
        self.tables = [table1, table2, table3]

        # setting floor texture
        base_floor.texture = FLOOR_TEXTURE

        base_ceiling.texture = CEILING_TEXTURE

        # set wall texture
        for b in base_walls:
            b.texture = WALL_TEXTURE

        # player stuff
        self.p_inventory = Inventory()

        # player
        self.player = FirstPersonController(inventory=self.p_inventory, model='cube', y=5, x=5, origin_y=-.5, speed=10)

        # display mug
        self.p_mug = MugCon(self.player, self.p_inventory)

        # editor cam, used on spawn (depricated)
        self.editor_camera = EditorCamera(enabled=False, ignore_paused=True)

        # other stuff
        # holds sent mugs, given to mug-customer handler
        self.cur_mugs = []
        # holds customers, given to mug-customer handler
        self.cur_customers = []

        # handles mug-customer collisions and deletion
        self.mug_cust_collisions = MugCustomerHandler(self.cur_mugs, self.cur_customers, self.player)
        # handles tooltips for tables and taps
        self.tooltip_checker = TooltipHandler(self.tables, tap_holder)

        # SOUNDS (wont work when in another file)

        self.drink_sound = Audio("Sounds/drink.mp3", autoplay=False)
        self.mug_fill_sound = Audio("Sounds/pouring_1.mp3", autoplay=False, volume=2)
        self.bg_music = Audio("Sounds/bg-song.mp3", autoplay=True, loops=10000000)
        self.dash_sound = Audio("Sounds/dash.mp3", autoplay=False, volume=2)

        # begins a recurring event (spawning customers in)
        class SpawnCustomer(Entity):
            def __init__(self, cur_cust, event_start_delay=5, event_delay=4):
                super().__init__()
                self.event_start_delay = event_start_delay
                self.event_delay = event_delay
                self.spawn_list = [(3, .4, 40), (23, .4, 40), (43, .4, 40)]
                self.cur_customers = cur_cust

            def start_event(self):
                if self.enabled:
                    invoke(self.execute_event, delay=self.event_start_delay)

            def event_cooldown(self):
                if self.enabled:
                    invoke(self.execute_event, delay=self.event_delay)

            def execute_event(self):
                if self.enabled:
                    g = Customer(choice(self.spawn_list))
                    self.cur_customers.append(g)
                    invoke(self.event_cooldown, delay=0)

        # start spawner
        self.c_spawner = SpawnCustomer(self.cur_customers)
        self.c_spawner.start_event()

        for key, value in kwargs.items():
            setattr(self, key, value)

    # handle inputs (l click in updates)
    def input(self, key):
        # FINAL INPUTS
        if key == 'escape':
            quit()

        # sends mug down table if right clicked on
        if key == "right mouse down":
            table_ray = raycast(camera.world_position, camera.forward, distance=5)
            table = table_ray.entity
            try:
                if self.p_inventory.mug == 3 and table.parent in self.tables:
                    sent_mug = TableMug(position=(table.x, (table.y + 1.2), table.z))
                    self.cur_mugs.append(sent_mug)
                    self.p_inventory.delete_mug()
            except:
                pass

        # plays dash sound if player dashes
        if key == "space" and not self.player.dashing:
            self.dash_sound.play()

        # switches controls
        if key == "c":
            self.player.control_num = (self.player.control_num + 1) % len(self.player.controls)

        # DEV INPUTS
        if key == "y":
            scene.clear()
        if key == "p":
            for c in self.cur_customers:
                c.turn_around()
        if key == "o":
            for c in self.cur_customers:
                c.drink()
        if key == "i":
            for c in self.cur_customers:
                c.idle()
        if key == "u":
            for c in self.cur_customers:
                c.walk_forward()
        # sound tests
        if key == "l":
            self.stop()

    # updates for each frame (i think)
    def update(self):
        try:
            # updated display mug
            self.p_mug.update()
            # updates collisions between sent mugs and customers
            self.mug_cust_collisions.update()
            # updates table and tap tooltips (not in object updates in case we want to add distance to them)
            self.tooltip_checker.update()

            # filling display mug with tap interaction
            # left click input use
            tap_ray = raycast(camera.world_position, camera.forward, distance=6, traverse_target=self.tap_holder)
            if mouse.left and tap_ray.hit:
                if self.p_inventory.mug == 0:
                    self.p_inventory.empty_mug()
                if not self.mug_fill_sound.status == 2:
                    self.mug_fill_sound.play()
                self.p_inventory.fill_mug()
            elif (not mouse.left or not tap_ray.hit) and self.p_inventory.mug == 2:
                self.p_mug.filling_mug.current_frame = 0
                if self.mug_fill_sound.status == 2:
                    self.mug_fill_sound.stop(destroy=True)
                self.p_inventory.delete_mug()
            if self.p_inventory.mug == 3 and self.mug_fill_sound.status == 2:
                self.mug_fill_sound.stop()
        except:
            pass

    def stop(self):
        self.enabled = False
        disable_list = []
        for i in scene.entities:
            disable_list.append(i)
        disable_list.reverse()
        for i in range(20):
            disable_list.pop()
        for i in disable_list:
            i.enabled = False
        self.end_fun(self.player.score)
