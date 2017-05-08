from csv import *
from operator import itemgetter
from pylab import *
from numpy import *

file2 = open("bilancaMesec.csv","rt")

slovar = {}

#Prevzem energije od elekrarn

mesecno = DictReader(file2)

mesci = [1,2,3,4,5,6,7,8,9,10,11,12]
meseci = ["Jan","Feb","Mar","Apr","Maj","Jun","Jul","Aug","Sep","Okt","Nov","Dec"]
meseci2016 = [1,2,3,4,5,6,7,8,9]
mesci2016 = ["Jan","Feb","Mar","Apr","Maj","Jun","Jul","Aug","Sep"]
leta = ["2012","2013","2014","2015","2016"]



for row in mesecno:
    hydro = float(int(row['Prevzem - DEM na prenosnem omrezju'])+int(row['Prevzem - SEL na prenosnem omrezju'])+int(
    row['Prevzem - HESS na prenosnem omrezju'])+int(row['Prevzem - SENG na prenosnem omrezju'])+int(row['Prevzem - male HE na prenosnem omrezju']))/1000

    foto = float(int(row['Prevzem - male fotovoltaicne elektrarne na prenosnem omrezju']))/1000

    thermo = float(int(row['Prevzem - TES na prenosnem omrezju'])+int(row['Prevzem - TEB na prenosnem omrezju'])+int(
    row['Prevzem - TET na prenosnem omrezju'])+int(row['Prevzem - TE-TOL na prenosnem omrezju'])+int(row['Prevzem - SPTE na prenosnem omrezju']))/1000

    nuklear = float(int(row['Prevzem - nuklearna elektrarna na prenosnem omrezju']))/1000

    proizNaDist = float(int(row['Prevzem - proizvodnja na distribucijskem omrezju']))/1000

    uvozPrenos = float(int(row['Prevzem - uvoz na prenosnem omrezju']))/1000

    uvozDistribuci = float(int(row['Prevzem - uvoz na distribucijskem omrezju']))/1000

    prevzemSkup = float(int(row['Prevzem - skupaj']))/1000

    if int(row['leto'].split('M')[0]) == 2012 and int(row['leto'].split('M')[1]) == 1:
        slovar[2012] = [[hydro,foto,thermo,nuklear,proizNaDist,uvozPrenos,uvozDistribuci,prevzemSkup]]
    if int(row['leto'].split('M')[0]) == 2012 and int(row['leto'].split('M')[1]) > 1:
        slovar[2012].append([hydro, foto, thermo, nuklear, proizNaDist, uvozPrenos, uvozDistribuci, prevzemSkup])
    if int(row['leto'].split('M')[0]) == 2013 and int(row['leto'].split('M')[1]) == 1:
        slovar[2013] = [[hydro,foto,thermo,nuklear,proizNaDist,uvozPrenos,uvozDistribuci,prevzemSkup]]
    if int(row['leto'].split('M')[0]) == 2013 and int(row['leto'].split('M')[1]) > 1:
        slovar[2013].append([hydro, foto, thermo, nuklear, proizNaDist, uvozPrenos, uvozDistribuci, prevzemSkup])
    if int(row['leto'].split('M')[0]) == 2014 and int(row['leto'].split('M')[1]) == 1:
        slovar[2014] = [[hydro,foto,thermo,nuklear,proizNaDist,uvozPrenos,uvozDistribuci,prevzemSkup]]
    if int(row['leto'].split('M')[0]) == 2014 and int(row['leto'].split('M')[1]) > 1:
        slovar[2014].append([hydro, foto, thermo, nuklear, proizNaDist, uvozPrenos, uvozDistribuci, prevzemSkup])
    if int(row['leto'].split('M')[0]) == 2015 and int(row['leto'].split('M')[1]) == 1:
        slovar[2015] = [[hydro,foto,thermo,nuklear,proizNaDist,uvozPrenos,uvozDistribuci,prevzemSkup]]
    if int(row['leto'].split('M')[0]) == 2015 and int(row['leto'].split('M')[1]) > 1:
        slovar[2015].append([hydro, foto, thermo, nuklear, proizNaDist, uvozPrenos, uvozDistribuci, prevzemSkup])
    if int(row['leto'].split('M')[0]) == 2016 and int(row['leto'].split('M')[1]) == 1:
        slovar[2016] = [[hydro,foto,thermo,nuklear,proizNaDist,uvozPrenos,uvozDistribuci,prevzemSkup]]
    if int(row['leto'].split('M')[0]) == 2016 and int(row['leto'].split('M')[1]) > 1:
        slovar[2016].append([hydro, foto, thermo, nuklear, proizNaDist, uvozPrenos, uvozDistribuci, prevzemSkup])


hidroEl = []
fotoEl = []
termoEl = []
nuklearEl = []
proizNaDistOmr = []
uvozPrenosno = []
uvozDistribucijsko = []
prevzemSkupaj = []

for month in slovar[2012]:
    hidroEl.append(month[0])
    fotoEl.append(month[1])
    termoEl.append(month[2])
    nuklearEl.append(month[3])
    proizNaDistOmr.append(month[4])
    uvozPrenosno.append(month[5])
    uvozDistribucijsko.append(month[6])
    prevzemSkupaj.append(month[7])


hidroEl2012 = np.column_stack((np.array(hidroEl,dtype="float"), np.array(mesci,dtype="int")))
fotoEl2012 = np.column_stack((np.array(fotoEl,dtype="float"), np.array(mesci,dtype="int")))
termoEl2012 = np.column_stack((np.array(termoEl,dtype="float"), np.array(mesci,dtype="int")))
nuklearEl2012 = np.column_stack((np.array(nuklearEl,dtype="float"), np.array(mesci,dtype="int")))
proizNaDistOmrEl2012 = np.column_stack((np.array(proizNaDistOmr,dtype="float"), np.array(mesci,dtype="int")))
uvozPrenosnoEl2012 = np.column_stack((np.array(uvozPrenosno,dtype="float"), np.array(mesci,dtype="int")))
uvozDistribucijskoEl2012 = np.column_stack((np.array(uvozDistribucijsko,dtype="float"), np.array(mesci,dtype="int")))
prevzemSkupaj2012 = np.column_stack((np.array(prevzemSkupaj,dtype="float"), np.array(mesci,dtype="int")))

hidroEl = []
fotoEl = []
termoEl = []
nuklearEl = []
proizNaDistOmr = []
uvozPrenosno = []
uvozDistribucijsko = []
prevzemSkupaj = []

for month in slovar[2013]:
    hidroEl.append(month[0])
    fotoEl.append(month[1])
    termoEl.append(month[2])
    nuklearEl.append(month[3])
    proizNaDistOmr.append(month[4])
    uvozPrenosno.append(month[5])
    uvozDistribucijsko.append(month[6])
    prevzemSkupaj.append(month[7])


hidroEl2013 = np.column_stack((np.array(hidroEl,dtype="float"), np.array(mesci,dtype="int")))
fotoEl2013 = np.column_stack((np.array(fotoEl,dtype="float"), np.array(mesci,dtype="int")))
termoEl2013 = np.column_stack((np.array(termoEl,dtype="float"), np.array(mesci,dtype="int")))
nuklearEl2013 = np.column_stack((np.array(nuklearEl,dtype="float"), np.array(mesci,dtype="int")))
proizNaDistOmrEl2013 = np.column_stack((np.array(proizNaDistOmr,dtype="float"), np.array(mesci,dtype="int")))
uvozPrenosnoEl2013 = np.column_stack((np.array(uvozPrenosno,dtype="float"), np.array(mesci,dtype="int")))
uvozDistribucijskoEl2013 = np.column_stack((np.array(uvozDistribucijsko,dtype="float"), np.array(mesci,dtype="int")))
prevzemSkupaj2013 = np.column_stack((np.array(prevzemSkupaj,dtype="float"), np.array(mesci,dtype="int")))

hidroEl = []
fotoEl = []
termoEl = []
nuklearEl = []
proizNaDistOmr = []
uvozPrenosno = []
uvozDistribucijsko = []
prevzemSkupaj = []

for month in slovar[2014]:
    hidroEl.append(month[0])
    fotoEl.append(month[1])
    termoEl.append(month[2])
    nuklearEl.append(month[3])
    proizNaDistOmr.append(month[4])
    uvozPrenosno.append(month[5])
    uvozDistribucijsko.append(month[6])
    prevzemSkupaj.append(month[7])


hidroEl2014 = np.column_stack((np.array(hidroEl,dtype="float"), np.array(mesci,dtype="int")))
fotoEl2014 = np.column_stack((np.array(fotoEl,dtype="float"), np.array(mesci,dtype="int")))
termoEl2014 = np.column_stack((np.array(termoEl,dtype="float"), np.array(mesci,dtype="int")))
nuklearEl2014 = np.column_stack((np.array(nuklearEl,dtype="float"), np.array(mesci,dtype="int")))
proizNaDistOmrEl2014 = np.column_stack((np.array(proizNaDistOmr,dtype="float"), np.array(mesci,dtype="int")))
uvozPrenosnoEl2014 = np.column_stack((np.array(uvozPrenosno,dtype="float"), np.array(mesci,dtype="int")))
uvozDistribucijskoEl2014 = np.column_stack((np.array(uvozDistribucijsko,dtype="float"), np.array(mesci,dtype="int")))
prevzemSkupaj2014 = np.column_stack((np.array(prevzemSkupaj,dtype="float"), np.array(mesci,dtype="int")))

hidroEl = []
fotoEl = []
termoEl = []
nuklearEl = []
proizNaDistOmr = []
uvozPrenosno = []
uvozDistribucijsko = []
prevzemSkupaj = []

for month in slovar[2015]:
    hidroEl.append(month[0])
    fotoEl.append(month[1])
    termoEl.append(month[2])
    nuklearEl.append(month[3])
    proizNaDistOmr.append(month[4])
    uvozPrenosno.append(month[5])
    uvozDistribucijsko.append(month[6])
    prevzemSkupaj.append(month[7])


hidroEl2015 = np.column_stack((np.array(hidroEl,dtype="float"), np.array(mesci,dtype="int")))
fotoEl2015 = np.column_stack((np.array(fotoEl,dtype="float"), np.array(mesci,dtype="int")))
termoEl2015 = np.column_stack((np.array(termoEl,dtype="float"), np.array(mesci,dtype="int")))
nuklearEl2015 = np.column_stack((np.array(nuklearEl,dtype="float"), np.array(mesci,dtype="int")))
proizNaDistOmrEl2015 = np.column_stack((np.array(proizNaDistOmr,dtype="float"), np.array(mesci,dtype="int")))
uvozPrenosnoEl2015 = np.column_stack((np.array(uvozPrenosno,dtype="float"), np.array(mesci,dtype="int")))
uvozDistribucijskoEl2015 = np.column_stack((np.array(uvozDistribucijsko,dtype="float"), np.array(mesci,dtype="int")))
prevzemSkupaj2015 = np.column_stack((np.array(prevzemSkupaj,dtype="float"), np.array(mesci,dtype="int")))

hidroEl = []
fotoEl = []
termoEl = []
nuklearEl = []
proizNaDistOmr = []
uvozPrenosno = []
uvozDistribucijsko = []
prevzemSkupaj = []

for month in slovar[2016]:
    hidroEl.append(month[0])
    fotoEl.append(month[1])
    termoEl.append(month[2])
    nuklearEl.append(month[3])
    proizNaDistOmr.append(month[4])
    uvozPrenosno.append(month[5])
    uvozDistribucijsko.append(month[6])
    prevzemSkupaj.append(month[7])


hidroEl2016 = np.column_stack((np.array(hidroEl,dtype="float"), np.array(meseci2016,dtype="int")))
fotoEl2016 = np.column_stack((np.array(fotoEl,dtype="float"), np.array(meseci2016,dtype="int")))
termoEl2016 = np.column_stack((np.array(termoEl,dtype="float"), np.array(meseci2016,dtype="int")))
nuklearEl2016 = np.column_stack((np.array(nuklearEl,dtype="float"), np.array(meseci2016,dtype="int")))
proizNaDistOmrEl2016 = np.column_stack((np.array(proizNaDistOmr,dtype="float"), np.array(meseci2016,dtype="int")))
uvozPrenosnoEl2016 = np.column_stack((np.array(uvozPrenosno,dtype="float"), np.array(meseci2016,dtype="int")))
uvozDistribucijskoEl2016 = np.column_stack((np.array(uvozDistribucijsko,dtype="float"), np.array(meseci2016,dtype="int")))
prevzemSkupaj2016 = np.column_stack((np.array(prevzemSkupaj,dtype="float"), np.array(meseci2016,dtype="int")))


fig, axes = plt.subplots(1,5, figsize=(5,5))
axes[0].plot(prevzemSkupaj2012[:,1],prevzemSkupaj2012[:,0],color="darkblue",label="Skupaj")
axes[0].plot(hidroEl2012[:,1],hidroEl2012[:,0],color="blue",label="Hidro El")
axes[0].plot(fotoEl2012[:,1],fotoEl2012[:,0],color="teal",label="Foto El")
axes[0].plot(termoEl2012[:,1],termoEl2012[:,0],color="lightgreen",label="TermoEl")
axes[0].plot(nuklearEl2012[:,1],nuklearEl2012[:,0],color="green",label="Nuklear")
axes[0].plot(proizNaDistOmrEl2012[:,1],proizNaDistOmrEl2012[:,0],color="pink",label="Proiz na dist.omr")
axes[0].plot(uvozPrenosnoEl2012[:,1],uvozPrenosnoEl2012[:,0],color="yellow",label="Uvoz na prenosnem omr")
axes[0].plot(uvozDistribucijskoEl2012[:,1],uvozDistribucijskoEl2012[:,0],color="black",label="Uvoz distribucijski")
axes[0].set_xlabel("Leto 2012")
axes[0].set_ylabel("Proizvodnja v GWh")
axes[0].set_xticks(mesci)
axes[0].set_xticklabels(np.array(meseci,dtype="str"),rotation=90)
axes[0].legend(loc=9,mode="expand")
axes[0].set_ylim(0, 2200)

axes[1].plot(prevzemSkupaj2013[:,1],prevzemSkupaj2013[:,0],color="darkblue",label="Skupaj")
axes[1].plot(hidroEl2013[:,1],hidroEl2013[:,0],color="blue",label="Hidro El")
axes[1].plot(fotoEl2013[:,1],fotoEl2013[:,0],color="teal",label="Foto El")
axes[1].plot(termoEl2013[:,1],termoEl2013[:,0],color="lightgreen",label="TermoEl")
axes[1].plot(nuklearEl2013[:,1],nuklearEl2013[:,0],color="green",label="Nuklear")
axes[1].plot(proizNaDistOmrEl2013[:,1],proizNaDistOmrEl2013[:,0],color="pink",label="Proiz na dist.omr")
axes[1].plot(uvozPrenosnoEl2013[:,1],uvozPrenosnoEl2013[:,0],color="yellow",label="Uvoz na prenosnem omr")
axes[1].plot(uvozDistribucijskoEl2013[:,1],uvozDistribucijskoEl2013[:,0],color="black",label="Uvoz distribucijski")
axes[1].set_xlabel("Leto 2013")
axes[1].set_ylabel("Proizvodnja v GWh")
axes[1].set_xticks(mesci)
axes[1].set_xticklabels(np.array(meseci,dtype="str"),rotation=90)
axes[1].legend(loc=9,mode="expand")
axes[1].set_xticks(mesci)
axes[1].set_xticklabels(np.array(meseci,dtype="str"),rotation=90)
axes[1].set_ylim(0, 2200)

axes[2].plot(prevzemSkupaj2014[:,1],prevzemSkupaj2014[:,0],color="darkblue",label="Skupaj")
axes[2].plot(hidroEl2014[:,1],hidroEl2014[:,0],color="blue",label="Hidro El")
axes[2].plot(fotoEl2014[:,1],fotoEl2014[:,0],color="teal",label="Foto El")
axes[2].plot(termoEl2014[:,1],termoEl2014[:,0],color="lightgreen",label="TermoEl")
axes[2].plot(nuklearEl2014[:,1],nuklearEl2014[:,0],color="green",label="Nuklear")
axes[2].plot(proizNaDistOmrEl2014[:,1],proizNaDistOmrEl2014[:,0],color="pink",label="Proiz na dist.omr")
axes[2].plot(uvozPrenosnoEl2014[:,1],uvozPrenosnoEl2014[:,0],color="yellow",label="Uvoz na prenosnem omr")
axes[2].plot(uvozDistribucijskoEl2014[:,1],uvozDistribucijskoEl2014[:,0],color="black",label="Uvoz distribucijski")
axes[2].set_xlabel("Leto 2014")
axes[2].set_ylabel("Proizvodnja v GWh")
axes[2].set_xticks(mesci)
axes[2].set_xticklabels(np.array(meseci,dtype="str"),rotation=90)
axes[2].legend(loc=9,mode="expand")
axes[2].set_xticks(mesci)
axes[2].set_xticklabels(np.array(meseci,dtype="str"),rotation=90)
axes[2].set_ylim(0, 2200)

axes[3].plot(prevzemSkupaj2015[:,1],prevzemSkupaj2015[:,0],color="darkblue",label="Skupaj")
axes[3].plot(hidroEl2015[:,1],hidroEl2015[:,0],color="blue",label="Hidro El")
axes[3].plot(fotoEl2015[:,1],fotoEl2015[:,0],color="teal",label="Foto El")
axes[3].plot(termoEl2015[:,1],termoEl2015[:,0],color="lightgreen",label="TermoEl")
axes[3].plot(nuklearEl2015[:,1],nuklearEl2015[:,0],color="green",label="Nuklear")
axes[3].plot(proizNaDistOmrEl2015[:,1],proizNaDistOmrEl2015[:,0],color="pink",label="Proiz na dist.omr")
axes[3].plot(uvozPrenosnoEl2015[:,1],uvozPrenosnoEl2015[:,0],color="yellow",label="Uvoz na prenosnem omr")
axes[3].plot(uvozDistribucijskoEl2015[:,1],uvozDistribucijskoEl2015[:,0],color="black",label="Uvoz distribucijski")
axes[3].set_xlabel("Leto 2015")
axes[3].set_ylabel("Proizvodnja v GWh")
axes[3].set_xticks(mesci)
axes[3].set_xticklabels(np.array(meseci,dtype="str"),rotation=90)
axes[3].legend(loc=9,mode="expand")
axes[3].set_xticks(mesci)
axes[3].set_xticklabels(np.array(meseci,dtype="str"),rotation=90)
axes[3].set_ylim(0, 2200)

axes[4].plot(prevzemSkupaj2016[:,1],prevzemSkupaj2016[:,0],color="darkblue",label="Skupaj")
axes[4].plot(hidroEl2016[:,1],hidroEl2016[:,0],color="blue",label="Hidro El")
axes[4].plot(fotoEl2016[:,1],fotoEl2016[:,0],color="teal",label="Foto El")
axes[4].plot(termoEl2016[:,1],termoEl2016[:,0],color="lightgreen",label="TermoEl")
axes[4].plot(nuklearEl2016[:,1],nuklearEl2016[:,0],color="green",label="Nuklear")
axes[4].plot(proizNaDistOmrEl2016[:,1],proizNaDistOmrEl2016[:,0],color="pink",label="Proiz na dist.omr")
axes[4].plot(uvozPrenosnoEl2016[:,1],uvozPrenosnoEl2016[:,0],color="yellow",label="Uvoz na prenosnem omr")
axes[4].plot(uvozDistribucijskoEl2016[:,1],uvozDistribucijskoEl2016[:,0],color="black",label="Uvoz distribucijski")
axes[4].set_xlabel("Leto 2016")
axes[4].set_ylabel("Proizvodnja v GWh")
axes[4].set_xticks(mesci)
axes[4].set_xticklabels(np.array(meseci,dtype="str"),rotation=90)
axes[4].legend(loc=9,mode="expand")
axes[4].set_xticks(meseci2016)
axes[4].set_xticklabels(np.array(mesci2016,dtype="str"),rotation=90)
axes[4].set_ylim(0, 2200)



fig.suptitle("Prevzem energije")
plt.show()