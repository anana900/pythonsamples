'''
Created on Jan 19, 2022

@author: anana
'''

import os

from src.web.przeszukiwanie_strony import znajdz_stolice

DIR_PATH = 'dousuniecia'

def create_file(dir_path: str = DIR_PATH, filename: str = None):
    if filename is None:
        return None
    
    if dir_path not in os.listdir():
        os.mkdir(dir_path)
        
    with open('./' + dir_path + f'/{filename}', 'w+') as _:
        pass

def remove_file(dir_path: str = DIR_PATH, filename: str = None):
    if filename is None:
        return None
    
    sciezka_pliku = dir_path + '/' + filename
    
    if os.path.exists(sciezka_pliku):
        try:
            os.remove(sciezka_pliku)
        except OSError as err:
            print(f"Problem z usunięciem pliku: {err}")
        else:
            print(f"{sciezka_pliku} został usunięty")
    else:
        print(f"UWAGA Nie ma takiego pliku: {sciezka_pliku}")

def get_file_list(dir_path: str = DIR_PATH, plik_pattern: str = ''):
    if plik_pattern == '':
        return os.listdir(dir_path)
    else:
        return [f for f in os.listdir(dir_path) if plik_pattern in f]

def read_file(dir_path: str = DIR_PATH, filename: str = None, mode: str = 'r'):
    with open(dir_path+'/'+filename, mode) as f:
        return f.read()

def write_file(dir_path: str = DIR_PATH, filename: str = None, mode: str = 'w', data: str = None):
    with open(dir_path+'/'+filename, mode) as f:
        f.write(data)

def zapisz_stolice(dir_path: str = DIR_PATH, filename: str = None, data: list = None):
    wynik = [str(znajdz_stolice([p])[p]) for p in data]
    write_file(filename=filename, data = '\n'.join(wynik))

if __name__ == '__main__':
    panstwa_europa_full = (
        "Russia", "Germany", "United Kingdom", "France",
        "Italy", "Spain", "Ukraine", "Poland",
        "Romania", "Netherlands", "Belgium", "Czech Republic (Czechia)",
        "Greece", "Portugal", "Sweden", "Hungary",
        "Belarus", "Austria", "Serbia", "Switzerland",
        "Bulgaria", "Denmark", "Finland", "Slovakia",
        "Norway", "Ireland", "Croatia", "Moldova",
        "Bosnia and Herzegovina", "Albania", "Lithuania", "North Macedonia",
        "Slovenia", "Latvia", "Estonia", "Montenegro",
        "Luxembourg", "Malta", "Iceland", "Andorra",
        "Monaco", "Liechtenstein", "San Marino", "Holy See"
        )

    #print(get_file_list())
    #[remove_file(filename=item) for item in get_file_list()]
    create_file('stolice')
    
    zapisz_stolice(filename='stolice', data=panstwa_europa_full[:13])
    print(read_file(filename='stolice'))
    
    print(get_file_list())
    