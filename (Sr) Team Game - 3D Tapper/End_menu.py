from ursina import Entity, invoke, scene, camera, Text, Sprite
import time
title_font = "other/OldePixel.ttf"
button_font = "other/OldePixel.ttf"
info_font = "other/OldePixel.ttf"


class DeathMenu(Entity):
    def __init__(self, score):
        super().__init__(parent=camera.ui, ignore_paused=True)

        Text(text="You   Lost!", font='other/OldePixel.ttf', x=-0.13, y=0.25)
        Text(text=f"Your                       Score   was   {score}", font='other/OldePixel.ttf',  x=-0.31, y=0.12)
        Sprite("Sprites n GUI/root beer.png", parent=camera.ui, scale=.047, x=-.10, y=.10)

