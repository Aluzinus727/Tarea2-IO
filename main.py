from simulated_annealing import SimulatedAnnealing

if __name__ == '__main__':
    sim_ann = SimulatedAnnealing(
        min_temperature=0.01,
        alfa=0.99,
        temperature=250,
        seed=1
    )

    sim_ann.run(n_problems=10)