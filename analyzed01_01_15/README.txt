Pierwsza analiza naszych danych:
Wp�yw pr�dko�ci wiatru na op�nienia lot�w w Dublinie dnia 01.01.2015

*Otworzenie dw�ch dokument�w xlsx w trybie read_only
*Wybranie interesuj�cych danych z kolumn
*Przedstawienie zale�no�ci na wykresie

CO NALE�Y POPRAWI�:
*Iteracja po danych - dla innych dni ni� 01.01.15 zajmie zdecydowanie zbyt wiele czasu (107.000 rekord�w)
*Wy�uskanie lot�w tylko z Dublina (teraz s� r�wnie� uj�te z innych lotnisk mimo �e pogoda jest dla Dublina)
*Oznaczenie WX oznacza op�nienie przez pogod� - uwzgl�dni� by si� odr�nia�o na wykresie
*Podpisy osi i generalny wygl�d wykresu
*Wczytywanie danych przez api wunderground zamiast przez excela - b�dzie to spore uproszczenie