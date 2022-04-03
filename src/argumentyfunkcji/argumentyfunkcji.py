'''
Created on Apr 3, 2022

@author: anana
'''

def funk_argumenty(arg1, arg2):
    print(f"{funk_argumenty.__name__} {arg1} {arg2}")

def funk_argumenty_domyslne(arg1, arg2='a'):
    print(f"{funk_argumenty_domyslne.__name__} {arg1} {arg2}")

def funk_argumenty_nazwy_obowiazkowe(arg1, *, arg2):
    '''
    Po gwiazdce * argumenty należy podawać poprzez nazwę
    '''
    print(f"{funk_argumenty_nazwy_obowiazkowe.__name__} {arg1} {arg2}")

def funk_argumenty_jako_lista(arg1, *arg2):
    print(arg1)
    for a in arg2:
        print(a)

def funk_argumenty_jako_lista_nazw(arg1, **arg2):
    print(arg1)
    for argument, wartosc in arg2.items():
        print(f"{argument} {wartosc}")

def funk_argumenty_jako_lista_nazw_spakowane_listy(**arg2):
    for argument, wartosc in arg2.items():
        for w in wartosc:
            print(f"{argument}: {w}")

def funk_argumenty_jako_lista_nazw_spakowane_slowniki(**arg2):
    for argument, wartosc in arg2.items():
        for parametr, w in wartosc.items():
            print(f"{argument} {parametr}: {w}")

if __name__ == '__main__':
    funk_argumenty(1,2)
    funk_argumenty_domyslne(100)
    funk_argumenty_domyslne(100, 200)
    funk_argumenty_nazwy_obowiazkowe('a', arg2='b')
    funk_argumenty_jako_lista(1,2,3,4,5,6,7)
    funk_argumenty_jako_lista(1)
    funk_argumenty_jako_lista_nazw(1,ola=4,ala=5)
    funk_argumenty_jako_lista_nazw(1)
    funk_argumenty_jako_lista_nazw_spakowane_listy(ustawienia=(1,2,3),
                                                   konfiguracje=('a','b','c'))
    funk_argumenty_jako_lista_nazw_spakowane_slowniki(ustawienia={'a':1,'b':2},
                                                      konfiguracje={'a':'a','b':'b','c':'c'})

