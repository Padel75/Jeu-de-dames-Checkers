# Auteurs: Ariane Fiset et Pascal de Le Rue

from tkinter import Tk, Label, NSEW, Button
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

        # Création du bouton 'quitter'
        self.bouton = Button(self, text="Quitter", command=self.quit, padx=10, pady=10)
        self.bouton.grid(padx=20, pady=20)

    def selectionner(self, event):
        """Méthode qui gère le clic de souris sur le damier.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """
        if self.bool_piece_selectionnee:

            # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
            ligne_deplacement = event.y//self.canvas_damier.n_pixels_par_case
            colonne_deplacement = event.x//self.canvas_damier.n_pixels_par_case
            if self.partie.position_cible_valide(Position(ligne_deplacement, colonne_deplacement))[0] == True:
                self.position_cible_graphique = Position(ligne_deplacement, colonne_deplacement)
            else:
                print(self.partie.position_cible_valide(Position(ligne_deplacement, colonne_deplacement))[1])

            self.partie.couple_de_position = self.position_selectionnee, self.position_cible_graphique
            self.partie.tour()

            # On affiche le damier mis a jour.
            self.canvas_damier.actualiser()

            self.bool_piece_selectionnee = False
            self.piece_selectionnee = None
            self.position_selectionnee = None

        if not self.bool_piece_selectionnee:
            # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
            ligne = int(event.y // self.canvas_damier.n_pixels_par_case)
            colonne = int(event.x // self.canvas_damier.n_pixels_par_case)
            if self.partie.position_source_valide(Position(ligne, colonne))[0]:
                self.position_selectionnee = Position(ligne, colonne)
                self.partie.position_source_selectionnee = self.position_selectionnee
            else:
                print(self.partie.position_cible_valide(Position(ligne, colonne))[1])

            # On récupère l'information sur la pièce à l'endroit choisi.
            self.piece_selectionnee = self.partie.damier.recuperer_piece_a_position(self.position_selectionnee)

            if self.piece_selectionnee is None:
                self.messages['foreground'] = 'red'
                self.messages['text'] = 'Erreur: Aucune pièce à cet endroit.'
            else:
                self.messages['foreground'] = 'black'
                self.messages['text'] = 'Pièce sélectionnée à la position {}.'.format(self.position_selectionnee)
                self.bool_piece_selectionnee = True

            # On affiche le damier mis a jour.
            self.canvas_damier.actualiser()

        # TODO: À continuer....


if __name__ == '__main__':
    # Point d'entrée principal du TP4.
    fenetre = FenetrePartie()
    fenetre.mainloop()
