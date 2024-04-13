import numpy as np
import matplotlib.pyplot as plt

marime_celula = 4 #dimensiunea unei celule
path_imagine = "poza1.jpg" #imaginea cu obstacolele
#path_imagine = "poza2.jpeg"  #imaginea cu obstacolele

def bcd_cu_obstacole(numpy_map, marime_celula):
    #calculam dimensiunea grilei de celule
    nr_linii = numpy_map.shape[0] // marime_celula
    nr_coloane = numpy_map.shape[1] // marime_celula

    vizitat = np.zeros((nr_linii, nr_coloane), dtype=bool)
    #grupam obstacolele in celulele unde numpy_map este 1
    for i in range(nr_linii):
        for j in range(nr_coloane):
            if numpy_map[i * marime_celula:(i + 1) * marime_celula, j * marime_celula:(j + 1) * marime_celula].any():
                vizitat[i, j] = True

    #plotam harta
    plt.imshow(vizitat, cmap='gray')
    plt.title('Harta obstacole')
    plt.show()

    #parcurgem celulele in zigzag evitand obstacolele
    poligoane = []
    for linie in range(nr_linii):
        if linie % 2 == 0:  #parcurgem de la stanga la dreapta
            for col in range(nr_coloane):
                if not vizitat[linie][col]:
                    poligon = traversare_celula(linie, col, marime_celula, vizitat)
                    poligoane.append(poligon)
        else:  #parcurgem de la dreapta la stanga
            for col in reversed(range(nr_coloane)):
                if not vizitat[linie][col]:
                    poligon = traversare_celula(linie, col, marime_celula, vizitat)
                    poligoane.append(poligon)

    return poligoane
def traversare_celula(linie, coloana, marime_celula, vizitat):
    #determinarea coordonatelor celulei
    x = coloana * marime_celula
    y = linie * marime_celula

    #parcurgerea celulei si marcarea celulelor vizitate
    poligon = [(x,y), (x + marime_celula,y), (x + marime_celula,y + marime_celula), (x,y + marime_celula)]
    vizitat[linie][coloana] = True

    return poligon

def transforma_imagine_in_matrice_binara(path_imagine):
    img = plt.imread(path_imagine)#citim imaginea

    #verificam daca imaginea a fost citita corect
    if img is None:
        print("Nu s-a putut citi imaginea.")
        return None

    img_gray = np.mean(img, axis=2)  #convertirea la alb-negru
    matrice_binara = np.where(img_gray > 0.01, 1, 0)  #conversia in matrice binara

    return matrice_binara

matrice_binara = transforma_imagine_in_matrice_binara(path_imagine)
poligoane = bcd_cu_obstacole(matrice_binara, marime_celula)

map_array = np.zeros((matrice_binara.shape[0] // marime_celula + 1, matrice_binara.shape[1] // marime_celula + 1))
for poligon in poligoane:
    p1, p2, p3, p4 = poligon
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    map_array[y1 // marime_celula, x1 // marime_celula] = 1
    map_array[y2 // marime_celula, x2 // marime_celula] = 1
    map_array[y3 // marime_celula, x3 // marime_celula] = 1
    map_array[y4 // marime_celula, x4 // marime_celula] = 1

#inversam axa y
plt.gca().invert_yaxis()
plt.imshow(map_array, cmap='gray')
plt.title('Harta traseu')
plt.show()

