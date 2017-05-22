1. Na naszym trello przypi�te s� dane pogodowe, kt�re otrzymali�my od Agnieszki.
Nale�y je pobra�.

2. W folderze nazwanym WheatherApi s� kolejne foldery, kt�rych nazwami s� nazwy poszczeg�lnych lotnisk.
W nich za� s� jsony, do kt�rych jednak trzeba doda� znak nowej linii, bo inaczej logstash nie b�dzie
m�g� ich przeczyta�. W celu �atwego dodania znaku nowej linii u�y�em zwyczajnie programu notepad++.
Nale�y zauwa�y�, �e ka�dy z json�w ko�czy si� charakterystyczn� sekwencj� nawias�w: "}		]	}}".
Klikamy ctrl+shift+f w notatniku i ustawiamy konfiguracj�, kt�r� pokaza�em w pliku notepad.jpg
W Directory nale�y poda� �cie�k� do folderu WheatherApi, zaznaczy� In all sub-folders, 
zaznaczy� Extended, �eby rozpoznawa�o "\n" i klikn�� Replace in Files. Ca�o�� zamieniania mo�e trwa�
par� minut, ale na koniec b�dziemy mieli ju� w pe�ni prygotowane jsony.

3. Odpalamy wszystkie 3 narz�dzia. Tym razem jako parametr logstasha mamy drugi plik konfiguracyjny,
kt�ry wrzuci�em do tego folderu (nazwany jsonconf.conf).
Przypominam, odpalenie logstasha: logstash -f jsonconf.conf.
Danych pogodowych jest mn�stwo, tymbardziej �e podzieli�em sobie wszystko na poszczeg�lne pomiary godzinowe.
Wrzuca�y mi si� one przez oko�o 7 godzin.
--------------------------------------------------------
W zasadzie to wszystko lecz jeszcze par� s��w dotycz�cych pliku konfiguracyjnego.
Jego napisanie by�o jeszcze bardziej skomplikowane ni� poprzednio w przypadku pliku csv.

w sekcji input nale�y poda� �cie�k� (path) do json�w. Oczywi�cie */*.json oznacza wszystkie pliki z rozszerzeniem
json z podfolder�w folderu WheatherApi. codec i type ustawione na json, aby logstash wiedzia� co staramy si� wrzuci�.
sincedb_path na wszelki wypadek ustawione na "NUL", a start_position na beginning. Dzi�ki temu, jak np przerwiecie 
import json�w, to zaczynaj�c od pocz�tku nie powinno by� �adnego b��du zwi�zanego z powt�rnym czytaniem tego samego pliku.

W sekcji filter split odpowiada za podzielenie jsona na poszczeg�lne godziny obserwacji. Wydaje mi si� �e tak �atwiej 
b�dzie bada� pliki. 
W grok tworz� dwie nowe zmienne, ktorych nie ma w pocz�tkowym jsonie lecz widoczne b�d� w kibanie. 
airport - nazwa podfolderu, dzi�ki temu b�dzie mo�na jako� ��czy� loty i dane pogodowe po oznaczeniu lotniska.
time - dodatkowe pole, kt�re raczej b�dzie nieu�ywane ale musia�em je doda� bo inaczej airport pobiera�o ca�� �cie�k�
do ko�ca (np airport = DUB/Dublin_20163012 zamiast samo DUB).
W sekcji mutate tworz� pole eventDate, kt�re docelowo b�dzie timestampem w kibanie.
U�ywam do tego poszczeg�lnych p�l zawartych w jsonach, bo nie ma w nich daty kt�ra pasowa�aby idealnie na timestamp.
Problematycznym by�oby np zamiana angielskich oznacze� AM/PM na czas 24-godzinny. Zauwa�y�em jednak �e jsony maj� 
takie pola jak year, mon, mday, hour, min, kt�rych po��czenie da taki sam timestamp jak w przypadk�w zaimportowanych
ju� lot�w (z dodaniem sekund i milisekund ustawionych na 0).
Dat� w odpowiednim formacie tworz� poni�ej w "date"

w sekcji output index nazwa�em flightsairportindex bo b�dziemy por�wnywa� te dane z tymi zawatymi w poprzednio 
utworzonym indeksie "flights". Aby to docelowo by�o mo�liwe, a przynajmniej by�o proste, nale�y podobno nazwa�
oba indeksy tak samo zaczynaj�co si� nazw� (czyli u nas "flights" jest tym cz�onem).