# Auteurs: Ariane Fiset et Pascal de Le Rue

from tkinter import Tk, Label, NSEW, Button, Canvas, Frame, ttk
from canvas_damier import CanvasDamier
from partie import Partie
from position import Position
from os import getcwd, remove
from piece import Piece



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

        self.texte_deplacements = 'Liste des déplacements, du plus récent au plus ancien: \n'

        self.rep_courant = getcwd()

        #Cadre des boutons
        self.cadre_bouton = Frame()
        self.cadre_bouton.grid()

        # Création du bouton 'Nouvelle partie'
        self.bouton_nouvelle_partie = Button(self.cadre_bouton, text="Nouvelle partie",
                                             command=self.nouvelle_partie, padx=10, pady=10)
        self.bouton_nouvelle_partie.grid(padx=10, pady=10, column=0, row=0)


        # Création du bouton 'quitter'
        self.bouton_Quitter = Button(self.cadre_bouton, text="Quitter", command=self.quit, padx=10, pady=10)
        self.bouton_Quitter.grid(padx=10, pady=10, column=1, row=0)

        # Création du bourron 'Règlements'
        self.bouton_reglements = Button(self.cadre_bouton, text="Règlements",
                                        command=self.ouvrir_reglements, padx=10, pady=10)
        self.bouton_reglements.grid(padx=10, pady=10, column=2, row=0)

        # Création du bouton 'Déplacement'
        self.bouton_deplacements = Button(self.cadre_bouton, text='Déplacements',
                                          command=self.afficher_deplacements, padx=10, pady=10)
        self.bouton_deplacements.grid(padx=10, pady=10, column=3, row=0)

        # Création du bouton 'Sauvegarder'
        self.bouton_sauvegarder = Button(self.cadre_bouton, text='Sauvegarder',
                                         command=self.sauvegarder_partie, padx=10, pady=10)
        self.bouton_sauvegarder.grid(padx=10, pady=10, column=0, row=1)

        # Création du bouton 'Charger'
        self.bouton_charger = Button(self.cadre_bouton, text='Charger',
                                         command=self.charger_partie, padx=10, pady=10)
        self.bouton_charger.grid(padx=10, pady=10, column=2, row=1)

        # Dimension du damier
        #self.partie.damier.n_colonnes = self.Fenetredimension.dimension_colonne_damier
        #self.partie.damier.n_lignes = self.Fenetredimension.dimension_lignes_damier

    def nouvelle_partie(self):
        self.destroy()
        self.__init__()


    def ouvrir_reglements(self):
        fenetre_reglements = Tk()
        texte = Label(fenetre_reglements, text="REGLEMENTS DU JEU : \n"
                                               " - Le joueur avec les pièces blanches commence la partie \n \n"
                                               " - Une pièce de départ s'appel un pion et peut se déplacer \n"
                                               "en diagonale vers l'avant. Une case doit être libre pour \n"
                                               "pouvoir s'y déplacer. \n \n"
                                               " - Lorsqu'un pion atteint le côté opposé du plateau, il \n"
                                               " devient un dame. Une dame a la particularité qu'elle peut \n"
                                               " aussi se déplacer vers l'arrière. \n \n"
                                               " - Une prise est l'action de 'manger' une pièce adverse. \n"
                                               " Elle est effectuée en sautant par-dessus la pièce adverse,\n"
                                               " toujours en diagonale, vers l'avant ou l'arrière. On ne \n"
                                               " peut pas sauter par-dessus qu'une pièce adverse à la fois :\n"
                                               " il faut donc que la case d'arrivée soit libre \n \n"
                                               " - Après une prise, le joueur courant peut effectuer une\n"
                                               " (ou plusieurs) prise(s) supplémentaire(s) en utilisant la\n"
                                               " même pièce. \n \n"
                                               " - Lors du tour d'un joueur, si celui-ci peut prendre une\n"
                                               " pièce ennemie, il doit absolument le faire. \n \n"
                                               " - Lorsqu'un joueur commence son tour et prend une pièce\n"
                                               " adverse, s'il peut continuer son tour en continuant de\n"
                                               " prendre des pièces adverses avec la même pièce, il doit\n"
                                               " le faire.", anchor='e')
        texte.grid()
        fenetre_reglements.mainloop()

    def afficher_deplacements(self):
        fenetre_deplacements = Tk()
        texte_d = Label(fenetre_deplacements, text=self.texte_deplacements, anchor='e', padx=10, pady=10)
        texte_d.grid()
        fenetre_deplacements.mainloop()



    def existe(self, nom_de_fichier):
        """
        Fonction vérifiant l'existence d'un fichier.

        Note: Cette fonction est directement inspirée d'une fonction contenu dans le livre
        'Apprendre à programmer avec Python 3', Gérard Swinnen, page 118.

        Args:
            nom_de_fichier (str): le nom d'un fichier.

        Returns:
            bool: True si le fichier existe, False autrement
        """
        try:
            f = open(nom_de_fichier, 'r')
            f.close()
            return True
        except Exception:
            return False

    def sauvegarder_partie(self):
        # demander par une fenêtre si l'utilisateur veut écraser une éventuelle sauvegarde précédente.
        if self.existe('sauvegarde.txt'):
            remove('sauvegarde.txt')
        else:
            fichier = open('sauvegarde.txt', 'w')
            print(self.partie.damier.cases, file=fichier)
            fichier.close()

    def charger_partie(self):
        if self.existe('sauvegarde.txt'):
            unfichier = open('sauvegarde.txt', 'r')
            dicostr = unfichier.readline()
            unfichier.close()
            # Point test:
            print(type(dicostr))
            print(dicostr)

            dico = {}
            clef = ''
            clef_p = ''
            valeur = ''

            for i in dicostr:
                if i == '{' or i == '}' or i == ' ' or i == ',':
                    pass
                elif i == 'o' or i == 'O' or i == 'x' or i =='X':
                    if i == 'o':
                        valeur = Piece("blanc", "pion")
                        dico[clef_p] = valeur
                        clef_p = ''
                        valeur = ''
                        clef = ''
                    if i == 'O':
                        valeur = Piece("blanc", "dame")
                        dico[clef_p] = valeur
                        clef_p = ''
                        valeur = ''
                        clef = ''
                    if i == 'x':
                        valeur = Piece("noir", "pion")
                        dico[clef_p] = valeur
                        clef_p = ''
                        valeur = ''
                        clef = ''
                    if i == 'X':
                        valeur = Piece("noir", "dame")
                        dico[clef_p] = valeur
                        clef_p = ''
                        valeur = ''
                        clef = ''
                elif i == ':':
                    tuple1 = ''
                    for i in clef:
                        try:
                            int(i)
                            tuple1 += i
                        except Exception:
                            pass
                    clef_p = Position(int(tuple1[0]), int(tuple1[1]))
                    tuple1 = ''
                    clef = ''
                else:
                    clef += i

            print(valeur)
            print(dicostr)
            print(dico)
            self.partie.damier.cases = dico
            self.canvas_damier.actualiser()
        else:
             print('ce fichier n\'existe pas')



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

            self.texte_deplacements += 'Déplacement du joueur {}, de {} vers {}. \n'.format(str(
                self.partie.couleur_joueur_courant), str(self.position_selectionnee),
                str(self.position_cible_graphique))

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

class Fenetredimension(Tk):
    """Interface graphique du dimensionnement de la partie de dame
       Attributes:
            partie (Partie): Le gestionnaire de la partie de dame
            canvas_damier (CanvasDamier): Le «widget» gérant l'affichage du damier à l'écran
            messages (Label): Un «widget» affichant des messages textes à l'utilisateur du programme
    """

    def __init__(self):
        """#Constructeur de la classe Fenetredimension.
        """
        # Appel du constructeur de la classe de base (Tk)
        super().__init__()
        # Création de combobox dimensions damier
        fenetre_dim = Tk()

        self.texte = Label(fenetre_dim, text='Quel est la taille du damier que vous désirez')
        self.texte.grid()
        self.dimension_lignes_damier = ttk.Combobox(fenetre_dim, text='Nombre de lignes du damier', values=('5', '6', '7', '8', '9', '10', '11', '12'))
        self.dimension_lignes_damier.grid()
        self.dimension_lignes_damier.current(3)
        self.dimension_colonne_damier = ttk.Combobox(fenetre_dim, text='Nombre de colonne du damier', values=('5', '6', '7', '8', '9', '10', '11', '12'))
        self.dimension_colonne_damier.grid()
        self.dimension_colonne_damier.current(3)
        self.bouton_debut_partie = Button(fenetre_dim, text='Débuter la partie', command=fenetre_dim.quit)
        self.bouton_debut_partie.grid()


if __name__ == '__main__':
    # Ouverture de la fenetre de dimensionnement de la partie
    #fenetre_dimensionnement = Fenetredimension()
    #fenetre_dimensionnement.mainloop()

    # Ouverture de la fenetre du jeu
    fenetre = FenetrePartie()
    fenetre.mainloop()