import csv
import random


class Representation:
    def __init__(self):
        self.instalations = {}

        self.load_data()


    def load_data(self):
        """
            Carga el archivo csv que contiene la información del problema.
            El archivo contiene la siguiente información de cada comuna:
            ID, nombre, costo de instalar una instalación en ese lugar y IDs de comunas adyacentes.
        """

        with open('data/data.csv', newline='') as File:
            reader = csv.reader(File)
            next(reader, None)  # skip the headers
            for row in reader:
                _id, name, cost, adjacent = row
                self.instalations[int(_id)] = {
                    'name': name,
                    'cost': float(cost),
                    'adjacent': list(map(int, adjacent.split(' ')))
                }


    def get_initial_solution(self):
        """
            Retorna la solución inicial de manera aleatoria.
        """
        solution = {}

        while not self.check_answer(solution):
            for i in self.instalations.keys():
                solution[i] = random.randint(0, 1)

        return solution

    def check_answer(self, answer: dict):
        """
            Verifica si una solución es válida (cubre a todas las comunas).
            Retorna verdadero si es válida, falso en caso contrario.
        """
        if len(answer.keys()) != len(self.instalations.keys()):
            return

        covered = []
        for i in answer.keys():
            if answer[i]:
                covered.append(i)
                covered += self.instalations[i]['adjacent']

        covered = list(set(covered))

        if len(covered) == len(self.instalations.keys()):
            return True
        
        return

    def get_cost(self, answer: dict):
        """
            Retorna el costo total de una solución.
        """
        total_cost = 0
        for i in answer.keys():
            total_cost += self.instalations[i]['cost'] * answer[i]

        return total_cost