from croque_marmotte import CroqueLaitue
from renderer import Renderer

nb_player = int(input("How many players ?\n"))
nb_squares = int(input("How many squares ?\n"))
jeu = CroqueLaitue(nb_player, nb_squares)
jeu.play_game()