
import pandas as pd
from numpy import dot
from numpy.linalg import norm

from saradnicko_filtriranje import normalizacija


def one_hot_kodiranje(df, kolona):
    ''' Funkcija koja vrši one-hot kodiranje kolone i vraća je u DataFrame '''
    one_hot_enkodiranje_df = pd.get_dummies(df[kolona])
    one_hot_enkodiranje_df.reset_index(drop=True, inplace=True)
    return pd.concat([df, one_hot_enkodiranje_df], axis=1)


# Funkcija koja odredjuje kosinusnu slicnost dva ulazna vektora
def cos_slicnost(v1, v2):
    return sum(dot(v1, v2)/(norm(v1)*norm(v2)))


if __name__ == '__main__':

    # Uvoz podataka
    df = pd.read_csv('podaci.csv')

    # Normalizacija kolona
    df['trajanje_pesme_norm'] = normalizacija(df['trajanje_pesme'].values)
    df['ocena_pesme_norm'] = normalizacija(df['ocena_pesme'].values)

    # One-hot kodiranje
    df = one_hot_kodiranje(df, kolona='godina_izdavanja')
    df = one_hot_kodiranje(df, kolona='zanr_pesme')
    df = one_hot_kodiranje(df, kolona='jezik')

    # Uklanjanje premapiranih kolona
    cols = ['trajanje_pesme', 'ocena_pesme',
            'jezik', 'zanr_pesme', 'godina_izdavanja']
    df.drop(columns=cols, inplace=True)

    # Izračunavanje sličnosti vektora sa id-jevima knjiga u odnosu na sve ostale vektore
    df.set_index('id_pesme', inplace=True)

    inputVec = df.loc[df.index[0]].values
    df['predikcija'] = df.apply(
        lambda x: cos_slicnost(inputVec, x.values), axis=1)

    # Rezultat filtriranja
    rezultat = df.nlargest(columns='predikcija', n=5)

    print(rezultat)
