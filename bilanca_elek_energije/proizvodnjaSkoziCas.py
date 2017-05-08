from csv import *
from operator import itemgetter
from pylab import *
from numpy import *

file2 = open("bilancaLeto.csv","rt")

slovar = {}

#Odjem energije skozi leta

leto = []
skupniOdjem = []

mesecno = DictReader(file2)

for row in mesecno:
    leto.append(int(row['leto']))
    skupniOdjem.append(int(row['Odjem-skupaj']))


odjemEnergijeTime = np.column_stack((np.array(skupniOdjem,dtype="int"), np.array(leto,dtype="int")))

fig, axes = plt.subplots(1,1, figsize=(5,5))
axes.plot(odjemEnergijeTime[:,1],odjemEnergijeTime[:,0],color="darkblue",label="Skupni Odjem")
axes.set_xticks(arange(1990,2016,1))
axes.set_xlabel("Leto")
axes.set_ylabel("Količina v GWh")
fig.suptitle("Skupni odjem skozi leta")
plt.show()