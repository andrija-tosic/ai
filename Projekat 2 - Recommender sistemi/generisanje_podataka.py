import pandas as pd
from random import randint


def generisanje_podataka(broj_pesama=500, broj_zanrova=10, broj_izvodjaca=300, broj_slusaoca=3000, velicina_dataseta=10000):
    return pd.DataFrame(
        {
            'id_pesme': [randint(1, broj_pesama) for _ in range(velicina_dataseta)],
            'id_izvodjaca': [randint(1, broj_izvodjaca) for _ in range(velicina_dataseta)],
            'zanr_pesme': [randint(1, broj_zanrova) for _ in range(velicina_dataseta)],
            'id_slusaoca': [randint(1, broj_slusaoca) for _ in range(velicina_dataseta)],
            'trajanje_pesme': [randint(1, 6) for _ in range(velicina_dataseta)],
            'ocena_pesme': [randint(1, 10) for _ in range(velicina_dataseta)],
            'godina_izdavanja': [randint(2000, 2023) for _ in range(velicina_dataseta)],
            'jezik': [randint(1, 7) for _ in range(velicina_dataseta)]
        }
    ).drop_duplicates()


if __name__ == '__main__':
    d = generisanje_podataka()
    d.to_csv('podaci.csv', index=False)
