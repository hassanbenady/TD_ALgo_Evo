import random
import math
import itertools

random.seed(42)


INF = 1000
ARETES = {
    (1, 2): 14, (1, 3): 15, (1, 8): 17,
    (2, 3): 13, (2, 4): 14, (2, 5): 20, (2, 8): 21,
    (3, 4): 11, (3, 5): 21, (3, 6): 17, (3, 7): 9, (3, 8): 9,
    (4, 5): 11, (4, 6): 10, (4, 7): 8, (4, 8): 20,
    (5, 6): 15, (5, 7): 18,
    (6, 7): 9,
    (7, 8): 13,
}
VILLES = list(range(1, 9))


def dist(a, b):
    return ARETES.get((a, b), ARETES.get((b, a), INF))


def longueur(tour):
    return sum(dist(tour[k], tour[(k + 1) % len(tour)]) for k in range(len(tour)))


def affiche(tour):
    return "-".join(map(str, tour + [tour[0]]))


def taboue_tsp(max_iter=30, tenure=3):
    courant = [1, 2, 3, 4, 5, 6, 7, 8]
    meilleur, meilleur_l = courant[:], longueur(courant)
    taboue = {}
    print("Solution initiale :", affiche(courant), "longueur =", meilleur_l)

    for it in range(1, max_iter + 1):
        candidats = []

        for i, j in itertools.combinations(range(1, len(courant)), 2):
            v = courant[:]
            v[i], v[j] = v[j], v[i]
            l = longueur(v)
            mv = frozenset((courant[i], courant[j]))
            if taboue.get(mv, 0) < it or l < meilleur_l:
                candidats.append((l, mv, v))
        if not candidats:
            break
        l, mv, v = min(candidats, key=lambda t: t[0])
        courant = v
        taboue[mv] = it + tenure
        if l < meilleur_l:
            meilleur, meilleur_l = v[:], l
        print(f"  it {it:2d} | {affiche(courant)} | L = {l} | meilleur = {meilleur_l}")
    return meilleur, meilleur_l


def recuit_simule(T0=30.0, alpha=0.7, n_iter=5):
    courant = [1, 2, 3, 4, 5, 6, 7, 8]
    l_courant = longueur(courant)
    meilleur, meilleur_l = courant[:], l_courant
    T = T0
    print("Solution initiale :", affiche(courant), "longueur =", l_courant)

    for it in range(1, n_iter + 1):


        while True:
            i, j = random.sample(range(1, len(courant)), 2)
            voisin = courant[:]
            voisin[i], voisin[j] = voisin[j], voisin[i]
            l_voisin = longueur(voisin)
            if l_voisin < INF:
                break
        delta = l_voisin - l_courant

        if delta <= 0:
            accepte, p = True, 1.0
        else:
            p = math.exp(-delta / T)
            accepte = random.random() < p

        print(f"  it {it} | T = {T:6.2f} | voisin {affiche(voisin)} L = {l_voisin} "
              f"| delta = {delta:+d} | p = {p:.3f} | {'accepté' if accepte else 'refusé'}")
        if accepte:
            courant, l_courant = voisin, l_voisin
            if l_courant < meilleur_l:
                meilleur, meilleur_l = courant[:], l_courant
        T *= alpha
    return meilleur, meilleur_l


def croisement_ox(p1, p2):
    n = len(p1)
    a, b = sorted(random.sample(range(1, n), 2))
    enfant = [None] * n
    enfant[0] = 1
    enfant[a:b + 1] = p1[a:b + 1]
    reste = [v for v in p2 if v not in enfant]
    for k in range(1, n):
        if enfant[k] is None:
            enfant[k] = reste.pop(0)
    return enfant


def mutation(tour, p=0.2):
    t = tour[:]
    if random.random() < p:
        i, j = random.sample(range(1, len(t)), 2)
        t[i], t[j] = t[j], t[i]
    return t


def selection_tournoi(pop, k=3):
    return min(random.sample(pop, k), key=longueur)


def genetique(taille_pop=40, generations=60, p_mut=0.3):
    def individu():
        autres = VILLES[1:]
        random.shuffle(autres)
        return [1] + autres


    pop = [[1, 2, 3, 4, 5, 6, 7, 8]]
    while len(pop) < taille_pop:
        ind = individu()
        if longueur(ind) < INF and ind not in pop:
            pop.append(ind)
    meilleur = min(pop, key=longueur)

    for g in range(1, generations + 1):
        nouvelle = [meilleur[:]]
        while len(nouvelle) < taille_pop:
            p1, p2 = selection_tournoi(pop), selection_tournoi(pop)
            nouvelle.append(mutation(croisement_ox(p1, p2), p_mut))
        pop = nouvelle
        cand = min(pop, key=longueur)
        if longueur(cand) < longueur(meilleur):
            meilleur = cand[:]
        if g % 5 == 0 or g == 1:
            print(f"  génération {g:2d} | meilleur = {affiche(meilleur)} L = {longueur(meilleur)}")
    return meilleur, longueur(meilleur)


if __name__ == "__main__":
    print("=" * 60)
    print("Q1 : Recherche taboue (TSP)")
    print("=" * 60)
    t, l = taboue_tsp()
    print("\nMeilleur tour :", affiche(t), "| longueur =", l)

    print("\n" + "=" * 60)
    print("Q2 : Recuit simulé (5 itérations)")
    print("=" * 60)
    t, l = recuit_simule()
    print("\nMeilleur tour :", affiche(t), "| longueur =", l)

    print("\n" + "=" * 60)
    print("Q3 : Algorithme génétique")
    print("=" * 60)
    t, l = genetique()
    print("\nMeilleur tour :", affiche(t), "| longueur =", l)
