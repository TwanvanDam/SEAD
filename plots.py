import matplotlib.pyplot as plt

def piechart(data, plot):
    categories, weights = list(data.keys()) ,list(data.values())

    plt.figure()
    plt.pie(weights, labels=categories, autopct=lambda p: '{:,.0f} [kg]  \n {:.1f}%'.format((p / 100) * sum(weights), p), startangle=90)
    plt.axis('equal')
    plt.title('Distribution of weights')
    plt.savefig("./Plots/piechart.pdf")
    if plot:
        plt.show()
