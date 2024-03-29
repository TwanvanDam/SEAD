import matplotlib.pyplot as plt

def piechart(data, plot):
    categories = list(data.keys())
    percentages = list(data.values())

    plt.figure()
    plt.pie(percentages, labels=categories, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Distribution of weights')
    total = sum(percentages)
    if plot:
        plt.show()
