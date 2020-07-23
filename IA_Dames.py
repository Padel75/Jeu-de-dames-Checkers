__author__ = 'Ariane Fiset et Pascal de Le Rue'

from random import randint
from interface_dames import FenetrePartie
from tkinter import Event
from position import Position

class IA_dames(FenetrePartie):

    def __init__(self):

        super().__init__()

        self.position_1 = -1
        self.position_2 = -1

    def jouer_contre_IA(self):

        if self.partie.couleur_joueur_courant == 'blanc':
            self.selectionner(Event)

        else:
            if self.partie.damier.piece_de_couleur_peut_faire_une_prise('noir'):
                for position_a in self.partie.damier.cases:
                    piece = self.partie.damier.recuperer_piece_a_position(position_a)
                    if piece.couleur == 'noir':
                        if position_a.piece_peut_faire_une_prise():
                            for position_b in Position.quatre_positions_sauts(position_a):
                                if position_a.position_cible_valide(position_b)[0]:
                                    self.partie.damier.deplacer(position_a, position_b)
                                    return
            else:

                while not Position(self.position_1) in self.partie.damier.cases and \
                self.partie.damier.recuperer_piece_a_position(Position(self.position_1).couleur != 'noir'):
                    self.position_1 = (randint(0, 7), randint(0, 7))
                    break

                for pos in Position(self.position_1).quatre_positions_diagonales():
                    if Position(self.position_1).position_cible_valide(pos)[0]:
                        self.partie.damier.deplacer(self.position_1, pos)
                        return

if __name__ == 'main':
    ia = IA_dames()
    ia.mainloop()