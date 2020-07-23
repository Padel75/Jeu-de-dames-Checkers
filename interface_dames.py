# Auteurs: Ariane Fiset et Pascal de Le Rue

from tkinter import Tk, Label, NSEW, Button, Canvas
from canvas_damier import CanvasDamier
from partie import Partie
from position import Position


class FenetrePartie(Tk):
    """Interface graphique de la partie de dames.

    Attributes:
        partie (Partie): Le gestionnaire de la partie de dame
        canvas_damier (CanvasDamier): Le «widget» gérant l'affichage du damier à l'écran
        messages (Label): Un «widget» affichant des messages textes à l'utilisateur du programme

        TODO: AJOUTER VOS PROPRES ATTRIBUTS ICI!
    """

    def __init__(self):
        """Constructeur de la classe FenetrePartie. On initialise une partie en utilisant la classe Partie du TP3 et
        on dispose les «widgets» dans la fenêtre.
        """

        # Appel du constructeur de la classe de base (Tk)
        super().__init__()

        # La partie
        self.partie = Partie()

        # Création du canvas damier.
        self.canvas_damier = CanvasDamier(self, self.partie.damier, 60)
        self.canvas_damier.grid(sticky=NSEW)
        self.canvas_damier.bind('<Button-1>', self.selectionner)

        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid()

        # Ajout d'une étiquette de couleur du tour du joueur
        self.couleur_joueur = Label(self)
        self.couleur_joueur.grid()
        self.couleur_joueur['text'] = 'Tour du joueur {}'.format('blanc')

        # Nom de la fenêtre («title» est une méthode de la classe de base «Tk»)
        self.title("Jeu de dames")

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Pour se rappeler si une pièce est sélectionnée:
        self.bool_piece_selectionnee = False
        self.piece_selectionnee = None
        self.position_selectionnee = None

        # Variable de déplacement
        self.position_cible_graphique = None

        # Création du bouton 'Nouvelle partie'
        self.bouton_nouvelle_partie = Button(self, text="Nouvelle partie", command=self.nouvelle_partie)
        self.bouton_nouvelle_partie.grid()


        # Création du bouton 'quitter'
        self.bouton_Quitter = Button(self, text="Quitter", command=self.quit, padx=10, pady=10)
        self.bouton_Quitter.grid(padx=10, pady=10)

        # Création du bourron 'Réglements'
        self.bouton_reglements = Button(self, text="Reglements", command=self.open_rules)
        self.bouton_reglements.grid()

    def nouvelle_partie(self):
        self.partie.__init__()


    def ouvrir_reglements(self):
        fenetre_reglements = Tk()
        texte = Label(fenetre_reglements, text="REGLEMENTS DU JEU : \n - Le joueur avec les pièces blanches commence la"
                                              " partie \n - Une pièce de départ s'appel un pion et peut se déplacer en"
                                              " diagonale vers l'avant. Une case doit être libre pour pouvoir s'y "
                                              "déplacer. \n - Lorsqu'un pion atteint le côté opposé du plateau, il "
                                              "devient un dame. Une dame a la particularité qu'elle peut aussi se "
                                              "déplacer vers l'arrière. \n - Une prise est l'action de 'manger' une "
                                              "pièce adverse. Elle est effectuée en sautant par-dessus la pièce "
                                              "adverse, toujours en diagonale, vers l'avant ou l'arrière. On ne peut "
                                              "pas sauter par-dessus qu'une pièce adverse à la fois : il faut donc que"
                                              " la case d'arrivée soit libre \n - Après une prise, le joueur courant "
                                              "peut effectuer une (ou plusieurs) prise(s) supplémentaire(s) en "
                                              "utilisant la même pièce. \n - Lors du tour d'un joueur, si celui-ci peut"
                                              " prendre une pièce ennemie, il doit absolument le faire. \n - Lorsqu'un "
                                              "joueur commence son tour et prend une pièce adverse, s'il peut continuer"
                                              " son tour en continuant de prendre des pièces adverses avec la même "
                                              "pièce, il doit le faire.")
        texte.grid()

        fenetre_reglements.mainloop()


    def selectionner(self, event):
        """Méthode qui gère le clic de souris sur le damier.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """
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






if __name__ == '__main__':
    # Point d'entrée principal du TP4.
    fenetre = FenetrePartie()
    fenetre.mainloop()