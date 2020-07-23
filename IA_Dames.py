__author__ = 'Ariane Fiset et Pascal de Le Rue'

from random import randint
from interface_dames import FenetrePartie
from tkinter import Event
from position import Position

class IA_dames():

    def __init__(self):

        self.interface = FenetrePartie()
        self.position_1 = -1
        self.position_2 = -1

    def jouer_contre_IA(self):

        if self.interface.partie.couleur_joueur_courant == 'blanc':
            self.interface.selectionner(Event)

        else:
            if self.interface.partie.damier.piece_de_couleur_peut_faire_une_prise('noir'):
                for position_a in self.interface.partie.damier.cases:
                    piece = self.interface.partie.damier.recuperer_piece_a_position(position_a)
                    if piece.couleur == 'noir':
                        if position_a.piece_peut_faire_une_prise():
                            for position_b in Position.quatre_positions_sauts(position_a):
                                if position_a.position_cible_valide(position_b)[0]:
                                    self.interface.partie.damier.deplacer(position_a, position_b)
                                    return
            else:

                while not Position(self.position_1) in self.interface.partie.damier.cases:
                    self.position_1 = (randint(0, 7), randint(0, 7))
