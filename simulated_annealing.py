import math
import copy
import random
import numpy as np


from representation import Representation


class SimulatedAnnealing:
    def __init__(
        self,
        max_iterations: int,
        alfa: float,
        temperature: int,
    ):
        self.representation = Representation()

        self.current_iterations = 0
        self.max_iterations = max_iterations

        self.alfa = alfa
        self.temperature = temperature
        self.actual_temperature = temperature

    def run(
        self, 
        n_problems: int
    ):
        """
            Recibe un número que corresponde a la cantidad de veces a resolver el problema.
            Muestra por pantalla el costo de la mejor solución de cada resolución, la media y la desviación estándar.
        """
        costs = []

        for _ in range(n_problems):
            cost = self._run()
            costs.append(cost)

            # Se reinician los valores iniciales de temperatura y número de iteraciones.
            self.actual_temperature = self.temperature
            self.current_iterations = 0

        for i, cost in enumerate(costs, start=1):
            print(i, cost)

        print(f'Media: {np.average(costs)}')
        print(f'Desviación estándar: {np.std(costs)}')

    def _run(self):
        """
            Lógica principal del simulated annealing.
        """
        solution = self.representation.get_initial_solution()

        while not self.check_finish():
            new_solution = self.get_neighboor(solution)
            if new_solution is None:
                solution = self.representation.get_initial_solution()
                continue

            if self.check_acceptance(new_solution, solution):
                solution = new_solution

            self.cooling()
            self.current_iterations += 1

        print(self.representation.get_cost(solution), solution)
        return self.representation.get_cost(solution)


    def cooling(self):
        """
            Se enfría la temperatura.
        """
        self.actual_temperature = self.alfa * self.actual_temperature

    def get_neighboor(self, s: dict):
        """
            Crea el vecindario mediante la heuristica bit-flip y retorna el vecino con la mejor solución.
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
        
        best_solution = valid_solutions[0]
        for i in valid_solutions:
            if self.representation.get_cost(i) <= self.representation.get_cost(best_solution):
                best_solution = i

        return best_solution

    def check_acceptance(self, s1, s2):
        """
            Criterio de aceptación.
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
        """
        if self.current_iterations >= self.max_iterations:
            return True
        
        return False