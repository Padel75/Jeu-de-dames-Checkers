__author__ = 'Ariane Fiset et Pascal de Le Rue'

from random import randint
from interface_dames import FenetrePartie
from tkinter import Event
from position import Position

class IA_dames(FenetrePartie):

    def __init__(self):

        super().__init__()

        self.position_1 = -1, -1
        self.position_2 = -2, -2

    def jouer_contre_IA(self, event):

        if self.partie.couleur_joueur_courant == 'blanc':
            if self.bool_piece_selectionnee:

                # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
                ligne_deplacement = event.y//self.canvas_damier.n_pixels_par_case
                colonne_deplacement = event.x//self.canvas_damier.n_pixels_par_case

                if self.partie.position_cible_valide(Position(ligne_deplacement, colonne_deplacement))[0]:
                    self.position_cible_graphique = Position(ligne_deplacement, colonne_deplacement)

                else:
                    self.messages['foreground'] = 'black'
                    self.messages['text'] = self.partie.position_cible_valide(Position(ligne_deplacement, colonne_deplacement))[1]

                self.partie.couple_de_position = self.position_selectionnee, self.position_cible_graphique
                self.partie.tour()

                # On affiche le damier mis a jour.
                self.canvas_damier.actualiser()

                couleur = str(self.partie.couleur_joueur_courant)
                self.couleur_joueur['text'] = 'Tour du joueur {}'.format(couleur)

                # Réinitialisation des attributs
                self.bool_piece_selectionnee = False
                self.piece_selectionnee = None
                self.position_selectionnee = None
                self.partie.position_source_selectionnee = None
                return


            if not self.bool_piece_selectionnee:

                # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
                ligne = event.y // self.canvas_damier.n_pixels_par_case
                colonne = event.x // self.canvas_damier.n_pixels_par_case

                if self.partie.position_source_valide(Position(ligne, colonne))[0]:
                    if self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.partie.couleur_joueur_courant):
                        if self.partie.damier.piece_peut_faire_une_prise(Position(ligne, colonne)):
                            if self.partie.position_source_forcee is not None\
                                    and self.partie.position_source_forcee == Position(ligne, colonne):
                                self.position_selectionnee = Position(ligne, colonne)
                                self.partie.position_source_selectionnee = self.position_selectionnee
                            elif self.partie.position_source_forcee is None:
                                self.position_selectionnee = Position(ligne, colonne)
                                self.partie.position_source_selectionnee = self.position_selectionnee
                            else:
                                self.messages['foreground'] = 'red'
                                self.messages['text'] = 'Erreur: Vous devez sélectionner la piece {}'\
                                    .format(str(self.partie.position_source_forcee))
                                return
                        else:
                            self.messages['foreground'] = 'red'
                            self.messages['text'] = 'Erreur: Vous devez sélectionner une pièce pouvant faire une prise.'
                    else:
                        self.position_selectionnee = Position(ligne, colonne)
                        self.partie.position_source_selectionnee = self.position_selectionnee

                    # On récupère l'information sur la pièce à l'endroit choisi.
                    self.piece_selectionnee = self.partie.damier.recuperer_piece_a_position(self.position_selectionnee)

                    if self.piece_selectionnee is None:
                        self.messages['foreground'] = 'red'
                        self.messages['text'] = 'Erreur: Aucune pièce à cet endroit.'
                    else:
                        self.messages['foreground'] = 'black'
                        self.messages['text'] = 'Pièce sélectionnée à la position {}.'.format(self.position_selectionnee)
                        self.bool_piece_selectionnee = True

                else:
                    print(self.partie.position_source_valide(Position(ligne, colonne))[1])
                    self.messages['foreground'] = 'black'
                    self.messages['text'] = self.partie.position_source_valide(Position(ligne, colonne))[1]
                    return

                # On affiche le damier mis a jour.
                self.canvas_damier.actualiser()


        else:
            if self.partie.damier.piece_de_couleur_peut_faire_une_prise('noir'):
                for position_a in self.partie.damier.cases:
                    piece = self.partie.damier.recuperer_piece_a_position(position_a)
                    if piece.couleur == 'noir':
                        if position_a.piece_peut_faire_une_prise():
                            for position_b in Position.quatre_positions_sauts(position_a):
                                if position_a.position_cible_valide(position_b)[0]:
                                    self.partie.couple_de_position = position_a, position_b
            else:
                while not Position(self.position_1) in self.partie.damier.cases and self.partie.damier.recuperer_piece_a_position(Position(self.position_1)).couleur == 'noir':
                    self.position_1 = (randint(0, 7), randint(0, 7))

                for pos in Position(self.position_1).quatre_positions_diagonales():
                    if self.partie.position_cible_valide(Position(pos))[0]:

                        self.position_2 = pos

                self.partie.couple_de_position = self.position_1, self.position_2

                self.partie.tour()

                # On affiche le damier mis a jour.
                self.canvas_damier.actualiser()

                couleur = str(self.partie.couleur_joueur_courant)
                self.couleur_joueur['text'] = 'Tour du joueur {}'.format(couleur)

                # Réinitialisation des attributs
                self.position_1 = -1, -1
                self.position_2 = -2, -2
                self.bool_piece_selectionnee = False
                self.piece_selectionnee = None
                self.position_selectionnee = None
                self.partie.position_source_selectionnee = None
                return


if __name__ == 'main':
    ia = IA_dames()
    ia.mainloop()