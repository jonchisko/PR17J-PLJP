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
temp2012 = np.column_stack((np.array([1.6,-0.8,10.1,11.4,16.1,21.3,22.7,23.3,17.0,11.7,8.8,0.8],dtype="float"),np.array(mesci,dtype="int")))
skup2012 = np.column_stack((np.array(skup2012,dtype="float"), np.array(mesci,dtype="int")))

izgub2013 = np.column_stack((np.array(izgub2013,dtype="float"), np.array(mesci,dtype="int")))
temp2013 = np.column_stack((np.array([2.0,0.9,3.9,12.4,14.8,19.8,23.5,22.5,16.2,13.2,7.3,2.7],dtype="float"),np.array(mesci,dtype="int")))
skup2013 = np.column_stack((np.array(skup2013,dtype="float"), np.array(mesci,dtype="int")))

izgub2014 = np.column_stack((np.array(izgub2014,dtype="float"), np.array(mesci,dtype="int")))
temp2014 = np.column_stack((np.array([5.4,4.4,10.0,13.1,15.7,20.2,20.8,19.6,16.2,13.6,8.8,3.9],dtype="float"),np.array(mesci,dtype="int")))
skup2014 = np.column_stack((np.array(skup2014,dtype="float"), np.array(mesci,dtype="int")))

izgub2015 = np.column_stack((np.array(izgub2015,dtype="float"), np.array(mesci,dtype="int")))
temp2015 = np.column_stack((np.array([2.8,2.4,7.6,11.8,17.0,20.6,24.3,22.3,16.5,11.0,6.9,2.6],dtype="float"),np.array(mesci,dtype="int")))
skup2015 = np.column_stack((np.array(skup2015,dtype="float"), np.array(mesci,dtype="int")))

izgub2016 = np.column_stack((np.array(izgub2016,dtype="float"), np.array(meseci2016,dtype="int")))
temp2016 = np.column_stack((np.array([1.1,5.5,7.5,12.5,15.3,19.9,23.2,20.6,18.3],dtype="float"),np.array(meseci2016,dtype="int")))
skup2016 = np.column_stack((np.array(skup2016,dtype="float"), np.array(meseci2016,dtype="int")))


fig, axes = plt.subplots(1,5, figsize=(5,5))
axes[0].plot(izgub2012[:,1],izgub2012[:,0],color="green",label="izguba")
axes[0].plot(temp2012[:,1],temp2012[:,0],color="blue",label="skupaj")
axes[0].set_xlabel("Leto 2012")
axes[0].set_ylabel("Temperatura in izguba")
axes[0].set_xticks(mesci)
axes[0].set_xticklabels(np.array(meseci,dtype="str"),rotation=90)
axes[0].set_ylim(-5, 180)

axes[1].plot(izgub2013[:,1],izgub2013[:,0],color="green",label="izguba")
axes[1].plot(temp2013[:,1],temp2013[:,0],color="blue",label="skupaj")
axes[1].set_xlabel("Leto 2013")
axes[1].set_xticks(mesci)
axes[1].set_xticklabels(np.array(meseci,dtype="str"),rotation=90)
axes[1].set_ylim(-5, 180)

axes[2].plot(izgub2014[:,1],izgub2014[:,0],color="green",label="izguba")
axes[2].plot(temp2014[:,1],temp2014[:,0],color="blue",label="skupaj")
axes[2].set_xlabel("Leto 2014")
axes[2].set_xticks(mesci)
axes[2].set_xticklabels(np.array(meseci,dtype="str"),rotation=90)
axes[2].set_ylim(-5, 180)

axes[3].plot(izgub2015[:,1],izgub2015[:,0],color="green",label="izguba")
axes[3].plot(temp2015[:,1],temp2015[:,0],color="blue",label="skupaj")
axes[3].set_xlabel("Leto 2015")
axes[3].set_xticks(mesci)
axes[3].set_xticklabels(np.array(meseci,dtype="str"),rotation=90)
axes[3].set_ylim(-5, 180)

axes[4].plot(izgub2016[:,1],izgub2016[:,0],color="green",label="izguba")
axes[4].plot(temp2016[:,1],temp2016[:,0],color="blue",label="skupaj")
axes[4].set_xlabel("Leto 2016")
axes[4].set_xticks(meseci2016)
axes[4].set_xticklabels(np.array(mesci2016,dtype="str"),rotation=90)
axes[4].set_ylim(-5, 180)


fig.suptitle("Odvisnost izgube z temperaturo")
plt.show()


