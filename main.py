from croque_marmotte import CroqueLaitue
from renderer import Renderer

nb_player = -1
nb_sqares = -1

while nb_player <= 0:
    inputed = input("How many players ?\n")

    try:
        nb_player = int(inputed)

    except BaseException:
        nb_player = -1
        print("There was an error, pls enter a new value")

while nb_squares <= 0:
    inputed = input("How many squares ?\n")

    try:
        nb_squares = int(inputed)
        
    except BaseException:
        nb_squares = -1
        print("There was an error, pls enter a new value")

jeu = CroqueLaitue(nb_player, nb_squares)
jeu.play_game()