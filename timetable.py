import random
class Profesor:
    def __init__(self, horario, id):
        self.horario = horario  # Definimos 0 como disponible
        self.id = id
    def consultarHorario(self, libre):
        return self.horario[libre] == 0

class Materia:
    def __init__(self, horas, ano, profesor, nombre):
        self.modulosSemanales = horas
        self.docente = profesor
        self.ano = ano
        self.nombre = nombre


def armarCalendarioVacio(modulos, salones):
    res = []
    for x in range(modulos):
        res.append([])
        for i in range(salones):
            res[x].append((-1, -1, -1, -1))
    return res


def solve(listaSupremaHorarios,profe,mates):
    find = materia_sin_asignar(mates)
    if not find:
        return True

    for i in range(len(listaHorarios)):
        index = valid(listaSupremaHorarios, i, (find.ano, find.docente),profe)
        if not index == -1:
            listaSupremaHorarios[i][index] = (index, find.nombre, find.docente, find.ano)
            find.modulosSemanales = find.modulosSemanales - 1

            if solve(listaSupremaHorarios,profe,mates):
                return True

            listaSupremaHorarios[i][index] = (-1, -1, -1, -1)
            find.modulosSemanales = find.modulosSemanales + 1

    return False


def valid(listaHorario, num, anoProfe,profes):
    horario = listaHorario[num]
    for hor in horario:
        if hor[3] == anoProfe[0]:
            return -1
        if anoProfe[1] == hor[2]:
            return -1
        if not profes[anoProfe[1]].consultarHorario(num):
            return -1

    cont = 0
    for hor in horario:
        if hor == (-1, -1, -1, -1):
            return cont
        cont = cont + 1
    return -1



def materia_sin_asignar(mates):

    for x in mates:
        if (not x.modulosSemanales == 0):
            return x

    return None

def print_board(bo):
    for i in range(len(bo)):
        strRes = ""
        for j in range(len(bo[0])):
            strRes += str(bo[i][j])
        print(strRes)





listaHorarios = armarCalendarioVacio(18, 3)
profesLista = [

    Profesor([0 for x in range(18)], 0),
    Profesor([0 for x in range(18)], 1),
    Profesor([1 if x % 3 == 0 else 0 for x in range(18)], 2),
    Profesor([1 if x % 2 == 0 else 0 for x in range(18)], 3),
    Profesor([1 if x % 4 == 0 else 0 for x in range(18)], 4),
    Profesor([0 for x in range(18)], 5),

]
materiasLista = [
    Materia(4, 1, 1, "matematicas"),
    Materia(2, 1, 2, "fisica"),
    Materia(2, 1, 3, "sistemas digitales"),
    Materia(3, 1, 4, "programacion"),
    Materia(4, 1, 1, "introduccion a la ing"),

    Materia(3, 2, 1, "p2"),
    Materia(5, 2, 5, "PyE"),
    Materia(1, 2, 3, "SD 2"),
    Materia(3, 2, 0, "Algoritmos"),
    Materia(3, 2, 2, "antropologia"),

    Materia(1, 3, 4, "Algoritmos 2"),
    Materia(1, 3, 3, "BD"),
    Materia(7, 3, 0, "Redes"),
    Materia(3, 3, 4, "SO"),
    Materia(3, 3, 2, "SE"),

]
random.shuffle(materiasLista)
solve(listaHorarios,profesLista,materiasLista)
print_board(listaHorarios)
