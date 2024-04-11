import numpy as np
import matplotlib.pyplot as plt

CELL_SIZE = 5  # Dimensiunea unei celule
IMAGE_PATH = "poza1.jpg"  # Calea către imaginea de intrare

def bcd_with_obstacles(numpy_map, cell_size):
    # Calcularea dimensiunii grilei de celule
    num_rows = numpy_map.shape[0] // cell_size
    num_cols = numpy_map.shape[1] // cell_size

    visited = np.zeros((num_rows, num_cols), dtype=bool)
    # group obstacles in cells where numpy_map is 1
    for i in range(num_rows):
        for j in range(num_cols):
            if numpy_map[i * cell_size:(i + 1) * cell_size, j * cell_size:(j + 1) * cell_size].any():
                visited[i, j] = True

    # Plot the map
    plt.imshow(visited, cmap='gray')
    plt.title('Map')
    plt.show()

    # Parcurgerea celulelor în zigzag evitând obstacolele
    polygons = []
    for row in range(num_rows):
        if row % 2 == 0:  # Parcurgere de la stânga la dreapta
            for col in range(num_cols):
                if not visited[row][col]:
                    polygon = traverse_cell(row, col, cell_size, visited)
                    polygons.append(polygon)
        else:  # Parcurgere de la dreapta la stânga
            for col in reversed(range(num_cols)):
                if not visited[row][col]:
                    polygon = traverse_cell(row, col, cell_size, visited)
                    polygons.append(polygon)

    return polygons


def traverse_cell(row, col, cell_size, visited):
    # Determinarea coordonatelor celulei
    x = col * cell_size
    y = row * cell_size
#

    # Parcurgerea celulei și marcarea celulelor vizitate
    polygon = [(x, y), (x + cell_size, y), (x + cell_size, y + cell_size), (x, y + cell_size)]
    visited[row][col] = True

    return polygon


# Exemplu de utilizare

def image_to_binary_matrix(image_path):
    # Citirea imaginii alb-negru
    img = plt.imread(image_path)

    # Verificare dacă imaginea a fost citită corect
    if img is None:
        print("Nu s-a putut citi imaginea.")
        return None

    # Conversia la o matrice binară
    img_gray = np.mean(img, axis=2)  # Convertirea la alb-negru
    binary_matrix = np.where(img_gray > 0.01, 1, 0)  # Conversia în matrice binară

    return binary_matrix

binary_matrix = image_to_binary_matrix(IMAGE_PATH)
polygons = bcd_with_obstacles(binary_matrix, CELL_SIZE)

map_array = np.zeros((binary_matrix.shape[0] // CELL_SIZE + 1, binary_matrix.shape[1] // CELL_SIZE + 1))
for polygon in polygons:
    p1, p2, p3, p4 = polygon
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    map_array[y1 // CELL_SIZE, x1 // CELL_SIZE] = 1
    map_array[y2 // CELL_SIZE, x2 // CELL_SIZE] = 1
    map_array[y3 // CELL_SIZE, x3 // CELL_SIZE] = 1
    map_array[y4 // CELL_SIZE, x4 // CELL_SIZE] = 1

# reverse y axis
plt.gca().invert_yaxis()
plt.imshow(map_array, cmap='gray')
plt.title('Map')
plt.show()

