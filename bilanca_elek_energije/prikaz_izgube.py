from csv import *
from operator import itemgetter
from pylab import *
from numpy import *

file = "bilancaLeto.csv"
file2 = open("bilancaMesec.csv","rt")

#Odjem - izgube na prenosnem omrezju,Odjem - izgube na distribucijskem omrezju,Odjem - skupaj

izgubePrenosno = 'Odjem - izgube na prenosnem omrezju'
izgubeDistribucijsko = 'Odjem - izgube na distribucijskem omrezju'
skupno = 'Odjem - skupaj'

izgubeOdjem = {}

mesecno = DictReader(file2)

for row in mesecno:
    for item in row:
        if item == 'leto':
            date = row[item].split("M")[0]+"|"+row[item].split("M")[1]
            izgubeP = int(row[izgubePrenosno])
            izgubeD = int(row[izgubeDistribucijsko])
            OdjemSkupaj = int(row[skupno])
            #print("Leto "+row[item].split("M")[0],"Mesec "+row[item].split("M")[1], "Izgube: ",(int(row[izgubePrenosno])+int(row[izgubeDistribucijsko])), "Skupni Odjem: "+row[skupno])
            izgubeOdjem[date] = [izgubeP,izgubeD,OdjemSkupaj]

#for month in izgubeOdjem:
    #print(month," ", izgubeOdjem[month])


#Vizualizacija
leto = []
izgubP = []
izgubD = []

skupajOdj = []



izgub2012 = []
skup2012 = []
izgub2013 = []
skup2013 = []
izgub2014 = []
skup2014 = []
izgub2015 = []
skup2015 = []
izgub2016 = []
skup2016 = []

mesci = [1,2,3,4,5,6,7,8,9,10,11,12]
meseci = ["Jan","Feb","Mar","Apr","Maj","Jun","Jul","Aug","Sep","Okt","Nov","Dec"]
meseci2016 = [1,2,3,4,5,6,7,8,9]
mesci2016 = ["Jan","Feb","Mar","Apr","Maj","Jun","Jul","Aug","Sep"]
leta = ["2012","2013","2014","2015","2016"]

temp = 2012
for item in izgubeOdjem:
    if int(item.split("|")[0]) == 2012:
        izgub2012.append((float(izgubeOdjem[item][0])+float(izgubeOdjem[item][1]))/1000)
        skup2012.append(float(izgubeOdjem[item][2])/1000)

    if int(item.split("|")[0]) == 2013:
        izgub2013.append((float(izgubeOdjem[item][0]) + float(izgubeOdjem[item][1])) / 1000)
        skup2013.append(float(izgubeOdjem[item][2]) / 1000)

    if int(item.split("|")[0]) == 2014:
        izgub2014.append((float(izgubeOdjem[item][0]) + float(izgubeOdjem[item][1])) / 1000)
        skup2014.append(float(izgubeOdjem[item][2]) / 1000)
    if int(item.split("|")[0]) == 2015:
        izgub2015.append((float(izgubeOdjem[item][0]) + float(izgubeOdjem[item][1])) / 1000)
        skup2015.append(float(izgubeOdjem[item][2]) / 1000)
    if int(item.split("|")[0]) == 2016:
        izgub2016.append((float(izgubeOdjem[item][0]) + float(izgubeOdjem[item][1])) / 1000)
        skup2016.append(float(izgubeOdjem[item][2]) / 1000)
    #MWh - GWh -> print(izgubeOdjem[item][2]/1000)


izgub2012 = np.column_stack((np.array(izgub2012,dtype="float"), np.array(mesci,dtype="int")))
skup2012 = np.column_stack((np.array(skup2012,dtype="float"), np.array(mesci,dtype="int")))
izgub2013 = np.column_stack((np.array(izgub2013,dtype="float"), np.array(mesci,dtype="int")))
skup2013 = np.column_stack((np.array(skup2013,dtype="float"), np.array(mesci,dtype="int")))
izgub2014 = np.column_stack((np.array(izgub2014,dtype="float"), np.array(mesci,dtype="int")))
skup2014 = np.column_stack((np.array(skup2014,dtype="float"), np.array(mesci,dtype="int")))
izgub2015 = np.column_stack((np.array(izgub2015,dtype="float"), np.array(mesci,dtype="int")))
skup2015 = np.column_stack((np.array(skup2015,dtype="float"), np.array(mesci,dtype="int")))
izgub2016 = np.column_stack((np.array(izgub2016,dtype="float"), np.array(meseci2016,dtype="int")))
skup2016 = np.column_stack((np.array(skup2016,dtype="float"), np.array(meseci2016,dtype="int")))


fig, axes = plt.subplots(1,5, figsize=(5,5))
axes[0].plot(izgub2012[:,1],izgub2012[:,0],color="green",label="izguba")
axes[0].plot(skup2012[:,1],skup2012[:,0],color="blue",label="skupaj")
axes[0].set_xlabel("Leto 2012")
axes[0].set_ylabel("Skupna izguba v GWh")
axes[0].set_xticks(mesci)
axes[0].set_xticklabels(np.array(meseci,dtype="str"),rotation=90)
axes[0].set_ylim(20, 2200)

axes[1].plot(izgub2013[:,1],izgub2013[:,0],color="green",label="izguba")
axes[1].plot(skup2013[:,1],skup2013[:,0],color="blue",label="skupaj")
axes[1].set_xlabel("Leto 2013")
axes[1].set_xticks(mesci)
axes[1].set_xticklabels(np.array(meseci,dtype="str"),rotation=90)
axes[1].set_ylim(20, 2200)

axes[2].plot(izgub2014[:,1],izgub2014[:,0],color="green",label="izguba")
axes[2].plot(skup2014[:,1],skup2014[:,0],color="blue",label="skupaj")
axes[2].set_xlabel("Leto 2014")
axes[2].set_xticks(mesci)
axes[2].set_xticklabels(np.array(meseci,dtype="str"),rotation=90)
axes[2].set_ylim(20, 2200)

axes[3].plot(izgub2015[:,1],izgub2015[:,0],color="green",label="izguba")
axes[3].plot(skup2015[:,1],skup2015[:,0],color="blue",label="skupaj")
axes[3].set_xlabel("Leto 2015")
axes[3].set_xticks(mesci)
axes[3].set_xticklabels(np.array(meseci,dtype="str"),rotation=90)
axes[3].set_ylim(20, 2200)

axes[4].plot(izgub2016[:,1],izgub2016[:,0],color="green",label="izguba")
axes[4].plot(skup2016[:,1],skup2016[:,0],color="blue",label="skupaj")
axes[4].set_xlabel("Leto 2016")
axes[4].set_xticks(meseci2016)
axes[4].set_xticklabels(np.array(mesci2016,dtype="str"),rotation=90)
axes[4].set_ylim(20, 2200)


fig.suptitle("Izguba skozi leta")
plt.show()


