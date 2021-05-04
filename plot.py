
''' Read data from csv file and plot the results
'''
import csv
import os

import matplotlib.pyplot as plt



def plot_communication():
    t_ideal = []
    r_ideal = []
    t_nc = []
    r_nc = []

    with open('experiments/non-communicativeApr_23_2021/performance2.csv') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            t_nc.append(int(row['timestep']))
            r_nc.append(float(row['reward']))

    with open('experiments/non-communicativeApr_24_2021/performance2.csv') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            t_nc.append(1249353 + int(row['timestep']))
            r_nc.append(float(row['reward']))

    with open('experiments/idealApr_27_2021/performance2.csv') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            t_ideal.append(int(row['timestep']))
            r_ideal.append(float(row['reward']))
    with open('experiments/idealApr_28_2021/performance2.csv') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            t_ideal.append(1249353 + int(row['timestep']))
            r_ideal.append(float(row['reward']))

    fig, ax = plt.subplots()
    ax.plot(t_nc, r_nc, 'r', label='Non-communicative strategy')

    ax.plot(t_ideal, r_ideal, 'b', label='Ideal communication strategy ')

    ax.set(xlabel='timestep', ylabel='reward')
    ax.legend()
    ax.grid()

    save_dir = os.path.dirname('./experiments')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    fig.savefig('test.png')


if __name__ == '__main__':
    plot_communication()

