#########################
#01.04.2017
#Wind speed vs delays
#########################
import openpyxl
import datetime
import matplotlib.pyplot as plt
import matplotlib.axes as ax
import numpy as np
import urllib2
import json

#check your path
flights = "D:\Studia\Semestr VI\Projekt_zespolowy\MyFlights.xlsx"
fl = openpyxl.load_workbook(flights, read_only=True)

print("Wpisz dane w konwencji DD-MM-RRRR")
day = str(raw_input("Wpisz dzien: "))
month = str(raw_input("Wpisz miesiac: "))
year = str(raw_input("Wpisz rok: "))

dateStr = year + "-" + month + "-" + day
flsheet = fl[dateStr]

myAPIkey = "4b30cfae89ac2135"
dateStr = year+month+day
jsonStyle = "http://api.wunderground.com/api/" + myAPIkey + "/history_" + dateStr + "/q/ie/Dublin.json"
f = urllib2.urlopen(jsonStyle)
json_string = f.read()
json_parsed = json.loads(json_string)

flightTime = []
flightDelay = []
WXTime = []
WXDelay = []
dayTime = []
dayWind = []
gustTime = []
gustSpeed = []

#Pobranie z wybranego arkusza danych do list na temat lotow
for row in range(2,flsheet.max_row):
        if (flsheet._get_cell(row,11).value == 'DUB'):
            if (flsheet._get_cell(row,14).value == 'WX'):                               # WX - czynniki pogodowe-utworzenie dla nich odrębnej listy
                WXTime.append(flsheet._get_cell(row,4).value)
                if (flsheet._get_cell(row,15).value == 'NULL'):
                    WXDelay.append(0)
                else:
                    WXDelay.append(flsheet._get_cell(row,15).value)
            else:
                flightTime.append(flsheet._get_cell(row,4).value)
                if(flsheet._get_cell(row,15).value == 'NULL'):
                    flightDelay.append(0)
                else:
                    flightDelay.append(flsheet._get_cell(row,15).value)

#Wyodrebnienie z uzyskanego jsona interesujacych danych na temat wiatru
for i in json_parsed['history']['observations']:
    if(i['metar'][:5] == 'METAR'):                                                      #pobranie danych ze stacji METAR (odczyty co pol godziny, szczegolowsze dane)
        time = i['date']['hour'] + ":" + i['date']['min']
        dayTime.append(datetime.datetime.strptime(time, '%H:%M').time())                #pobranie godziny z odczytu i zapisanie jej w odpowiednim formacie 'datatime'
        dayWind.append(i['wspdm'])                                                      #dodanie predkosci wiatru do listy
        if(i['wgustm']!='-9999.0'):                                                     #sprawdzenie czy odczytana jest predkosc wiatru w porywach (-9999.0 == NULL w jsonie)
            gustTime.append(datetime.datetime.strptime(time, '%H:%M').time())           #jezeli jest podana wartosc w porywach doklejamy ja do listy oraz zapisujemy czas odczytu
            gustSpeed.append(i['wgustm'])

plt.figure(1)
ax1 = plt.subplot(211)
delay, = plt.plot_date(flightTime, flightDelay)
WX, = plt.plot_date(WXTime, WXDelay)
plt.title("Wplyw predkosci wiatru na opoznienia w lotach (dnia " + day + "." + month + "." + year + ")")
plt.ylabel("czas w minutach")
plt.xlabel("")
plt.legend([delay,WX],['Opoznienie','Czynnik pogodowy'],loc=2)
plt.subplot(212,sharex=ax1)
plt.ylabel("predkosc wiatru [km/h]")
plt.xlabel("godzina")
wind, = plt.plot(dayTime,dayWind)
gust, = plt.plot_date(gustTime,gustSpeed)
plt.legend([wind,gust],['Predkosc wiatru','W porywach'], loc=2)
plt.show()