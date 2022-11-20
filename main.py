from simulated_annealing import SimulatedAnnealing

if __name__ == '__main__':
    sim_ann = SimulatedAnnealing(
        max_iterations=1000,
        alfa=0.01,
        temperature=2500
    )

    sim_ann.run(n_problems=10)