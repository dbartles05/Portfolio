from ursina import Ursina, application
from Main_menu import MenuMenu
from Main_Game import MainGame
from End_menu import DeathMenu


def start():
    menu.stop()
    game = MainGame(end_fun=gameover)


def gameover(score):
    end_menu = DeathMenu(score)


app = Ursina(title='Main Menu')

menu = MenuMenu(start_fun=start, application=application)

app.run()
