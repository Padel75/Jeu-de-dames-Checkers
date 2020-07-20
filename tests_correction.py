# Auteurs: Pascal Germain

from partie import Partie
from damier import Damier
from piece import Piece
from position import Position

###########################################################################

print("Tests de la classe Position...")

pos99 = Position(9,9)

set_diag_haut = set([Position(8,8), Position(8,10)])
set_diag_bas = set([Position(10,8), Position(10,10)])
assert set(pos99.positions_diagonales_bas()) == set_diag_bas
assert set(pos99.positions_diagonales_haut()) == set_diag_haut
assert set(pos99.quatre_positions_diagonales()) == set_diag_bas.union(set_diag_haut)

set_sauts = set([Position(7,7), Position(7,11), Position(11,7), Position(11,11)])
assert set(pos99.quatre_positions_sauts()) == set_sauts

###########################################################################

print("Tests de la classe Damier...")
d1 = Damier()

for i in range(8):
    assert not d1.position_est_dans_damier(Position(i,8)) and not d1.position_est_dans_damier(Position(i,-1))
    assert not d1.position_est_dans_damier(Position(8, i))  and not d1.position_est_dans_damier(Position(-1, i))
    for j in range(8):
        assert d1.position_est_dans_damier(Position(i,j)), "Probleme: " + str((i,j))


d1.cases = {Position(7,7):Piece('blanc', 'pion'), Position(6,6):Piece('noir', 'pion'), Position(5,5):Piece('noir', 'pion')}
print(d1)

assert not d1.piece_de_couleur_peut_se_deplacer('blanc')
assert d1.piece_de_couleur_peut_se_deplacer('noir')
assert not d1.piece_de_couleur_peut_faire_une_prise('blanc')
assert not d1.piece_de_couleur_peut_faire_une_prise('noir')

assert d1.piece_peut_se_deplacer_vers(Position(6,6), Position(7,5))
assert not d1.piece_peut_se_deplacer_vers(Position(5,5), Position(4,4))
assert not d1.piece_peut_se_deplacer_vers(Position(6,6), Position(7,6))
assert not d1.piece_peut_se_deplacer_vers(Position(6,6), Position(5,5))
assert not d1.piece_peut_se_deplacer_vers(Position(7,7), Position(8,6))

for i, j in [(8,8), (5,5), (7,5)]:
    assert not d1.piece_peut_sauter_vers(Position(6,6), Position(i,j)), "Probleme: (6,6) --> " + str((i,j))
    assert not d1.piece_peut_sauter_vers(Position(7,7), Position(i,j)), "Probleme: (7,7) --> " + str((i,j))

for i,j in [(0,0), (1,1), (7,7), (5,8)]:
    assert not d1.piece_peut_se_deplacer(Position(i,j)), "Probleme: " + str((i,j))

for i in range(8):
    for j in range(8):
        assert not d1.piece_peut_faire_une_prise(Position(i,j)), "Probleme: " + str((i,j))

assert d1.deplacer(Position(0,0), Position(1,1)) == 'erreur'
assert d1.deplacer(Position(5,5), Position(6,6)) == 'erreur'
assert d1.deplacer(Position(5,5), Position(4,4)) == 'erreur'

print("Déplacement (6,6) --> (7,5)")
assert d1.deplacer(Position(6,6), Position(7,5)) == 'ok'
print(d1)

assert d1.recuperer_piece_a_position(Position(7,5)) is not None
assert d1.recuperer_piece_a_position(Position(7,5)).est_dame()

assert d1.piece_peut_se_deplacer_vers(Position(7,5), Position(6,4))
assert d1.piece_peut_se_deplacer_vers(Position(7,5), Position(6,6))

print("Déplacement (7,7) --> (6,6)")
assert d1.deplacer(Position(7,7), Position(6,6)) == 'ok'
print(d1)

assert d1.piece_de_couleur_peut_faire_une_prise('blanc')
assert d1.piece_de_couleur_peut_faire_une_prise('noir')
assert d1.piece_de_couleur_peut_se_deplacer('blanc')
assert d1.piece_de_couleur_peut_se_deplacer('noir')

for pos in d1.cases:
    assert d1.piece_peut_faire_une_prise(pos), "Probleme: " + str(pos)

print("Déplacement (7,5) --> (5,7)")
assert d1.deplacer(Position(7,5), Position(5,7)) == 'prise'
print(d1)

assert d1.recuperer_piece_a_position(Position(7,5)) is None
assert d1.recuperer_piece_a_position(Position(6,6)) is None
assert d1.recuperer_piece_a_position(Position(5,7)) is not None

assert not d1.piece_de_couleur_peut_faire_une_prise('blanc')
assert not d1.piece_de_couleur_peut_faire_une_prise('noir')
assert not d1.piece_de_couleur_peut_se_deplacer('blanc')
assert d1.piece_de_couleur_peut_se_deplacer('noir')

###########################################################################

print("Tests de la classe Partie...")

p1 = Partie()
p1.damier.cases = {Position(1,1):Piece('blanc', 'pion'),
                   Position(4,4):Piece('blanc', 'pion'),
                   Position(5,5):Piece('noir', 'pion'),
                   Position(3,5):Piece('noir', 'pion')}

print(p1.damier)

p1.couleur_joueur_courant = 'blanc'
assert p1.position_source_valide(Position(4,4))[0]
for (i,j) in [(-1,0), (0,0), (5,5), (3,5)]:
    assert not p1.position_source_valide(Position(i,j))[0], "Probleme: " + str((i,j))

p1.couleur_joueur_courant = 'noir'
assert not p1.position_source_valide(Position(4,4))[0]
assert p1.position_source_valide(Position(3,5))[0]
assert p1.position_source_valide(Position(5,5))[0]

p1.doit_prendre = True
p1.position_source_forcee = Position(5,5)
assert not p1.position_source_valide(Position(3,5))[0]
assert p1.position_source_valide(Position(5,5))[0]

p1.position_source_selectionnee = Position(5,5)
assert p1.position_cible_valide(Position(3,3))[0]
for i in range(-1,9):
    for j in range(-1,9):
        if (i,j) != (3,3):
            assert not p1.position_cible_valide(Position(i,j))[0], "Probleme: " + str((i,j))

p1.couleur_joueur_courant = 'blanc'
p1.doit_prendre = True
p1.position_source_forcee = None
p1.position_source_selectionnee = Position(4,4)
assert p1.position_cible_valide(Position(2,6))[0]
assert p1.position_cible_valide(Position(6,6))[0]
for i in range(-1,9):
    for j in range(-1,9):
        if (i,j) != (2,6) and (i,j) != (6,6):
            assert not p1.position_cible_valide(Position(i,j))[0], "Probleme: " + str((i,j))

del p1.damier.cases[Position(4,4)]

p1.couleur_joueur_courant = 'blanc'
p1.doit_prendre = False
p1.position_source_forcee = None
p1.position_source_selectionnee = Position(1,1)
assert p1.position_cible_valide(Position(0,0))[0]
assert p1.position_cible_valide(Position(0,2))[0]
for i in range(-1,9):
    for j in range(-1,9):
        if (i,j) != (0,0) and (i,j) != (0,2):
            assert not p1.position_cible_valide(Position(i,j))[0], "Probleme: " + str((i,j))

###########################################################################

print("Fin des tests...")
