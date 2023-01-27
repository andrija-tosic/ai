import pandas as pd
import numpy as np

from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds


def normalizacija(v):
    '''Funkcija koja normalizuje ulazni vektor'''
    return (v - v.min()) / (v.max() - v.min())


if __name__ == '__main__':
    # Importovanje podataka
    df = pd.read_csv('podaci.csv')

    # Generiše se pivot tabela u kojoj su čitaoci indeks, kolona su pesme, a vrednosti su ocene
    pivot_tabela_df = df.pivot_table(
        columns='id_pesme',
        index='id_slusaoca',
        values='ocena_pesme'
    ).fillna(0)

    # Konverzija u kompresovanu retko posednutu (CSR) matricu
    matrica_ocena = csr_matrix(pivot_tabela_df.values)

    # Faktorizacija matrica
    u, s, v = svds(matrica_ocena, k=10)

    # Konstrukcija dijagonalne matrice od sopstvenog vektora
    s = np.diag(s)

    # Izračunavanje predviđenih ocena skalarnim proizvodom vektora u sa dijagonalnom matricom s, i jediničnom matricom v
    # Ocene se normalizuju u skup [0, 1]
    predvidjene_ocene = np.dot(np.dot(u, s), v)
    predvidjene_ocene = normalizacija(predvidjene_ocene)

    # Konverzija vektora u pandas DataFrame
    predikcija_df = pd.DataFrame(
        predvidjene_ocene,
        columns=pivot_tabela_df.columns,
        index=list(pivot_tabela_df.index)
    ).transpose()

    korisnik_id = 5

    # Generisanje preporuka
    korisnik_predikcije = predikcija_df[korisnik_id].sort_values(
        ascending=False).reset_index().rename(columns={korisnik_id: 'predikcija'})

    # Rezultat filtriranja
    rezultat = korisnik_predikcije.sort_values(
        by='predikcija', ascending=False).head(5)

    print("Preporuke za korisnika sa id-jem {}\n".format(korisnik_id), rezultat)
