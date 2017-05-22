1. Na naszym trello przypiête s¹ dane pogodowe, które otrzymaliœmy od Agnieszki.
Nale¿y je pobraæ.

2. W folderze nazwanym WheatherApi s¹ kolejne foldery, których nazwami s¹ nazwy poszczególnych lotnisk.
W nich zaœ s¹ jsony, do których jednak trzeba dodaæ znak nowej linii, bo inaczej logstash nie bêdzie
móg³ ich przeczytaæ. W celu ³atwego dodania znaku nowej linii u¿y³em zwyczajnie programu notepad++.
Nale¿y zauwa¿yæ, ¿e ka¿dy z jsonów koñczy siê charakterystyczn¹ sekwencj¹ nawiasów: "}		]	}}".
Klikamy ctrl+shift+f w notatniku i ustawiamy konfiguracjê, któr¹ pokaza³em w pliku notepad.jpg
W Directory nale¿y podaæ œcie¿kê do folderu WheatherApi, zaznaczyæ In all sub-folders, 
zaznaczyæ Extended, ¿eby rozpoznawa³o "\n" i klikn¹æ Replace in Files. Ca³oœæ zamieniania mo¿e trwaæ
parê minut, ale na koniec bêdziemy mieli ju¿ w pe³ni prygotowane jsony.

3. Odpalamy wszystkie 3 narzêdzia. Tym razem jako parametr logstasha mamy drugi plik konfiguracyjny,
który wrzuci³em do tego folderu (nazwany jsonconf.conf).
Przypominam, odpalenie logstasha: logstash -f jsonconf.conf.
Danych pogodowych jest mnóstwo, tymbardziej ¿e podzieli³em sobie wszystko na poszczególne pomiary godzinowe.
Wrzuca³y mi siê one przez oko³o 7 godzin.
--------------------------------------------------------
W zasadzie to wszystko lecz jeszcze parê s³ów dotycz¹cych pliku konfiguracyjnego.
Jego napisanie by³o jeszcze bardziej skomplikowane ni¿ poprzednio w przypadku pliku csv.

w sekcji input nale¿y podaæ œcie¿kê (path) do jsonów. Oczywiœcie */*.json oznacza wszystkie pliki z rozszerzeniem
json z podfolderów folderu WheatherApi. codec i type ustawione na json, aby logstash wiedzia³ co staramy siê wrzuciæ.
sincedb_path na wszelki wypadek ustawione na "NUL", a start_position na beginning. Dziêki temu, jak np przerwiecie 
import jsonów, to zaczynaj¹c od pocz¹tku nie powinno byæ ¿adnego b³êdu zwi¹zanego z powtórnym czytaniem tego samego pliku.

W sekcji filter split odpowiada za podzielenie jsona na poszczególne godziny obserwacji. Wydaje mi siê ¿e tak ³atwiej 
bêdzie badaæ pliki. 
W grok tworzê dwie nowe zmienne, ktorych nie ma w pocz¹tkowym jsonie lecz widoczne bêd¹ w kibanie. 
airport - nazwa podfolderu, dziêki temu bêdzie mo¿na jakoœ ³¹czyæ loty i dane pogodowe po oznaczeniu lotniska.
time - dodatkowe pole, które raczej bêdzie nieu¿ywane ale musia³em je dodaæ bo inaczej airport pobiera³o ca³¹ œcie¿kê
do koñca (np airport = DUB/Dublin_20163012 zamiast samo DUB).
W sekcji mutate tworzê pole eventDate, które docelowo bêdzie timestampem w kibanie.
U¿ywam do tego poszczególnych pól zawartych w jsonach, bo nie ma w nich daty która pasowa³aby idealnie na timestamp.
Problematycznym by³oby np zamiana angielskich oznaczeñ AM/PM na czas 24-godzinny. Zauwa¿y³em jednak ¿e jsony maj¹ 
takie pola jak year, mon, mday, hour, min, których po³¹czenie da taki sam timestamp jak w przypadków zaimportowanych
ju¿ lotów (z dodaniem sekund i milisekund ustawionych na 0).
Datê w odpowiednim formacie tworzê poni¿ej w "date"

w sekcji output index nazwa³em flightsairportindex bo bêdziemy porównywaæ te dane z tymi zawatymi w poprzednio 
utworzonym indeksie "flights". Aby to docelowo by³o mo¿liwe, a przynajmniej by³o proste, nale¿y podobno nazwaæ
oba indeksy tak samo zaczynaj¹co siê nazw¹ (czyli u nas "flights" jest tym cz³onem).