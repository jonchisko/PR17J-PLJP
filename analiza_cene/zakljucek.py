import numpy as np
import operator
from csv import DictReader
import matplotlib
import matplotlib.pyplot as plt
import pylab
from collections import defaultdict
import matplotlib.patches as mpatches
import operator

from scipy import stats
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import mean_squared_error



"""
1)proizvodnja stroma in cena
2)proizvodnja stroma in zaposleni, 
3)cena in zaposleni
4)korelacija med subvencijami,investicijami IN ceno
5)http://scikit-learn.org/stable/modules/cross_validation.html#cross-validation
naredi model, ki napoveduje končno ceno iz za ceno v primerjavi z expensi oziroma mogoče če kšn drug atribut
tko da morm zgradit en nov data frame za to, da bo to šlo skoz
"""


#1)proizvodbja stroma in cena

#preberem koncno ceno
reader = DictReader(open("./data/cene_koncna.csv", "rt", encoding="utf-8"))
leto = []
koncnaCena = []
for row in reader:
    koncnaCena.append(row["D - Slovenija"])
    leto.append(int(row["leto"]))

#preberem bilanco,letno
reader = DictReader(open("./data/bilancaLeto.csv", "rt", encoding="utf-8"))
bilanca = []
for row in reader:
    let = int(row["leto"])
    if let >= 2005:
        bilanca.append(row["Prevzem-skupaj"])

koncnaCena = np.array(koncnaCena, dtype="float")
bilanca = np.array(bilanca, dtype="float")
#bilanca je v gigavatnih urah
fig, axes = plt.subplots(1,2)
axes[0].plot(leto, koncnaCena, label="cena")
axes[0].plot(leto, bilanca, label="prejem energije")
axes[0].set_yscale("log")
axes[0].set_title("Cena in bilanca (log scale)")
axes[0].legend(loc=4)
axes[0].set_xticks(np.array(leto, dtype="int"))
axes[0].set_xticklabels(np.array(leto, dtype="int"))
axes[0].set_xlabel("Leto")
axes[0].set_ylabel("log vrednosti")
razmerje = koncnaCena/bilanca
axes[1].plot(leto, razmerje)
axes[1].fill_between(leto, razmerje, np.zeros((11)), alpha=0.1)
axes[1].set_title("Razmerje cena[EUR] in bilanca[GWh]")
axes[1].set_ylabel("Cena[EUR]/Bil[GWh]")
axes[1].set_xlabel("Leto")
axes[1].set_xticks(np.array(leto, dtype="int"))
axes[1].set_xticklabels(np.array(leto, dtype="int"))
plt.show()


#2)proizvodnja stroma in zaposleni


#3)cena in zaposleni

#4)korelacija med subvencijami,investicijami IN ceno
reader = DictReader(open("./data/investicije_leto.csv", "rt", encoding="utf-8"))
invest = []
for row in reader:
    if int(row["leto"]) >= 2005:
        invest.append(row["SKUPAJ"])
invest = np.array(invest, dtype="float")

reader = DictReader(open("./data/subvencija_obnovljivi_visokizkoristek.csv", "rt", encoding="utf-8"))
subvencija1 = []
for row in reader:
    if int(row["leto"]) >= 2005 and int(row["leto"]) < 2016:
        subvencija1.append(row["Skupaj OVE + SPTE"])
subvencija1 = np.array(subvencija1, dtype="float")

reader = DictReader(open("./data/subvecnije_rud_trbov_hrastnik_rjavi_premog.csv", "rt", encoding="utf-8"))
subvencija2 = []
for row in reader:
    if int(row["leto"]) >= 2005 and int(row["leto"]) < 2016:
        subvencija2.append(row["Znesek pomoci (EUR)"])
subvencija2 = np.array(subvencija2, dtype="float")

print("Korelacija investicij ter koncne cene", stats.pearsonr(koncnaCena, np.array(invest, dtype="float")))
print("Korelacija subvencij obnovljivih virov in SPTE ter koncne cene", stats.pearsonr(koncnaCena, np.array(subvencija1, dtype="float")))
print("Korelacija subvencij premogovnika ter koncne cene", stats.pearsonr(koncnaCena[:8], np.array(subvencija2, dtype="float")))

"""
Calculates a Pearson correlation coefficient and the p-value for testing non-correlation.

The Pearson correlation coefficient measures the linear relationship between two datasets. 
Strictly speaking, Pearson’s correlation requires that each dataset be normally distributed. 
Like other correlation coefficients, this one varies between -1 and +1 with 0 implying no correlation. 
Correlations of -1 or +1 imply an exact linear relationship. Positive correlations imply that as x increases, 
so does y. Negative correlations imply that as x increases, y decreases.

The p-value roughly indicates the probability of an uncorrelated system producing datasets that have a Pearson 
correlation at least as extreme as the one computed from these datasets. The p-values are not entirely reliable but are 
probably reasonable for datasets larger than 500 or so.
"""

#5)http://scikit-learn.org/stable/modules/cross_validation.html#cross-validation
#naredi model, ki napoveduje končno ceno iz za ceno v primerjavi z expensi oziroma mogoče če kšn drug atribut
#tko da morm zgradit en nov data frame za to, da bo to šlo skoz

from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import mean_squared_error
from sklearn import svm
from sklearn.metrics import mean_absolute_error

#preberi se potrebne, moc elektrarn in koncno porabo
reader = DictReader(open("./data/Moc_elektrarn.csv", "rt", encoding="utf-8"))
moc = []
for row in reader:
    if int(row["leto"]) >= 2005 and int(row["leto"]) < 2016:
        moc.append(row["Skupaj"])
moc = np.array(moc, dtype="float")

reader = DictReader(open("./data/KoncnaPorabaEE.csv", "rt", encoding="utf-8"))
poraba = []
for row in reader:
    if int(row["leto"]) >= 2005 and int(row["leto"]) < 2016:
        poraba.append(row["Koncna poraba - Gospodinjstva"])
poraba = np.array(poraba, dtype="float")

"""Ucenje, precno preverjanje


TimeSeriesSplit is a variation of k-fold which returns first k folds as train set and the (k+1) th fold as test set.
 Note that unlike standard cross-validation methods, successive training sets are supersets of those that come before them. 
 Also, it adds all surplus data to the first training partition, which is always used to train the model.
This class can be used to cross-validate time series data samples that are observed at fixed time intervals.

>>> X = np.array([[1, 2], [3, 4], [1, 2], [3, 4], [1, 2], [3, 4]])
>>> y = np.array([1, 2, 3, 4, 5, 6])
>>> tscv = TimeSeriesSplit(n_splits=3)
>>> print(tscv)  
TimeSeriesSplit(n_splits=3)
>>> for train, test in tscv.split(X):
...     print("%s %s" % (train, test))
[0 1 2] [3]
[0 1 2 3] [4]
[0 1 2 3 4] [5]

"""

#sestavi dataset
#razred je cena
#cena gre od 2005 do 2015
y = koncnaCena
dataset = np.column_stack((invest, subvencija1, moc, poraba))

tscv = TimeSeriesSplit(n_splits=9)
print("dataset")
print(dataset)
print("razred")
print(y)
error = 0
i = 0

#print("%s %s" %(train, test))
#dolocene vrstice in vse atribute
min_atribut = 0
min_error = 100000
min_a = 0
best_model = None

for a in np.arange(0.1, 30, 0.1):
    print(a)
    for atribut_start in range(4):
        for atribut_end in range(atribut_start, 4):
            for model in [LinearRegression(), Lasso(alpha=a), Ridge(alpha=a)]:
                i=0
                for train, test in tscv.split(dataset):
                    dataTrain = np.reshape(dataset[train, atribut_start:atribut_end+1], (len(train), atribut_end - atribut_start + 1) )
                    razredTrain = np.reshape(y[train], (len(train), 1) )

                    model.fit(dataTrain, razredTrain.ravel())

                    dataTest = np.reshape(dataset[test, atribut_start:atribut_end+1], (1, atribut_end - atribut_start + 1))
                    razredTest = np.reshape(y[test], (1, 1) )
                    hx = model.predict(dataTest)
                    #error += mean_squared_error(hx, razredTest.ravel())
                    error += mean_absolute_error(hx, razredTest.ravel())
                    #break
                    i += 1
                error = error/i
                if error < min_error:
                    min_error = error
                    min_atribut = [atribut_start, atribut_end]
                    min_a = a
                    best_model = model
print("Srednja absolutna napaka, najboljsi subset atributov za napoved, vrednost alpha, model : ", min_error, min_atribut, min_a, best_model)
print("Korelacija cene in moci elektrarn", stats.pearsonr(koncnaCena, moc))


#preberi zaposlene
readerList = []
file = "./data/Zaposleni_EES.csv"
reader = DictReader(open(file, "rt", encoding="utf-8"))
readerList.append(reader)
for i in range(2,10):
    file = "./data/Zaposleni_EES-"+str(i)+".csv"
    reader = DictReader(open(file, "rt", encoding="utf-8"))
    readerList.append(reader)

elektrarne = ["Holding Slovenske elektrarne",	"Dravske elektrarne Maribor",	"Soske elektrarne Nova Gorica",
              "Hidroelektrarne na Spodnji Savi",	"Termoelektrarna Trbovlje",	"Termoelektrarna sostanj",
              "HSE Invest",    "Gen Energija",    "Nuklerana elektrarna Krsko", "Savske elektrarne Ljubljana", "Termoelektrarna Brestanica",
              "Energetika Ljubljana - enota TE-TOL", "Gorenjske elektrarne",	"OVEN Elektro Maribor",	"Elektro Ljubljana OVE",
              "Elektro Slovenija",    "Elektro Celje",    "Elektro Primorska", "Elektro Gorenjska",	"Elektro Ljubljana",	"Elektro Maribor",
              "Elektro Energija",    "Energija Plus",   "Borzen", "SODO"]
data = [[] for x in range(len(elektrarne))]
offset = 0

zaposleni = [0 for x in range(14)]
for read in readerList:
    counter = 0
    for row in read:
        delavci = 0
        a = 3
        if offset == len(elektrarne)-1:
            a = 1
        for ele in range(a):
            e = elektrarne[offset+ele]
            value = row[e]
            if value == "?":
                value = 0
            data[offset+ele].append(value)
            delavci += int(value)
        zaposleni[counter]+=delavci
        counter += 1
    offset+=3

#print(zaposleni)
zaposleni = np.array(zaposleni, dtype="int")
leto = np.arange(2001,2015,1)
print("Zaposleni", zaposleni)

fig = plt.figure(figsize=(10, 10))
#fig, axes = plt.subplots()
#axes.plot(leto, zaposleni)
axes1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
axes2 = fig.add_axes([0.15, 0.5, 0.2, 0.3])

# Prikazi okolico nicle
axes1.plot(leto, zaposleni)
axes1.fill_between(leto, zaposleni, np.zeros(14), alpha=0.2)
axes1.set_xlabel('Leto')
axes1.set_ylabel('Število zaposlenih')
axes1.set_ylim([0, 7000])
axes1.set_title('Število zaposlenih (Velik y razpon)')
axes1.set_xticks(np.arange(2001,2015,1))
axes1.set_xticklabels(np.arange(2001, 2015, 1))

# Prikazi vecji interval
axes2.plot(leto, zaposleni, color="r")
axes2.fill_between(leto, zaposleni, (np.zeros(14)+6100), color="r", alpha=0.2)
axes2.set_xlabel('Leto')
axes2.set_ylabel('Število zaposlenih')
axes2.set_title('Pogled razlike ("od blizu")')
axes2.set_xticks(np.arange(2001,2015,3))
plt.show()

pomembne = ["Holding Slovenske Elektrarne",
"Nuklearna elektrarna Krsko",
"Elektro Celje",
"Elektro Maribor",
"Elektro Primorska",
"Termoelektrarna sostanj",
"Elektro Slovenija",
"Elektro Gorenjska"]

fig,axes = plt.subplots()
for i,x in enumerate(data):
    if elektrarne[i] in pomembne:
        axes.plot(leto, x, label=elektrarne[i])
axes.legend(loc=1)
axes.set_xlabel("Leto")
axes.set_ylabel("Število zaposlenih")
axes.set_title("Gibanje zaposlenih (najbolj zanimivi)")
plt.show()


#razlike
razlike = []
for i in range(len(zaposleni)-1):
    razlike.append(zaposleni[i] - zaposleni[i+1])

razlike = np.array(razlike, dtype="float")
fig, axes = plt.subplots()
poz = razlike.copy()
neg = razlike.copy()
poz[poz<0] = np.nan
neg[neg>=0] = np.nan
axes.bar(np.arange(2002,2015,1), poz, color="g", alpha=0.8)
axes.bar(np.arange(2002,2015,1), neg, color="r", alpha=0.8)
axes.set_title("Razlika gibanja zaposlenih")
axes.set_xlabel("Leto")
axes.set_ylabel("Razlika v zaposlenih")
axes.set_xticks(np.arange(2002,2015,1))
axes.set_xticklabels(np.arange(2002,2015,1))
plt.show()

#2)proizvodnja stroma in zaposleni
fig, axes = plt.subplots(1,2)
bilanca = []
reader = DictReader(open("./data/bilancaLeto.csv", "rt", encoding="utf-8"))
for row in reader:
    let = int(row["leto"])
    if let >= 2001 and let <= 2014:
        bilanca.append(row["Prevzem-skupaj"])

bilanca = np.array(bilanca, dtype="float")
zaposleni = np.array(zaposleni, dtype="float")

axes[0].plot(np.arange(2001,2015,1), bilanca, label="bilanca")
axes[0].plot(np.arange(2001,2015,1), zaposleni, label="zaposleni")
axes[0].set_xticks(np.arange(2001,2015,2))
axes[0].set_xticklabels(np.arange(2001,2015,2))
axes[0].set_title("Gibanje bilance, zaposlenih")
axes[0].set_xlabel("Leto")
axes[0].set_ylabel("log scale")
axes[0].set_yscale("log")
axes[0].legend(loc=1)

axes[1].plot(np.arange(2001,2015,1), bilanca/zaposleni)
axes[1].set_title("Razmerje bilanca, zaposleni")
axes[1].set_xlabel("Leto")
axes[1].set_ylabel("bilanca/zaposleni [GWh/zaposlen]")
axes[1].fill_between(np.arange(2001,2015,1), bilanca/zaposleni, np.zeros(14), color="b", alpha=0.2)
axes[1].set_xticks(np.arange(2001,2015,2))
axes[1].set_xticklabels(np.arange(2001,2015,2))
plt.show()


#3)cena in zaposleni
fig, axes = plt.subplots(1,2)
#leto 2005-2014
cena = []
reader = DictReader(open("./data/cene_koncna.csv", "rt", encoding="utf-8"))
for row in reader:
    let = int(row["leto"])
    if let <= 2014:
        cena.append(row["D - Slovenija"])

cena = np.array(cena, dtype="float")
zaposleni1 = zaposleni[4:]

axes[0].plot(np.arange(2005,2015,1), cena, label="cena")
axes[0].plot(np.arange(2005,2015,1), zaposleni1, label="zaposleni")
axes[0].set_xticks(np.arange(2005,2015,2))
axes[0].set_xticklabels(np.arange(2005,2015,2))
axes[0].set_title("Gibanje cena, zaposlenih")
axes[0].set_xlabel("Leto")
axes[0].set_ylabel("log scale")
axes[0].set_yscale("log")
axes[0].legend(loc=1)

axes[1].plot(np.arange(2005,2015,1), cena/zaposleni1)
axes[1].set_title("Razmerje cena, zaposleni")
axes[1].set_xlabel("Leto")
axes[1].set_ylabel("cena/zaposleni [EUR/zaposlen]")
axes[1].fill_between(np.arange(2005,2015,1), cena/zaposleni1, np.zeros(10), color="b", alpha=0.2)
axes[1].set_xticks(np.arange(2005,2015,2))
axes[1].set_xticklabels(np.arange(2005,2015,2))
plt.show()