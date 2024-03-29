from Fok100 import Coeff
from plots import piechart

def run(plotting):
    Fokker = Coeff()
    data = {
        'OEW': 30,
        'Fuel': 20,
        'Payload': 15,
    }
    piechart(data, plotting)


if __name__ == '__main__':
    plot = True
    run(plot)