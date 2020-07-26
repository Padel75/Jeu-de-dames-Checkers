# Auteurs: Ariane Fiset et Pascal de Le Rue

from tkinter import Tk, Label, NSEW, Button, Canvas, Frame, ttk
from canvas_damier import CanvasDamier
from partie import Partie
from position import Position
from os import getcwd, remove
from piece import Piece



class FenetrePartie(Tk):
    """
    Interface graphique de la partie de dames.

    Attributes:
        partie (Partie): Le gestionnaire de la partie de dame.
        canvas_damier (CanvasDamier): Le «widget» gérant l'affichage du damier à l'écran.
        messages (Label): Un «widget» affichant des messages textes à l'utilisateur du programme.
        couleur_joueur (Label): Un «widget» affichant la couleur du joueur courant.
        bool_piece_selectionnee (bool): Un booleen dont la valeur est True si une pièce est sélectionnée par le joueur.
        piece_selectionnee (Piece): La pièce sélectionnée par le joueur.
        position_selectionnee (Position): La position de la pièce sélectionnée par le joueur.
        position_cible_graphique (Position): La position cible valide sélectionnée par le joueur.
        texte_deplacements (str): Le texte enregistrant les déplacements effectuées par les joueurs.
        cadre_bouton (Frame): Un cadre servant à positionner les boutons.
        bouton_nouvelle_partie (Button): Un bouton pour initialiser une nouvelle partie.
        bouton_Quitter (Button): Un bouton pour quitter la fenêtre de partie.
        bouton_reglements (Button): Un bouton pour afficher les règlements dans une nouvelle fenêtre.
        bouton_deplacements (Button): Un bouton pour afficher l'historique des déplacements de la partie dans une
                                        nouvelle fenêtre.
        bouton_sauvegarder (Button): Un bouton pour sauvegarder la partie dans un fichier .txt.
        bouton_charger (Button): Un bouton pour charger la précédente sauvegarde.
        bouton_triche (Button): Un bouton pour ouvrir les options de triches dans une nouvelle fenêtre.
        fenetre_alarme (Tk): Une fenêtre affichant un message d'alarme au joueur.
    """
    def __init__(self):
        """Constructeur de la classe FenetrePartie. On initialise une partie en utilisant la classe Partie du TP3 et
        on dispose les «widgets» dans la fenêtre.
        """
        # Appel du constructeur de la classe de base (Tk):
        super().__init__()

        # La partie:
        self.partie = Partie()

        # Création du canvas damier:
        self.canvas_damier = CanvasDamier(self, self.partie.damier, 60)
        self.canvas_damier.grid(sticky=NSEW)
        self.canvas_damier.bind('<Button-1>', self.selectionner)

        # Ajout d'une étiquette d'information:
        self.messages = Label(self)
        self.messages.grid()

        # Ajout d'une étiquette de couleur du tour du joueur:
        self.couleur_joueur = Label(self)
        self.couleur_joueur.grid()
        self.couleur_joueur['text'] = 'Tour du joueur {}'.format('blanc')

        # Nom de la fenêtre («title» est une méthode de la classe de base «Tk»):
        self.title("Jeu de dames")

        # Truc pour le redimensionnement automatique des éléments de la fenêtre:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Ajout de variables se rappelant si une pièce est sélectionnée:
        self.bool_piece_selectionnee = False
        self.piece_selectionnee = None
        self.position_selectionnee = None

        # Ajout d'uhe variable gérant le déplacement:
        self.position_cible_graphique = None

        # Ajout d'une chaîne de caractère enregistrant les déplacements effectués:
        self.texte_deplacements = 'Liste des déplacements, du plus récent au plus ancien: \n'

        # Ajout du cadre des boutons:
        self.cadre_bouton = Frame()
        self.cadre_bouton.grid()

        # Création du bouton 'Nouvelle partie':
        self.bouton_nouvelle_partie = Button(self.cadre_bouton, text="Nouvelle partie",
                                             command=self.nouvelle_partie, padx=10, pady=10)
        self.bouton_nouvelle_partie.grid(padx=10, pady=10, column=0, row=0)


        # Création du bouton 'quitter':
        self.bouton_Quitter = Button(self.cadre_bouton, text="Quitter", command=self.quit, padx=10, pady=10)
        self.bouton_Quitter.grid(padx=10, pady=10, column=1, row=0)

        # Création du bourron 'Règlements':
        self.bouton_reglements = Button(self.cadre_bouton, text="Règlements",
                                        command=self.ouvrir_reglements, padx=10, pady=10)
        self.bouton_reglements.grid(padx=10, pady=10, column=2, row=0)

        # Création du bouton 'Déplacement':
        self.bouton_deplacements = Button(self.cadre_bouton, text='Déplacements',
                                          command=self.afficher_deplacements, padx=10, pady=10)
        self.bouton_deplacements.grid(padx=10, pady=10, column=3, row=0)

        # Création du bouton 'Sauvegarder':
        self.bouton_sauvegarder = Button(self.cadre_bouton, text='Sauvegarder',
                                         command=self.sauvegarder_partie, padx=10, pady=10)
        self.bouton_sauvegarder.grid(padx=10, pady=10, column=0, row=1)

        # Création du bouton 'Charger':
        self.bouton_charger = Button(self.cadre_bouton, text='Charger',
                                         command=self.charger_partie, padx=10, pady=10)
        self.bouton_charger.grid(padx=10, pady=10, column=1, row=1)

        # Création du bouton 'Tricher':
        self.bouton_triche = Button(self.cadre_bouton, text="Tricher",
                                        command=self.ouvrir_triches, padx=10, pady=10)
        self.bouton_triche.grid(padx=10, pady=10, column=2, row=1)

        # Initialisation de la variable 'fenetre_alarme':
        self.fenetre_alarme = None

    def nouvelle_partie(self):
        """
        Fonction supprimant la fenêtre de partie courante et relançant une nouvelle partie.
        """
        self.destroy()
        Nouvelle_partie = Fenetredimension()

    def ouvrir_reglements(self):
        """
        Fonction ouvrant une nouvelle fenêtre contenant un texte décrivant les règlements du jeu.
        """
        fenetre_reglements = Tk()  # Création de la nouvelle fenêtre.

        # Ajout de l'étiquette contenant le texte des règlements:
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
        """
        Fonction créant une nouvelle fenêtre contenant un texte affichant l'historique des déplacements des joueurs.
        L'enregistrement des déplacements est géré par la fonction selectionner.
        """
        fenetre_deplacements = Tk()  # Création de la nouvelle fenêtre.

        # Création de l'étiquette ayant les déplacements comme texte:
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
        try:  # Essai d'ouverture et de fermeture du fichier, et retour du booléen True en cas de succès
            f = open(nom_de_fichier, 'r')
            f.close()
            return True
        except Exception:  # En cas d'échec, retour de False
            return False

    def fonction_de_sauvegarde(self):
        """
        Fonction écrasant la sauvegarde précédente et sauvegardant la partie actuelle.
        """
        # Vérification de l'existence du fichier 'sauvegarde':
        if self.existe('sauvegarde.txt'):
            remove('sauvegarde.txt')

        # Création de la sauvegarde:
        fichier = open('sauvegarde.txt', 'w')
        print(self.partie.damier.cases, file=fichier)
        fichier.close()

        # Fermeture de la fenêtre d'alarme générée par la fonction self.sauvegarder_partie:
        self.fenetre_alarme.destroy()

    def sauvegarder_partie(self):
        """
        Fonction générant une fenêtre d'alarme demandant à l'utilisateur s'il veut bien sauvegarder.
        """
        # Génération de la nouvelle fenêtre d'alarme:
        self.fenetre_alarme = Tk()

        # Ajout d'une étiquette contenant le texte voulue:
        texte_alarme = Label(self.fenetre_alarme, text='Si vous sauvegarder maintenant, la sauvegarde précédente sera écrasée. \n Voulez-vous continuer?', padx=10, pady=10)
        texte_alarme.grid(row=0, column=1, padx=10, pady=10)

        # Création du bouton 'oui':
        bouton_oui = Button(self.fenetre_alarme, text='Oui', command=self.fonction_de_sauvegarde, padx=10, pady=10)
        bouton_oui.grid(row=1, column=0, padx=10, pady=10)

        # Création du bouton 'non':
        bouton_non = Button(self.fenetre_alarme, text='Non', command=self.fenetre_alarme.destroy, padx=10, pady=10)
        bouton_non.grid(row=1, column=2, padx=10, pady=10)

    def charger_partie(self):
        """
        Fonction chargeant une partie précédemment sauvegardée. Génère une fenêtre d'alarme en cas d'absence
         de sauvegarde.
        """
        if self.existe('sauvegarde.txt'):  # Vérification de l'exitence de la sauvegarde.

            # Récupération des données enregistrées dans le fichier .txt:
            unfichier = open('sauvegarde.txt', 'r')
            dicostr = unfichier.readline()
            unfichier.close()

            # initialisation des variables nécessaires:
            dico = {}  # Le dictionnaire récupéré.
            clef = ''  # La clé de dictionnaire récupérée sous format str.
            clef_p = ''  # La clé de dictionnaire récupérée sous format Position.
            valeur = ''  # La valeur associé à une clé de dictionnaire.

            # Parcours des éléments de la chaîne de caratères contenue dans le fichier .txt:
            for i in dicostr:
                if i == '{' or i == '}' or i == ' ' or i == ',':  # Les caractères à ignorer.
                    pass
                elif i == 'o' or i == 'O' or i == 'x' or i =='X':  # Les caratères représentant les types de pièces.

                    # Gestion des valeurs du dictionnaire:
                    if i == 'o':

                        valeur = Piece("blanc", "pion")  # La bonne valeur est associée à la variable 'valeur'.
                        dico[clef_p] = valeur  # Ajout de l'élément clé-valeur au dictionnaire 'dico'.

                        # Réinitialisation des variables:
                        clef_p = ''
                        valeur = ''
                        clef = ''

                    # Les mêmes étapes sont répétés pour les autres types de pièces:
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

                # Gestion des clefs du dictionnaire 'dico':
                elif i == ':':  # Passage d'une clef à une valeur dans la variable dico_str:
                    tuple1 = ''  # Initialisation de la chaîne de caractère 'tuple1'
                    for i in clef:  # Parcours des caractères de la chaîne de caractère 'clef'.
                        # Si le caractère peut être un entier, il est ajouter à tuple1:
                        try:
                            int(i)
                            tuple1 += i
                        except Exception:
                            pass

                    # La variable 'clef_p' reçoit la bonne valeur:
                    clef_p = Position(int(tuple1[0]), int(tuple1[1]))

                    # Réinitialisation des variables:
                    tuple1 = ''
                    clef = ''

                # Dans les autres cas, 'clef' continie de stocker les caratères:
                else:
                    clef += i

            # Le dictionnaire définissant la partie est mis à jour par la sauvegarde:
            self.partie.damier.cases = dico

            # Le damier est actualiser:
            self.canvas_damier.actualiser()

        # Si la sauvegarde n'existe pas, l'utilisateur en est informé:
        else:
            fenetre_alerte = Tk()  # Création d'une nouvelle fenêtre.
            texte = Label(fenetre_alerte, text='Aucune sauvegarde n\'est disponible', anchor='e')
            texte.grid(padx=10, pady=10)

            # Création du bouton pour quitter la fenêtre:
            bouton_quitter = Button(fenetre_alerte, text="Ok", command=fenetre_alerte.destroy, padx=10, pady=10)
            bouton_quitter.grid(padx=10, pady=10)

            fenetre_alerte.mainloop()

    def ouvrir_triches(self):
        """
        Fonction ouvrant une nouvelle fenêtre exposant les options de triches.
        """
        # Création d'une nouvelle fenêtre:
        fenetre_triche = Tk()

        # Création du bouton permettant de transformer toutes les pièces en dames:
        bouton_dame_tous = Button(fenetre_triche, text='Toutes les pièces \n deviennent des dames',
                                  command=self.pion_en_dames_tous, padx=10, pady=10)
        bouton_dame_tous.grid(column=0, row=0, padx=10, pady=10)

        # Création du bouton permettant de transformer les pièces blanches en dames:
        bouton_dame_blanc = Button(fenetre_triche, text='Les pièces blanches \n deviennent des dames',
                                   command=self.pion_en_dames_blanc, padx=10, pady=10)
        bouton_dame_blanc.grid(column=1, row=0, padx=10, pady=10)

        # Création du bouton permettant de transformer les pièces noires en dames:
        bouton_dame_noir = Button(fenetre_triche, text='Les pièces noires \n deviennent des dames.',
                                  command=self.pion_en_dames_noir, padx=10, pady=10)
        bouton_dame_noir.grid(column=2, row=0, padx=10, pady=10)

        # Création du bouton permettant de quitter la fenêtre:
        bouton_quitter = Button(fenetre_triche, text='Terminer', command = fenetre_triche.destroy, padx=10, pady=10)
        bouton_quitter.grid(column=1, row=1, padx=10, pady=10)

        fenetre_triche.mainloop()

    def pion_en_dames_noir(self):
        """
        Fonction transformant les pièces noires en dames.
        """
        # Boucle sur le dictionnaire définissant la partie:
        for position in self.partie.damier.cases:
            piece = self.partie.damier.recuperer_piece_a_position(position)

            # Promotion de la pièce si celle-ci est noire:
            if piece.couleur == 'noir':
                piece.promouvoir()

        # Actualisation du damier:
        self.canvas_damier.actualiser()

    def pion_en_dames_tous(self):
        """
        Fonction transformant toutes les pièces en dames.
        """
        # Boucle sur le dictionnaire définissant la partie:
        for position in self.partie.damier.cases:
            piece = self.partie.damier.recuperer_piece_a_position(position)

            # Promotion de la pièce:
            piece.promouvoir()

        # Actualisation du damier:
        self.canvas_damier.actualiser()

    def pion_en_dames_blanc(self):
        """
        Fonction transformant les pièces noires en dames.
        """
        # Boucle sur le dictionnaire définissant la partie:
        for position in self.partie.damier.cases:
            piece = self.partie.damier.recuperer_piece_a_position(position)

            # Promotion de la pièce si celle-ci est blanche:
            if piece.couleur == 'blanc':
                piece.promouvoir()

        # Actualisation du damier:
        self.canvas_damier.actualiser()


    def selectionner(self, event):
        """Méthode qui gère le clic de souris sur le damier, exécute la gestion des tours et retourne un message
        pertinent en cas de victoire.

        Args:
            event (tkinter.Event): Objet décrivant l'évènement qui a causé l'appel de la méthode.

        """
        # Gestion du clic de position cible:
        if self.bool_piece_selectionnee:

            # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
            ligne_deplacement = event.y//self.canvas_damier.n_pixels_par_case
            colonne_deplacement = event.x//self.canvas_damier.n_pixels_par_case

            # Vérification de la validité de la position cible désignée:
            if self.partie.position_cible_valide(Position(ligne_deplacement, colonne_deplacement))[0]:
                # Si la position cible est valide, elle est attribuée à la variable 'self.position_cible_graphique:
                self.position_cible_graphique = Position(ligne_deplacement, colonne_deplacement)

            else: # Affichage d'un message d'erreur pertinent en cas de position non valide:
                self.messages['foreground'] = 'red'
                self.messages['text'] = self.partie.position_cible_valide(Position(ligne_deplacement, colonne_deplacement))[1]

            # Attribution des positions sélectionnées par clic à la variable pertinente de la classe partie:
            self.partie.couple_de_position = self.position_selectionnee, self.position_cible_graphique

            # Mise à jour du texte des déplacements:
            self.texte_deplacements += 'Déplacement du joueur {}, de {} vers {}. \n'.format(str(
                self.partie.couleur_joueur_courant), str(self.position_selectionnee),
                str(self.position_cible_graphique))

            # Exécution d'un tour:
            self.partie.tour()

            # On affiche le damier mis a jour.
            self.canvas_damier.actualiser()

            #  Mise à jour de l'affichage du joueur courant:
            couleur = str(self.partie.couleur_joueur_courant)
            self.couleur_joueur['text'] = 'Tour du joueur {}'.format(couleur)

            # Réinitialisation des attributs
            self.bool_piece_selectionnee = False
            self.piece_selectionnee = None
            self.position_selectionnee = None
            self.partie.position_source_selectionnee = None

            # Gestion des messages de victoire:
            if not self.partie.damier.piece_de_couleur_peut_se_deplacer(self.partie.couleur_joueur_courant) and \
                    not self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.partie.couleur_joueur_courant):

                if self.partie.couleur_joueur_courant == 'noir':
                    self.messages['foreground'] = 'blue'
                    self.messages['text'] = 'Victoire du joueur blanc! Félicitations!'
                    return  # Arrêt de la méthode

                if self.partie.couleur_joueur_courant == 'blanc':
                    self.messages['foreground'] = 'blue'
                    self.messages['text'] = 'Victoire du joueur noir! Félicitations!'
                    return  # Arrêt de la méthode

            # Fin de l'exécution de la méthode:
            return

        # Gestion du clic de position source:
        if not self.bool_piece_selectionnee:

            # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
            ligne = event.y // self.canvas_damier.n_pixels_par_case
            colonne = event.x // self.canvas_damier.n_pixels_par_case

            # Validation de la position source sélectionnée
            if self.partie.position_source_valide(Position(ligne, colonne))[0]:
                # Si le joueur peut faire une prise, il y est obligé.
                # Vérification si le joueur peut faire une prise:
                if self.partie.damier.piece_de_couleur_peut_faire_une_prise(self.partie.couleur_joueur_courant):
                    # Vérification si la pièce sélectionnée peut faire une prise:
                    if self.partie.damier.piece_peut_faire_une_prise(Position(ligne, colonne)):
                        # Vérification si le joueur à déjà pris une pièce et doit continuer à prendre avec celle-ci:
                        if self.partie.position_source_forcee is not None\
                                and self.partie.position_source_forcee == Position(ligne, colonne):
                            # Si toutes les conditions sont réunies, les variables spnt mises à jour:
                            self.position_selectionnee = Position(ligne, colonne)
                            self.partie.position_source_selectionnee = self.position_selectionnee

                        # Si le joueur n'est pas contraint par une position source forcée:
                        elif self.partie.position_source_forcee is None:
                            self.position_selectionnee = Position(ligne, colonne)
                            self.partie.position_source_selectionnee = self.position_selectionnee

                        # Affichage d'un message d'erreur pertinent en cas d'erreur et arrêt de la méthode:
                        else:
                            self.messages['foreground'] = 'red'
                            self.messages['text'] = 'Erreur: Vous devez sélectionner la piece {}'\
                                .format(str(self.partie.position_source_forcee))
                            return  # Arrêt de la méthode

                    #  Affichage d'un message d'erreur pertinent en cas d'erreur:
                    else:
                        self.messages['foreground'] = 'red'
                        self.messages['text'] = 'Erreur: Vous devez sélectionner une pièce pouvant faire une prise.'

                # Si le joueur n'est pas contraint dans son choix de position source:
                else:
                    self.position_selectionnee = Position(ligne, colonne)
                    self.partie.position_source_selectionnee = self.position_selectionnee

                # On récupère l'information sur la pièce à l'endroit choisi.
                self.piece_selectionnee = self.partie.damier.recuperer_piece_a_position(self.position_selectionnee)

                # Affichage d'un message pertinent si le joueur à sélectionner une pièce source valide:
                if self.piece_selectionnee is not None:
                    self.messages['foreground'] = 'black'
                    self.messages['text'] = 'Pièce sélectionnée à la position {}.'.format(self.position_selectionnee)
                    self.bool_piece_selectionnee = True

            # Affichage d'un message d'erreur si la position source n'est pas valide et arrêt de la méthode:
            else:
                self.messages['foreground'] = 'red'
                self.messages['text'] = self.partie.position_source_valide(Position(ligne, colonne))[1]
                return  # Arrêt de la méthode

            # On affiche le damier mis a jour.
            self.canvas_damier.actualiser()

class Fenetredimension(Tk):
    """
    Interface graphique du dimensionnement de la partie de dame.

       Attributes:
           texte, texte1, texte2 (Label): Des étiquettes informatives.
           dimension_lignes_damier (Combobox): Une boîte contenant les choix de lignes.
           nbr_ligne_partie (int): Le nombre de lignes sélectionné.
           dimension_colonne_damier (Combobox): Une boîte contenant les choix de colonnes.
           nbr_colonne_partie (int): le nombre de colonnes sélectionné.
           bouton_debut_partie (Button): un bouton pour lancer la partie.
    """
    def __init__(self):
        """
        Constructeur de la classe Fenetredimension.
        """
        # Appel du constructeur parent:
        super().__init__()

        # Création de combobox dimensions damier
        self.title('Dimensions du jeu')

        self.texte = Label(self, text='Quel est la taille du damier que vous désirez', padx=10, pady=10)
        self.texte.grid(padx=10, pady=10, row=0)

        self.texte1 = Label(self, text='Nombre de lignes:', padx=10)
        self.texte1.grid(padx=10, row=1)

        self.dimension_lignes_damier = ttk.Combobox(self, text='Nombre de lignes du damier',
                                                values=('7', '8', '9', '10', '11', '12'))
        self.dimension_lignes_damier.grid(padx=10, pady=10, row=2)
        self.dimension_lignes_damier.current(1)

        self.nbr_ligne_partie = int(self.dimension_lignes_damier.get())

        self.texte2 = Label(self, text='Nombre de colonnes:', padx=10)
        self.texte2.grid(padx=10, row=3)

        self.dimension_colonne_damier = ttk.Combobox(self, text='Nombre de colonne du damier',
                                                values=('7', '8', '9', '10', '11', '12'))
        self.dimension_colonne_damier.grid(padx=10, pady=10, row=4)
        self.dimension_colonne_damier.current(1)

        self.nbr_colonne_partie = int(self.dimension_colonne_damier.get())

        self.bouton_debut_partie = Button(self, text='Débuter la partie',
                                          command=self.commande_bouton, padx=10, pady=10)
        self.bouton_debut_partie.grid(padx=10, pady=10, row=5)

    def commande_bouton(self):
        """
        Fonction de commande du bouton bouton_debut_partie
        """
        # Dimension du damier
        self.nbr_colonne_partie = int(self.dimension_colonne_damier.get())
        self.nbr_ligne_partie = int(self.dimension_lignes_damier.get())

        # Gestion du dictionnaire de pièces:
        dico_pst = {}

        for i in range(self.nbr_colonne_partie):

            if (i % 2) == 0:

                dico_pst[Position(self.nbr_ligne_partie-1, i)] = Piece("blanc", "pion")
                dico_pst[Position(self.nbr_ligne_partie-3, i)] = Piece("blanc", "pion")

                dico_pst[Position(1, i)] = Piece("noir", "pion")


            else:

                dico_pst[Position(self.nbr_ligne_partie-2, i)] = Piece("blanc", "pion")

                dico_pst[Position(0, i)] = Piece("noir", "pion")
                dico_pst[Position(2, i)] = Piece("noir", "pion")

        # Créatio  de la nouvelle partie:
        nouvelle_partie = FenetrePartie()

        # Mise à jour des paramètres:
        nouvelle_partie.partie.damier.n_colonnes = self.nbr_colonne_partie
        nouvelle_partie.partie.damier.n_lignes = self.nbr_ligne_partie
        nouvelle_partie.partie.damier.cases = dico_pst

        # Actualisation de l'affichage:
        nouvelle_partie.canvas_damier.actualiser()

        # Destruction de la fenêtre d'options:
        self.destroy()


if __name__ == '__main__':

    # Ouverture de la fenetre de dimensionnement de la partie
    fenetre_dimensionnement = Fenetredimension()
    fenetre_dimensionnement.mainloop()

    # Ouverture de la fenetre du jeu
    #fenetre = FenetrePartie()
    #fenetre.mainloop()