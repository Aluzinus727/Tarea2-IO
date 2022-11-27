import math
import copy
import random
import numpy as np

from representation import Representation


class SimulatedAnnealing:
    def __init__(
        self,
        min_temperature: float,
        alfa: float,
        temperature: int,
        seed: int = None
    ):
        self.representation = Representation()

        self.min_temperature = min_temperature

        self.alfa = alfa
        self.temperature = temperature
        self.actual_temperature = temperature

        if seed is not None:
            random.seed(seed)

    def run(
        self, 
        n_problems: int
    ):
        """
            Recibe un número que corresponde a la cantidad de veces a resolver el problema.
            Muestra por pantalla el costo de la mejor solución encontrada para cada problema, la media y la desviación estándar.
        """
        costs = []

        for _ in range(n_problems):
            cost = self._run()
            costs.append(cost)

            # Se reinician los valores iniciales de temperatura y número de iteraciones.
            self.actual_temperature = self.temperature

        for i, cost in enumerate(costs, start=1):
            print(i, cost)

        print(f'Media: {np.average(costs)}')
        print(f'Desviación estándar: {np.std(costs)}')

    def _run(self):
        """
            Lógica principal del simulated annealing.
        """
        solution = best_solution = self.get_initial_solution()

        while not self.check_finish():
            new_solution = self.get_neighboor(solution)
            if new_solution is None:
                solution = self.get_initial_solution()
                continue

            if self.check_acceptance(new_solution, solution):
                solution = new_solution

            if self.representation.get_cost(solution) < self.representation.get_cost(best_solution):
                best_solution = solution

            self.cooling()

        print(self.representation.get_cost(best_solution), best_solution)
        return self.representation.get_cost(best_solution)

    def get_initial_solution(self):
        """
            Retorna la solución inicial de manera aleatoria.
            Se verifica que la solución inicial sea válida.
        """
        solution = {}
        keys = self.representation.get_instalations_keys()

        while not self.representation.check_answer(solution):
            for i in keys:
                solution[i] = random.randint(0, 1)

        return solution

    def cooling(self):
        """
            Se enfría la temperatura.
        """
        self.actual_temperature *= self.alfa

    def get_neighboor(self, s: dict):
        """
            Crea el vecindario mediante la heuristica bit-flip y retorna un vecino aleatoriamente.
            Se ignoran las soluciones no válidas, y si no encuentra ningun vecino con solución valida, retorna None.
        """
        valid_solutions = []
        for i, bit in s.items():
            new_solution = copy.deepcopy(s)
            if bit == 0:
                new_solution[i] = 1
            else:
                new_solution[i] = 0

            if self.representation.check_answer(new_solution):
                valid_solutions.append(new_solution)

        if len(valid_solutions) == 0:
            return None
    
        return valid_solutions[random.randint(0, len(valid_solutions) - 1)]

    def check_acceptance(self, s1, s2):
        """
            Criterio de aceptación (metrópolis).
        """
        difference = self.representation.get_cost(s1) - self.representation.get_cost(s2)
        if difference < 0:
            return True
        
        if self.actual_temperature == 0:
            return False
        
        p = pow(math.e, -(difference)/self.actual_temperature)
        
        if random.uniform(0, 1) < p:
            return True

        return False

    def check_finish(self):
        """
            Criterio de término.
            Si la temperatura actual es menor a la temperatura mínima, finaliza.
        """
        return self.actual_temperature <= self.min_temperature