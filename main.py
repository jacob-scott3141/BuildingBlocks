import utils as u
import matplotlib.pyplot as plt
import numpy as np


def get_data(n: int, iterations: int, crossover: str, file_to_write: str):
    s = []
    g = []
    with open(file_to_write, 'a', buffering=1) as f:
        for i in range(n):
            for _ in range(iterations):
                islands = u.make_islands(50, 200)
                _, iters = u.do_sim(islands, crossover_type=crossover, show_best_genotype=True)
                if iters != -1:
                    f.write(f"{(i + 1) * 10}, {iters}\n")
                    g.append(iters)
                    s.append((i + 1) * 10)
            u.increment()
    return s, g


def format_data(file: str):
    s = []
    g = []

    with open(file, 'r') as f:
        gens = []
        current_size = 10

        for line in f:
            size, gen = line.split(", ")

            if int(size) > current_size:
                g.append(gens)
                s.append(current_size)
                gens = []
                current_size = int(size)

            gens.append(int(gen.strip()))
        g.append(gens)
        s.append(current_size)
    return s, g


if __name__ == '__main__':
    # get_data(3, 100, 'uniform', "data3.csv")
    #
    # g1 = u.Genotype().init_from_genotype(np.zeros(20, dtype=int))
    # g2 = u.Genotype().init_from_genotype(np.ones(20, dtype=int))
    # u.crossover(g1, g2, 'uniform')

    sizes, generations = format_data('data1.csv')

    data1 = {
        'x': sizes,
        'y': [sum(g)/len(g) for g in generations],
        'yerr': [[sum(g)/len(g) - min(g) for g in generations], [max(g) - sum(g)/len(g) for g in generations]],
        'ymin': [min(g) for g in generations],
        'ymax': [max(g) for g in generations]
    }

    sizes, generations = format_data('data2.csv')

    data2 = {
        'x': sizes,
        'y': [sum(g) / len(g) for g in generations],
        'yerr': [[sum(g)/len(g) - min(g) for g in generations], [max(g) - sum(g)/len(g) for g in generations]],
        'ymin': [min(g) for g in generations],
        'ymax': [max(g) for g in generations]
    }

    sizes, generations = format_data('data3.csv')

    data3 = {
        'x': sizes,
        'y': [sum(g) / len(g) for g in generations],
        'yerr': [[sum(g) / len(g) - min(g) for g in generations], [max(g) - sum(g) / len(g) for g in generations]],
        'ymin': [min(g) for g in generations],
        'ymax': [max(g) for g in generations]
    }

    for data in [data1, data2, data3]:
        print(data['yerr'])
        plt.errorbar(x=data['x'], y=data['y'], yerr=data['yerr'], fmt='--o', alpha=0.9, capsize=3, capthick=1)
        data = {
            'x': data['x'],
            'y1': data['ymin'],
            'y2': data['ymax']}
        # plt.fill_between(**data, alpha=.25)



    plt.yscale("log")
    plt.xlabel("n")
    plt.ylabel("generations to peak")
    plt.show()
