from datetime import date, timedelta
from pprint import pprint

import requests


def get_rates(currencies, days=30):
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    print(start_date, end_date)

    symbols = ','.join(currencies)
    requete = f"https://api.exchangerate.host/timeseries?start_date={start_date}&end_date={end_date}&symbols={symbols}"
    r = requests.get(requete)
    if not r and not r.json():
        return False, False

    api_rates = r.json().get("rates")
    all_rates = {currency: [] for currency in currencies}
    """all_rates stock un dictionnaire contenant chaque currency rentre en parametre de fonction
    comme etant une cle de avec une liste vide comme valeur par exemple, si XOF et USD ont ete rentre
    en parametre alors all_rates = {'XOF': [], 'USD': []}"""
    all_days = sorted(api_rates.keys())
    for each_day in all_days:
        [all_rates[currency].append(rate) for currency, rate in api_rates[each_day].items()]
        """api_rates:
           On obtient une liste de plusieurs dictionnaires de ce type avec api_rates en fonction
           du parametre days:
           {2021-04-28: {'USD': 1.2, 'XOF': 655}}
           sauf que generalement la liste n'est pas dans le bon ordre on peut avoir le 2021-04-28 ensuite le
           2021-04-30. Pour contrer ce probleme, une version sorted de cette liste de dates est stockee dans all_days qui 
           est une array, ainsi la loop for each_day in all_days permet d'acceder aux elements de cette liste. Maintenant 
           avec api_rates[each_day], on accede a la valeur correspondant a la cle each_day. Si par exemple 
           {2021-04-28: {'USD': 1.2, 'XOF': 655}} et que each_day = '2021-04-28' 
           alors api_rates[each_day] = {'USD': 1.2, 'XOF': 655}. 
           
           api_rates[each_day].items()
           il permet d'acceder a une liste de deux tupple comprenant
           deux valeurs chacune: le currency et son rate a la date each_day.
           [('USD', 1.212179), ('XOF', 655.957)]
           
           for currency, rate in api_rates[each_day].items()
           on accede a chacun des elements des deux
           tupples de la liste ainsi, si la liste est: [('USD', 1.212179), ('XOF', 655.957)] alors la premiere iteration
           de cette loop for va donner: currency = 'USD' et rate = 1.212179
           
           all_rates[currency]
           permet d'acceder a la valeur correspondant a la cle currency, si currency = 'USD',
           all_rates['USD'] = [], une liste vide (voir ligne 19)
           
           
           -all_rates[currency].append(rate)
           permettra d'ajouter rate a la liste all_rates[currency] qui est toujours vide avant la premiere iteration.
           par exemple si currency = 'USD' et que rate = 1.20195 a la premiere iteration, 
           on aura all_rates['USD'] = [1.20195]"""

    return all_days, all_rates


if __name__ == '__main__':
    days, rates = get_rates(currencies=["USD", "XOF"])
    pprint(days)
    pprint(rates)
