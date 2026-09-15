def find_n(elements, needle, n):
    """
    Devuelve True si encuentra n o más apariciones del elemento.

    No hace falta que estén seguidas.
    """
    if n >= 0:
        index = 0
        count = 0

        while count < n and index < len(elements):
            if needle == elements[index]:
                count += 1

            index += 1

        return count >= n

    else:
        return False


def find_one(elements, needle):
    """
    Comprueba si el elemento aparece al menos una vez.
    """
    return find_n(elements, needle, 1)


def find_strike(elements, needle, n):
    """
    Busca una racha de n elementos iguales y seguidos.

    Si aparece un elemento distinto, la racha se rompe
    y empezamos a contar otra vez desde cero.
    """
    if n >= 0:
        index = 0
        count = 0

        while count < n and index < len(elements):

            if needle == elements[index]:
                count += 1

            else:
                # Se rompe la racha y volvemos a empezar.
                count = 0

            index += 1

        return count >= n

    else:
        return False


def make_list(length, filler):
    """
    Crea una lista del tamaño indicado rellenándola
    con el mismo valor.
    """
    result = []
    index = 0

    while index < length:
        result.append(filler)
        index += 1

    return result


def index_first_element(elements, needle):
    """
    Busca la primera aparición de un elemento
    y devuelve su posición.
    """
    index = 0

    while index < len(elements):

        if needle == elements[index]:
            return index

        else:
            index += 1

    # Si no lo encontramos devolvemos None.
    return None


def map_list(elements, transform):
    """
    Crea una lista nueva aplicando una función
    a cada elemento de la lista original.
    """
    result = []

    for element in elements:
        result.append(transform(element))

    return result


def make_list_from_factory(length, factory):
    """
    Crea una lista usando una función o clase como fábrica.

    En nuestro caso nos sirve para crear varios LinearBoard
    independientes.
    """
    result = []
    index = 0

    while index < length:

        # Llamamos a la fábrica cada vez para crear
        # un objeto nuevo.
        result.append(factory())

        index += 1

    return result


def transpose(matrix):
    """
    Intercambia las filas y las columnas de una matriz.

    También funciona si la matriz no es cuadrada.
    """
    if not matrix:
        return []

    height = len(matrix[0])
    result = []

    for i in range(height):
        sub_result = []

        for j in range(len(matrix)):
            sub_result.append(matrix[j][i])

        result.append(sub_result)

    return result


def displace(l, distancia, filler=None):
    """
    Desplaza los elementos de una lista.

    Los huecos que aparecen al moverla se rellenan
    con filler.
    """
    n = len(l)
    result = []

    for i in range(n):

        # Calculamos de qué posición original
        # tiene que salir este elemento.
        index = i - distancia

        if 0 <= index < n:
            result.append(l[index])

        else:
            result.append(filler)

    return result


def displace_matrix(matrix, filler=None):
    """
    Desplaza cada columna de la matriz una cantidad diferente.

    Esto nos sirve para convertir una diagonal
    en una línea horizontal.
    """
    result = []

    for i in range(len(matrix)):

        # Cada columna se mueve i - 1 posiciones.
        result.append(
            displace(matrix[i], i - 1, filler)
        )

    return result


def reverse_list(elements):
    """
    Devuelve la lista en orden inverso.
    """
    return elements[::-1]


def reverse_matrix(matrix):
    """
    Invierte cada una de las columnas de la matriz.

    Lo usamos para transformar una diagonal ascendente
    en una diagonal descendente.
    """
    result = []

    for col in matrix:
        result.append(reverse_list(col))

    return result


def all_the_same_score(elements):
    """
    Comprueba si todos los elementos tienen la misma puntuación.

    Nos sirve para saber si podemos elegir una recomendación
    al azar porque todas son equivalentes.
    """
    if not elements:
        return True

    first_element = elements[0]
    result = True

    for element in elements:

        if element != first_element:
            result = False

    return result


def colpase_matrix(matrix, empty='.', sep='|'):
    """
    Convierte una matriz completa en una cadena de texto.

    Cada columna se separa con |.
    """
    result = ''

    for elt in matrix:
        result = result + sep + colapse_list(elt, empty)

    # Quitamos el primer separador que sobra.
    return result[1:]


def colapse_list(elements, empty='.'):
    """
    Convierte una lista en texto.

    Las posiciones vacías, que son None,
    las representamos con un punto.
    """
    result = ''

    for elt in elements:

        if elt is None:
            result = result + empty

        else:
            result = result + elt

    return result


def explode_list(list_of_strings):
    """
    Convierte una lista de textos en una lista de listas.

    Por ejemplo:
    ['x..o', 'oxoo']
    pasa a listas de caracteres.
    """
    result = []

    for element in list_of_strings:
        result.append(list(element))

    return result


def replace_all(matrix, old, new):
    """
    Sustituye un valor por otro en toda la matriz.
    """
    new_matrix = []

    for element in matrix:
        new_matrix.append(
            replace_in_list(element, old, new)
        )

    return new_matrix


def replace_in_list(elements, old, new):
    """
    Sustituye todas las apariciones de un valor
    dentro de una lista.
    """
    result = []

    for elt in elements:

        if elt == old:
            result.append(new)

        else:
            result.append(elt)

    return result
