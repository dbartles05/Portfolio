import ursina
from ursina import Entity, Sprite, Text,\
Button, camera, color, ButtonList, Func, rgb, Audio

title_font = "other/OldePixel.ttf"
button_font = "other/OldePixel.ttf"
info_font = "other/OldePixel.ttf"



class MenuMenu(Entity):
    def __init__(self, start_fun, **kwargs):
        super().__init__(parent=camera.ui, ignore_paused=True)
        self.main_menu = Entity(parent=self, enabled=True)
        self.help_menu = Entity(parent=self, enabled=False)
        self.options_menu = Entity(parent=self, enabled=False)
        self.controls_menu = Entity(parent=self, enabled=False)
        self.background = Sprite('shore', x=1, z=1, color = color.black)
        self.start = False

        txt1 = Text("3D   Tapper", scale=5.2, font=title_font, parent=self.main_menu, color = color.white, y=0.3, x=0, origin=(0,0), resolution=1080*Text.size)

        rootbeer1 = Sprite("Sprites n GUI/root beer flipped.png", scale=0.1, parent=self.main_menu, y=-0.2, x=0.6)
        rootbeer1.rotation_z += 30

        rootbeer2 = Sprite("Sprites n GUI/root beer.png", scale=0.1, parent=self.main_menu, y=0.1, x=-0.7)
        rootbeer2.rotation_z -= 30

        def switch(menu1, menu2):
            menu1.enable()
            menu2.disable()

        ButtonList(button_dict={
            "Insert    Coin": start_fun,
            "Help": Func(lambda: switch(self.help_menu, self.main_menu)),
            "Controls": Func(lambda: switch(self.controls_menu, self.main_menu)),
            "Credits": Func(lambda: switch(self.options_menu, self.main_menu)),
            "Exit": Func(lambda: application.quit())
        },y=0,parent=self.main_menu, font=button_font, scale = 1.3, x = -.4, resolution=1080*Text.size)

        Text("Credits: ", parent=self.options_menu, scale=2.0, font=info_font, y=0.4, x=0, origin=(0, 0))
        Text("Corey  Verkouteren   (Project   Manager)", font=info_font, parent=self.options_menu, y=0.4, x=0, origin=(0, 5))
        Text("Kaydaince  Lawson   (Design)", font=info_font, parent=self.options_menu, y=0.4, x=0, origin=(0, 9))
        Text("Jonathan  Carter   (Design,   Developer)", font=info_font, parent=self.options_menu, y=0.4, x=0, origin=(0, 13))
        Text("Dalton  Ison   (Developer)", font=info_font, parent=self.options_menu, y=0.4, x=0, origin=(0, 17))
        Text("Dustyn  Bartles   (Developer)", font=info_font, parent=self.options_menu, y=0.4, x=0, origin=(0, 21))
        Text("Game   Created   at   James   Rumsey   Technical   Institute", font=info_font, parent=self.options_menu, y=0.4, x=0, origin=(0, 27))


        heart1 = Sprite("Sprites n GUI/full.png", scale=1.1, parent=self.options_menu, y=0.3, x=0.6)
        heart1.rotation_z += 25

        heart2 = Sprite("Sprites n GUI/full.png", scale=1.1, parent=self.options_menu, y=-0.1, x=-0.7)
        heart2.rotation_z -= 25


        Button("Back",parent=self.options_menu, font=button_font, y=-0.4,scale=(0.1,0.05),color=rgb(50,50,50),
               on_click=lambda: switch(self.main_menu, self.options_menu))


        Text("How   to   Play: ", font=info_font, parent=self.help_menu, scale=2.0, y=0.4, x=0, origin=(0, 0))
        Text("Customers   will   spawn   randomly   at   one   of   the   three   lanes   ", font=info_font, parent=self.help_menu, y=0.4, x=0, origin=(0, 6))
        Text("Your   Job   is   to   serve   drinks   to   the   demanding   customers   before   "
              "they   get   to   the   end   of   the   lane", font=info_font, parent=self.help_menu, y=0.4, x=0, origin=(0, 12))
        Text("If   they   get   to   the   end   of   the   lane   without   a   drink   you   will   lose   a   life", font=info_font, parent=self.help_menu, y=0.4, x=0, origin=(0, 18))
        Text("You   get   3   lives,   each   drink   served   is   100   points,   Good   Luck!", font=info_font, parent=self.help_menu, y=0.4, x=0, origin=(0, 24))


        Button("Back", parent=self.help_menu, font=button_font, y=-0.4, scale=(0.1, 0.05), color=rgb(50, 50, 50),
               on_click=lambda: switch(self.main_menu, self.help_menu))


        Text ("Controls: ", parent=self.controls_menu, font=info_font, scale=2.0, y=0.4, x=0, origin=(0, 0))
        Text("WASD   Movement: ", parent=self.controls_menu, font=info_font, y=0.4, x=0, origin=(1.8, 10))
        Text("Arrow   Key   Movement: ", parent=self.controls_menu, font=info_font, y=0.4, x=0, origin=(-1.4, 10))
        Text("(Press   C   to   Switch   Between   Both   Movements)", parent=self.controls_menu, font=info_font, y=0.4, x=0, origin=(0, 5))
        Text("General   Controls: ", parent=self.controls_menu, font=info_font, y=0.4, x=0, origin=(0, 20))
        Text("Hold   Left   Click   at   Tap   to   Fill   Up   Mug", font=info_font, parent=self.controls_menu, y=0.4, x=0, origin=(0, 24))
        Text("Right   Click   at   Lane   to   Send   Mug   to   Customer", font=info_font, parent=self.controls_menu, y=0.4, x=0, origin=(0, 28))
        Text("WASD   to   move   around",  font=info_font,parent=self.controls_menu, y=0.4, x=0, origin=(1.4, 15))
        Text("Space   to   Dash",  font=info_font, parent=self.controls_menu, y=0.4, x=0, origin=(2.3, 20))
        Text("Arrow   Keys   to   move   around", font=info_font, parent=self.controls_menu, y=0.4, x=0, origin=(-1.1, 15))
        Text("Ctrl   to   Dash", font=info_font, parent=self.controls_menu, y=0.4, x=0, origin=(-2.6, 20))


        Button("Back",parent=self.controls_menu, font=button_font, y=-0.4,scale=(0.1,0.05),color=rgb(50,50,50),
               on_click=lambda: switch(self.main_menu, self.controls_menu))


        for key, value in kwargs.items ():
            setattr (self, key, value)

    def input(self, key):
        if self.main_menu.enabled and key == "escape":
                application.quit()
        elif self.options_menu.enabled and key == "escape":
            self.main_menu.enable()
            self.options_menu.disable()
        elif self.controls_menu.enabled and key == "escape":
            self.main_menu.enable()
            self.controls_menu.disable()

    def update(self):
        pass

    def stop(self):
        self.background.enabled = False
        self.enabled = False

