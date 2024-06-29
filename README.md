# Elections_Scraper
Projekt 3 - Elections_Scraper - Engeto

Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017. Zde je odkaz k nahlédnutí [zde](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

# Instalace knihoven
Knihovny, které jsou použity v kódu jsou uložené v souboru `requirements.txt`. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:
`pip3 install -r requirements.txt`. Script byl vytvořen v python verzi 3.12

# Spuštění projektu
Spuštění souboru Elections_Scraper.py v příkazovém řádku vyžaduje dva povinné argumenty.

`python Elections_Scraper.py <odkaz územního celku> <název souboru.csv>`

Po spuštění se stáhnou výsledky do souboru s příponou `.csv`

# Ukázka projektu
Výsledky hlasování pro okres Český Krumlov:
1. argument: `https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3102`
2. argument: `vysledky_cesky_krumlov.csv`

Spuštění programu:
python Elections_Scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3102" "vysledky_cesky_krumlov.csv"

Průběh stahování:

`
Argumenty jsou platné.
URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=3&xnumnuts=3102
CSV soubor: vysledky_cesky_krumlov.csv
Data jsou zapsaná do: vysledky_cesky_krumlov.csv
`

Částečný výstup:

`
Kód obce;Název obce;Registered;Envelopes;Valid;Občanská demokratická strana;.........
545406;Benešov nad Černou;1000;547;538;43;3;0;24;2;12;64;15;5;7;1;2;28;0;10;214;0;0;45;2;5;1;1;54;0
545414;Besednice;666;420;417;58;1;0;30;1;9;56;3;4;4;0;0;26;0;20;144;0;1;35;0;2;0;0;23;0
536253;Bohdalovice;234;106;105;13;0;0;9;0;1;13;0;4;0;0;0;7;0;0;37;0;0;0;0;0;0;1;20;0
545431;Brloh;839;515;510;69;0;0;25;1;26;47;6;4;12;0;1;46;1;19;143;0;4;45;0;4;0;1;54;2
.....
`
