Pierwsza analiza naszych danych:
Wp³yw prêdkoœci wiatru na opóŸnienia lotów w Dublinie dnia 01.01.2015

*Otworzenie dwóch dokumentów xlsx w trybie read_only
*Wybranie interesuj¹cych danych z kolumn
*Przedstawienie zale¿noœci na wykresie

CO NALE¯Y POPRAWIÆ:
*Iteracja po danych - dla innych dni ni¿ 01.01.15 zajmie zdecydowanie zbyt wiele czasu (107.000 rekordów)
*Wy³uskanie lotów tylko z Dublina (teraz s¹ równie¿ ujête z innych lotnisk mimo ¿e pogoda jest dla Dublina)
*Oznaczenie WX oznacza opóŸnienie przez pogodê - uwzglêdniæ by siê odró¿nia³o na wykresie
*Podpisy osi i generalny wygl¹d wykresu
*Wczytywanie danych przez api wunderground zamiast przez excela - bêdzie to spore uproszczenie