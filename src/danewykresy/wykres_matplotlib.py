import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def wykres_bar():
    """
    Wykres słupkowy dla kilku wartości Y w postaci wielokrotnych słupków oraz łączonych słupków.
    Etykieta nad każdym słupkiem.
    """
    gains = [1, 2, 3]
    adapt = [0,1,0]
    bpp8 = [1,1,1]
    bpp10 = [1,1,1]
    bpp12 = [1,1,1]
    fadapt = [0,0,1]
    fbpp8 = [0,0,0]
    fbpp10 = [0,0,0]
    fbpp12 = [0,0,0]
    label_descr = ['adapt', 'bpp8', 'bpp10', 'bpp12']
    dane = pd.DataFrame({'gains': gains, 'adapt': adapt, 'bpp8': bpp8, 'bpp10': bpp10, 'bpp12': bpp12,
                          'fadapt': fadapt, 'fbpp8': fbpp8, 'fbpp10': fbpp10, 'fbpp12': fbpp12})

    plt.figure(figsize=[30, 10])
    wd = 0.3
    x_pos = np.arange(1, 2 * len(dane), 2)

    plt.bar(x_pos, dane.adapt, color='g', width=wd, edgecolor='k')
    plt.bar(x_pos, dane.fadapt, color='r', width=wd, edgecolor='k', bottom=dane.adapt)
    plt.bar(x_pos + wd, dane.bpp8, color='g', width=wd, edgecolor='k')
    plt.bar(x_pos + wd, dane.fbpp8, color='r', width=wd, edgecolor='k', bottom=dane.bpp8)
    plt.bar(x_pos + (wd * 2), dane.bpp10, color='g', width=wd, edgecolor='k')
    plt.bar(x_pos + (wd * 2), dane.fbpp10, color='r', width=wd, edgecolor='k', bottom=dane.bpp10)
    plt.bar(x_pos + (wd * 3), dane.bpp12, color='g', width=wd, edgecolor='k')
    plt.bar(x_pos + (wd * 3), dane.fbpp12, color='r', width=wd, edgecolor='k', bottom=dane.bpp12)

    plt.xticks(x_pos + wd, dane.gains.values, fontsize=15)
    plt.yticks(fontsize=15)
    plt.title('The blogs posted by gains', fontsize=20)
    plt.xlabel('gains', fontsize=17)
    plt.ylabel('Fail/Pass', fontsize=17)

    # Etykiety każda w na pozycji bar
    label_offset = 0
    for gain_no in range(1, len(dane) + 1):
        for i, label in enumerate(label_descr):
            plt.text(gain_no + label_offset + (wd * i), 1, label, ha='center', fontsize=6)
        label_offset += 1

    plt.legend(loc='upper center', fontsize=15)
    plt.show()

if __name__=='__main__':
    wykres_bar()
