import random
import itertools

random.seed(42)


COUT = [[5, 3, 4],
        [6, 7, 2]]
STOCK = [8, 9]
DEMANDE = [4, 5, 8]


def cout_transport(x):
    return sum(COUT[i][j] * x[i][j]
               for i in range(len(STOCK)) for j in range(len(DEMANDE)))


def solution_initiale_coin_nord_ouest():
    stock, dem = STOCK[:], DEMANDE[:]
    x = [[0] * len(DEMANDE) for _ in STOCK]
    i = j = 0
    while i < len(stock) and j < len(dem):
        q = min(stock[i], dem[j])
        x[i][j] = q
        stock[i] -= q
        dem[j] -= q
        if stock[i] == 0:
            i += 1
        else:
            j += 1
    return x


def voisins_transport(x):
    m, n = len(STOCK), len(DEMANDE)
    for i1, i2 in itertools.permutations(range(m), 2):
        for j1, j2 in itertools.permutations(range(n), 2):
            if x[i1][j2] >= 1 and x[i2][j1] >= 1:
                y = [ligne[:] for ligne in x]
                y[i1][j1] += 1
                y[i1][j2] -= 1
                y[i2][j1] -= 1
                y[i2][j2] += 1
                yield (i1, i2, j1, j2), y


def taboue_transport(max_iter=50, tenure=3, patience=8):
    x = solution_initiale_coin_nord_ouest()
    meilleur, meilleur_cout = x, cout_transport(x)
    liste_taboue = {}
    print("Solution initiale (coin Nord-Ouest) :", x, "coût =", meilleur_cout)
    sans_amelioration = 0

    for it in range(1, max_iter + 1):
        candidats = []
        for mv, y in voisins_transport(x):
            c = cout_transport(y)
            est_tabou = liste_taboue.get(mv, 0) >= it

            if not est_tabou or c < meilleur_cout:
                candidats.append((c, mv, y))
        if not candidats:
            break
        c, mv, y = min(candidats, key=lambda t: t[0])
        x = y
        i1, i2, j1, j2 = mv

        liste_taboue[(i1, i2, j2, j1)] = it + tenure
        if c < meilleur_cout:
            meilleur, meilleur_cout = y, c
            sans_amelioration = 0
        else:
            sans_amelioration += 1
        print(f"  it {it:2d} | mouvement {mv} | coût = {c} | meilleur = {meilleur_cout}")
        if sans_amelioration >= patience:
            print("  -> arrêt : pas d'amélioration depuis", patience, "itérations")
            break
    return meilleur, meilleur_cout


if __name__ == "__main__":
    print("EXERCICE 2 - Transport de containers (recherche taboue)")
    x, c = taboue_transport()
    print("\nMeilleure solution :")
    for i, ligne in enumerate(x, 1):
        print(f"  D{i} ->", {f"M{j+1}": q for j, q in enumerate(ligne)})
    print("Coût total minimal trouvé =", c)
