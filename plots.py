import matplotlib.pyplot as plt
import numpy as np

def piechart(data, plot):
    categories, weights = list(data.keys()) ,list(data.values())

    plt.figure()
    plt.pie(weights, labels=categories, autopct=lambda p: '{:,.0f} [kg]  \n {:.1f}%'.format((p / 100) * sum(weights), p), startangle=90)
    plt.axis('equal')
    plt.title('Distribution of weights')
    plt.savefig("./Plots/piechart.pdf")
    if plot:
        plt.show()

def control_stability(x_range, control, stability, stability_static_margin):
    plt.plot(x_range, control, color='red', label='Control')
    plt.fill_between(x_range, control, facecolor='red', alpha=0.5, label='Not controllable')
    plt.plot(x_range, stability, color='blue',label='Stability')
    plt.fill_between(x_range, stability-stability_static_margin, facecolor='blue', alpha=0.5, label='Not stable')
    plt.ylim([0,1.1*np.max([np.max(stability), np.max(control)])])
    plt.xlim([np.min(x_range), np.max(x_range)])
    plt.xlabel(r'$x$ [mac]')
    plt.ylabel(r'$S_h/S$ [-]')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    x = np.arange(0.35, 0.75, 0.01)
    stability = -1.2 + 3*x
    control = 1.5 - 2*x
    stability_static_margin = 0.05

    control_stability(x, control, stability, stability_static_margin)
