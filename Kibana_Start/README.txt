1. Pobra� ze strony https://www.elastic.co/products Logstash, ElasticSearch i Kibana.
Nie trzeba ich instalowa�, jedynie rozpakowa�.

2. ElasticSearch dzia�a na porcie 9200, Kibana na porcie 5601, Logstash 9600

3. W katalogu bin narz�dzia logstash nale�y stworzy� plik (ja nazwa�em go logstash.conf)
W nim nale�y wyspecyfikowa� jak sprasowany zostanie dokument csv (ElasticSearch nie obs�uguje
format�w xlsx itp).

Sekcja input: path - �cie�ka do pliku csv, kt�ry otrzymali�my ostatnio od firmy
start_position - potrzebne przy parsowaniu dokumentu, be� tego parsowanie zaczyna�oby si�
od dowolnego momentu w kt�rym poprzednio zako�czyli�my, tak mamy pewno�� �e za ka�dym razem
rozpocznie si� od pocz�tku.
(Drobna uwaga bo mia�em z tym problemy - je�eli logstash przeczyta plik csv, mo�e "nie chcie�"
zrobi� tego po raz kolejny. Wtedy nale�y usun�� pliki o nazwie sincedb i wszystko wr�ci do normy)

Sekcja filter: csv - wymieniamy kolumny z pliku csv, podajemy separator (bo nie musi by� to
przecinek) oraz dodatkowo poda�em kolumny kt�re maj� nie zosta� zaimportowane, bo w sumie
s� zb�dne do naszych bada�
mutate - tutaj trzeba poda� wszelkie konwersje typ�w (na integer, float, string, boolean)
Potrzebna jest nam w zasadzie jedynie konwersja Delay na integer. Gdy tego nie zrobimy,
zmienna ta b�dzie widoczna w kibanie jako string i mia�em problemy z generacj� jakichkolwiek
wykres�w. (Warto�ci NULL z csv b�d� widoczne jako 0)
date - trzeba poda� dok�adny format daty jaki logstash b�dzie czyta� z pliku, w przeciwnym
razie b�dzie wyrzuca� b��dy. Wybra�em kolumn� Dep_Sched_Time jako t�, kt�ra b�dzie
"timestampem".

Sekcja output: specyfikujemy gdzie logstash b�dzie przesy�a� parsowane dane - czyli do 
elasticsearch. Definiujemy adres hosta oraz nazw� indeksu - ustawi�em flights.

4. Teraz mo�na przej�� do odpalenia wszystkich narz�dzi. Najpierw nale�y odpali� elasticsearch.
W katalogu bin nale�y otworzy� elasticsearch.bat lub zrobi� to z cmd.
Nast�pnie logstash - tutaj koniecznie z cmd komend� "logstash -f logstash.conf",
chyba �e jako� inaczej nazwali�cie plik z konfiguracj�
Powinien nawi�za� po��czenie z elasticsearch i zacz�� przesy�a� mu dane z pliku. 
B�dzie to widoczne w konsoli i ca�o�� przesy�ania b�dzie trwa� d�uuugo (u mnie oko�o 2 godzin)
Teraz mo�na odpali� ju� kiban� (kibana.bat)

5. Wchodz�c na localhost:5601 znajdujemy si� w panelu kibany. Nale�y za�o�y� index, dzi�ki
kt�remu b�dziemy widzie� nasze dane. Nazwali�my go flights wi�c nale�y wpisa�
jak�� nazw� kt�ra b�dzie do niego pasowa� (przyk�adowo: flights, flights*, fl*, fligh* itd)

6. W time-field name naszego indexu nale�y wybra� Dep_Sched_Time lub @timestamp
W pierwszym z przypadk�w b�dziemy widzie� nasze rekordy w �adny spos�b w zak�adce discover.
W drugim z przypadk�w wszystkie rekordy skupi� si� w dniu przesy�u danych i b�dzie widoczny
jeden wielki s�upek na osi czasu.

7. Je�eli nie wida� �adnej osi czasu nale�y zmieni� zakres czasowy w prawym g�rnym rogu
(domy�lnie wybrane jest tam 15 minut chyba).

8. Teraz mo�na w zak�adce Visualize wizualizowa� r�ne rzeczy, lecz jeszcze tego nie robi�em.
Nie mniej jednak dane z csv mamy ju� widoczne w kibanie :)