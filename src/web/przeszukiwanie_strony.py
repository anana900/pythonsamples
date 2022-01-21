'''
Created on Jan 13, 2022

@author: anana
'''

from requests import get
from time import time

def znajdz_stolice(lista_panstw = []):
    '''
    Wyszukuje nazwy stolic dla podanej listy państw
    kożystając ze strony angielskiej wikipedii.
    '''
    
    TAGET_URL = "https://en.wikipedia.org"
    stolice=dict()
    
    for p in lista_panstw:
        strona = get(TAGET_URL+"/wiki/{}".format(p))
    
        t = strona.text
        t = t.split(" ")
        
        for l in t:
            if "Capital" in l:
                stolica = t[t.index(l)+5][12:-1]        # wyznaczone drogą eksperymentalną
                stolice.update({p:stolica})
                break

    return stolice

if __name__ == '__main__':
    czas_rozpoczecia = time()
    
    panstwa = ['Poland', 'Germany', 'Sweden', 'Ukraine', 'Belorus', 'Russia', 'Austia', 'France']
    for item in znajdz_stolice(panstwa).items():
        print(item)
    
    print("Czas wykonania {}".format(time() - czas_rozpoczecia))    