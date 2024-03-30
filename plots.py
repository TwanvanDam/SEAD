import matplotlib.pyplot as plt

def piechart(data, plot):
    categories, percentages = list(data.keys()) ,list(data.values())

    plt.figure()
    plt.pie(percentages, labels=categories, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Distribution of weights')
    total = sum(percentages)
    if plot:
        plt.show()
