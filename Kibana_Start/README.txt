1. Pobraæ ze strony https://www.elastic.co/products Logstash, ElasticSearch i Kibana.
Nie trzeba ich instalowaæ, jedynie rozpakowaæ.

2. ElasticSearch dzia³a na porcie 9200, Kibana na porcie 5601, Logstash 9600

3. W katalogu bin narzêdzia logstash nale¿y stworzyæ plik (ja nazwa³em go logstash.conf)
W nim nale¿y wyspecyfikowaæ jak sprasowany zostanie dokument csv (ElasticSearch nie obs³uguje
formatów xlsx itp).

Sekcja input: path - œcie¿ka do pliku csv, który otrzymaliœmy ostatnio od firmy
start_position - potrzebne przy parsowaniu dokumentu, be¿ tego parsowanie zaczyna³oby siê
od dowolnego momentu w którym poprzednio zakoñczyliœmy, tak mamy pewnoœæ ¿e za ka¿dym razem
rozpocznie siê od pocz¹tku.
(Drobna uwaga bo mia³em z tym problemy - je¿eli logstash przeczyta plik csv, mo¿e "nie chcieæ"
zrobiæ tego po raz kolejny. Wtedy nale¿y usun¹æ pliki o nazwie sincedb i wszystko wróci do normy)

Sekcja filter: csv - wymieniamy kolumny z pliku csv, podajemy separator (bo nie musi byæ to
przecinek) oraz dodatkowo poda³em kolumny które maj¹ nie zostaæ zaimportowane, bo w sumie
s¹ zbêdne do naszych badañ
mutate - tutaj trzeba podaæ wszelkie konwersje typów (na integer, float, string, boolean)
Potrzebna jest nam w zasadzie jedynie konwersja Delay na integer. Gdy tego nie zrobimy,
zmienna ta bêdzie widoczna w kibanie jako string i mia³em problemy z generacj¹ jakichkolwiek
wykresów. (Wartoœci NULL z csv bêd¹ widoczne jako 0)
date - trzeba podaæ dok³adny format daty jaki logstash bêdzie czytaæ z pliku, w przeciwnym
razie bêdzie wyrzucaæ b³êdy. Wybra³em kolumnê Dep_Sched_Time jako t¹, która bêdzie
"timestampem".

Sekcja output: specyfikujemy gdzie logstash bêdzie przesy³aæ parsowane dane - czyli do 
elasticsearch. Definiujemy adres hosta oraz nazwê indeksu - ustawi³em flights.

4. Teraz mo¿na przejœæ do odpalenia wszystkich narzêdzi. Najpierw nale¿y odpaliæ elasticsearch.
W katalogu bin nale¿y otworzyæ elasticsearch.bat lub zrobiæ to z cmd.
Nastêpnie logstash - tutaj koniecznie z cmd komend¹ "logstash -f logstash.conf",
chyba ¿e jakoœ inaczej nazwaliœcie plik z konfiguracj¹
Powinien nawi¹zaæ po³¹czenie z elasticsearch i zacz¹æ przesy³aæ mu dane z pliku. 
Bêdzie to widoczne w konsoli i ca³oœæ przesy³ania bêdzie trwaæ d³uuugo (u mnie oko³o 2 godzin)
Teraz mo¿na odpaliæ ju¿ kibanê (kibana.bat)

5. Wchodz¹c na localhost:5601 znajdujemy siê w panelu kibany. Nale¿y za³o¿yæ index, dziêki
któremu bêdziemy widzieæ nasze dane. Nazwaliœmy go flights wiêc nale¿y wpisaæ
jak¹œ nazwê która bêdzie do niego pasowaæ (przyk³adowo: flights, flights*, fl*, fligh* itd)

6. W time-field name naszego indexu nale¿y wybraæ Dep_Sched_Time lub @timestamp
W pierwszym z przypadków bêdziemy widzieæ nasze rekordy w ³adny sposób w zak³adce discover.
W drugim z przypadków wszystkie rekordy skupi¹ siê w dniu przesy³u danych i bêdzie widoczny
jeden wielki s³upek na osi czasu.

7. Je¿eli nie widaæ ¿adnej osi czasu nale¿y zmieniæ zakres czasowy w prawym górnym rogu
(domyœlnie wybrane jest tam 15 minut chyba).

8. Teraz mo¿na w zak³adce Visualize wizualizowaæ ró¿ne rzeczy, lecz jeszcze tego nie robi³em.
Nie mniej jednak dane z csv mamy ju¿ widoczne w kibanie :)