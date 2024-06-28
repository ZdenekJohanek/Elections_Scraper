import argparse
import re
import sys
import csv
from requests import get
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup


def validni_adresa(adresa):
    # Ověrení, že argument je platná URL adresa a odpovídá specifickému formátu.
    parsed = urlparse(adresa)
    if not all([parsed.scheme, parsed.netloc, parsed.path]):
        return False

    # Ověření základní struktury URL
    if parsed.scheme != "https" or parsed.netloc != "volby.cz" or not parsed.path.startswith("/pls/ps2017nss/ps32"):
        return False

    # Ověření dotazovacích parametrů
    query_params = parse_qs(parsed.query)
    required_params = {"xjazyk", "xkraj", "xnumnuts"}
    if not required_params.issubset(query_params.keys()):
        return False

    return True


def validni_csv(soubor):
    # Ověření, že argument je soubor s příponou .csv.
    return re.match(r"^.+\.csv$", soubor) is not None


def get_arguments():
    # funkce ke ziskání a ověření vstupních argumentů
    parser = argparse.ArgumentParser(description="Ověření argumentů skriptu.")
    parser.add_argument(dest="adresa", type=str, help="URL adresa")
    parser.add_argument(dest="jmeno_souboru", type=str, help="Název souboru s příponou .csv")

    args = parser.parse_args()

    if not args.adresa:
        print("Chyba: URL adresa chybí.")
        sys.exit(1)
    if not args.jmeno_souboru:
        print("Chyba: Název souboru chybí.")
        sys.exit(1)
    if not validni_adresa(args.adresa):
        print(f"Chyba: {args.adresa} není platná URL adresa nebo neodpovídá očekávanému formátu.")
        sys.exit(1)
    if not validni_csv(args.jmeno_souboru):
        print(f"Chyba: {args.jmeno_souboru} není platný soubor s příponou .csv.")
        sys.exit(1)

    print(f"Argumenty jsou platné.\nURL: {args.adresa}\nCSV soubor: {args.jmeno_souboru}")
    return parser.parse_args()


def parse(adresa):
    # funkce k parsovani stranky
    odpoved = get(adresa)
    rozdelene_html = BeautifulSoup(odpoved.text, features="html.parser")
    return rozdelene_html


def odkaz_obce(adresa2, sufix):
    # funkce vrací adresu konkrétní obce
    adresa2.append(sufix)
    novy_odkaz = '/'.join(adresa2)
    adresa2.pop()
    return novy_odkaz


def soucet_hlasu(leva, prava):
    # funkce k sjednocení listů hlasů
    return leva + prava


def zapis(zapis_tabulka, jmeno_souboru, slovnik):
    # funkce k zápisu celého listu obsahujicí slovníky jednotlivých obcí
    nove_csv = open(jmeno_souboru, mode="w", newline="")
    zahlavi = slovnik.keys()
    zapisovac = csv.DictWriter(nove_csv, delimiter=";", dialect="excel", fieldnames=zahlavi)
    zapisovac.writeheader()
    for i in zapis_tabulka:
        zapisovac.writerow(i)
    nove_csv.close()


def main():
    zapis_tabulka = []
    args = get_arguments()
    adresa = args.adresa

    # příprava pro vytvoření adresy k jednotlivým obcím
    adresa2 = adresa.split("/")
    adresa2.pop()

    # příprava slovníku pro dohledávání všech hodnot pro zápis do tabulky
    kod_obce = parse(adresa).find_all("td", {"class": "cislo"})
    nazev_obce = parse(adresa).find_all("td", {"class": "overflow_name"})
    slovnik_obce = {}
    i = 0
    for a in kod_obce:
        slovnik_obce[a] = nazev_obce[i]
        i += 1

    # zde procházím připravený slovník(slovnik_obce) jednotlivých obcí výše k dohledání všech hodnot,
    # které zapíši do slovníku(slovník)
    slovnik = {}
    for code, nazev in slovnik_obce.items():
        slovnik["Kód obce"] = code.get_text()
        slovnik["Název obce"] = nazev.get_text()

        # získání odkazu obce pro dohledání údajů(Registered, Envelopes, Valid)
        tabulka = parse(odkaz_obce(adresa2, code.find('a')['href']))
        slovnik["Registered"] = tabulka.find("td", {"headers": "sa2"}).get_text().replace("\xa0", "")
        slovnik["Envelopes"] = tabulka.find("td", {"headers": "sa3"}).get_text().replace("\xa0", "")
        slovnik["Valid"] = tabulka.find("td", {"headers": "sa6"}).get_text().replace("\xa0", "")

        # získání všech názvů stran a jejich hlasů dané obce(jedna obec ze slovnik_obce)
        strany = tabulka.find_all("td", {"class": "overflow_name"})
        pocty_hlasu_leva = tabulka.find_all("td", {"headers": "t1sa2 t1sb3"})
        pocty_hlasu_prava = tabulka.find_all("td", {"headers": "t2sa2 t2sb3"})
        pocty_hlasu_celkem = soucet_hlasu(pocty_hlasu_leva, pocty_hlasu_prava)

        # zde do slovníku ukládám názvy stran a jejich hlasy(jedna obec ze slovnik_obce)
        j = 0
        for i in strany:
            slovnik[i.text] = pocty_hlasu_celkem[j].text.replace("\xa0", "")
            j = j + 1

        # zapíšu slovník jedné obce do listu, který budu zapisovat do csv
        zapis_tabulka.append(slovnik.copy())

    # volám funkci pro zápis celého seznamu do csv
    zapis(zapis_tabulka, args.jmeno_souboru, slovnik)
    print("Data jsou zapsaná do:", args.jmeno_souboru)


if __name__ == "__main__":
    main()
