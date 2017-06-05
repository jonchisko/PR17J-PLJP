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
axes[1].set_ylabel("Cena/Bilanca")
axes[1].set_xlabel("Leto")
axes[1].set_xticks(np.array(leto, dtype="int"))
axes[1].set_xticklabels(np.array(leto, dtype="int"))
#plt.show()


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


#print("%s %s" %(train, test))
#dolocene vrstice in vse atribute
min_atribut = 0
min_error_mean = 100000
min_a = 0
best_model = None
error_sq_best = 10000000


for a in np.arange(1, 10, 1):
    print(a)
    for atribut_start in range(4):
        for atribut_end in range(atribut_start, 4):
            error_mean = 0
            error_sq = 0
            i = 0
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
                    error_mean += mean_absolute_error(hx, razredTest.ravel())
                    error_sq += mean_squared_error(hx, razredTest.ravel())
                    #break
                    i += 1
                error_mean = error_mean/i
                error_sq = error_sq/i
                if error_mean < min_error_mean:
                    min_error_mean = error_mean
                    min_atribut = [atribut_start, atribut_end]
                    min_a = a
                    best_model = model
                    error_sq_best = error_sq

from math import sqrt

print("Srednja absolutna napaka, kvad_napaka, kvad_napaka koren, najboljsi subset atributov za napoved, vrednost alpha, model : ",
      min_error_mean, error_sq_best, sqrt(error_sq_best), min_atribut, min_a, best_model)
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
#plt.show()

pomembne = ["Holding Slovenske Elektrarne",
"Nuklearna elektrarna Krsko",
"Elektro Celje",
"Elektro Maribor",
"Elektro Primorska",
"Elektro Slovenija",
"Elektro Gorenjska","Elektro Ljubljana"
]

fig,axes = plt.subplots(1,3)
y = np.zeros(len(data[0]), dtype="float")
for i,x in enumerate(data):

    if elektrarne[i] in pomembne:
        style = "-."
        if elektrarne[i] == "Elektro Gorenjska":
            style="-"
        axes[0].plot(leto, x, ls=style, label=elektrarne[i])
        y+=np.array(x, dtype="float")
axes[1].plot(leto,y,"r--", lw=3, label="sum")
axes[0].legend(loc=1)
axes[0].set_xlabel("Leto")
axes[0].set_ylabel("Število zaposlenih")
axes[0].set_title("Gibanje zaposlenih (najbolj zanimivi)")
axes[2].set_xlabel("Leto")
axes[2].set_ylabel("Število zaposlenih")
axes[2].set_title("Seštevek zaposlenih Elektro")
axes[1].set_title("Seštevek zaposlenih Elektro - večji razpon")
axes[1].set_xlabel("Leto")
axes[1].set_ylabel("Število zaposlenih Elektro")
axes[2].plot(leto,y,"r--", lw=3, label="sum")
axes[1].set_ylim([0,4050])
for x in range(3):
    axes[x].set_xticks(np.arange(min(leto), max(leto) + 1, 3))
    axes[x].set_xticklabels(np.arange(min(leto), max(leto)+1, 3))
#plt.show()


#razlike
razlike = []
for i in range(len(zaposleni)-1):
    print(zaposleni[i])
    razlike.append(zaposleni[i+1] - zaposleni[i])

razlike = np.array(razlike, dtype="float")
fig, axes = plt.subplots()
poz = razlike.copy()
neg = razlike.copy()
poz[poz<0] = np.nan
neg[neg>=0] = np.nan
print(poz)
print(neg)
axes.bar(np.arange(2002,2015,1), poz, color="g", alpha=0.8)
axes.bar(np.arange(2002,2015,1), neg, color="r", alpha=0.8)
axes.set_title("Razlika gibanja zaposlenih")
axes.set_xlabel("Leto")
axes.set_ylabel("Razlika v zaposlenih")
axes.set_xticks(np.arange(2002,2015,1))
axes.set_xticklabels(np.arange(2002,2015,1))


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
axes[1].set_ylabel("bilanca/zaposleni")
axes[1].fill_between(np.arange(2001,2015,1), bilanca/zaposleni, np.zeros(14), color="b", alpha=0.2)
axes[1].set_xticks(np.arange(2001,2015,2))
axes[1].set_xticklabels(np.arange(2001,2015,2))
#plt.show()


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
axes[0].set_title("Gibanje cena, zaposleni")
axes[0].set_xlabel("Leto")
axes[0].set_ylabel("log scale")
axes[0].set_yscale("log")
axes[0].legend(loc=1)

axes[1].plot(np.arange(2005,2015,1), cena/zaposleni1)
axes[1].set_title("Razmerje cena, zaposleni")
axes[1].set_xlabel("Leto")
axes[1].set_ylabel("cena/zaposleni")
axes[1].fill_between(np.arange(2005,2015,1), cena/zaposleni1, np.zeros(10), color="b", alpha=0.2)
axes[1].set_xticks(np.arange(2005,2015,2))
axes[1].set_xticklabels(np.arange(2005,2015,2))
#plt.show()


"""
Korelacija investicij ter koncne cene (-0.1307414096552979, 0.70159954201736052)
Korelacija subvencij obnovljivih virov in SPTE ter koncne cene (0.9020608764310194, 0.00014610864766170738)
Korelacija subvencij premogovnika ter koncne cene (-0.96800070000529459, 7.9961297640388697e-05)



Srednja absolutna napaka, kvad_napaka, kvad_napaka koren, najboljsi subset atributov za napoved, vrednost alpha, model :  7.27980276492 133.011179176 11.533047263222416 [2, 3] 39.9 Lasso(alpha=39.900000000000006, copy_X=True, fit_intercept=True,
   max_iter=1000, normalize=False, positive=False, precompute=False,
   random_state=None, selection='cyclic', tol=0.0001, warm_start=False)
Korelacija cene in moci elektrarn (0.9429085307122419, 1.3680433898470748e-05)
Zaposleni [6608 6621 6485 6421 6364 6348 6386 6475 6545 6386 6422 6302 6255 6200]

"""

##########
##########
# PREMOG #
##########
##########

leto = []
lignit = []
rjavi = []
crni = []

reader = DictReader(open("./data/IzkopEnergijaIzkopaniPremog1.csv", "rt", encoding="utf-8"))
for row in reader:
    leto.append(row["leto"])
    lig = row["Lignit skupaj"]
    rj = row["Rjavi premog skupaj"]
    cr = row["crni premog skupaj"]
    if lig == "?":
        lig = 0
    if rj == "?":
        rj = 0
    if cr == "?":
        cr = 0
    lignit.append(lig)
    rjavi.append(rj)
    crni.append(cr)

leto = np.array(leto, dtype="int")
lignit = np.array(lignit, dtype="float")
rjavi = np.array(rjavi, dtype="float")
crni = np.array(crni, dtype="float")
#1000ton
fig, axes = plt.subplots(1,2)
axes[1].plot(leto,crni, color="black", label="črni premog")
axes[1].fill_between(leto, crni, np.zeros(len(crni)), color="black", alpha=0.2)
axes[1].plot(leto,rjavi+crni, color="orange", label="rjavi premog")
axes[1].fill_between(leto, rjavi+crni, crni, color="orange", alpha=0.2)
axes[1].plot(leto,lignit+rjavi+crni, color="red", label="lignit")
axes[1].fill_between(leto, lignit+rjavi+crni, rjavi+crni, color="red", alpha=0.2)
axes[1].legend(loc=1)
axes[1].set_title("Gibanje izkopa premoga od 1962")
axes[1].set_xlabel("Leto")
axes[1].set_ylabel("izkop [1000t]")

axes[0].plot(leto,crni, color="black", label="črni premog")
axes[0].plot(leto,rjavi, color="orange", label="rjavi premog")
axes[0].plot(leto,lignit, color="red", label="lignit")
axes[0].legend(loc=1)
axes[0].set_title("Gibanje izkopa premoga od 1962")
axes[0].set_xlabel("Leto")
axes[0].set_ylabel("izkop [1000t]")
#plt.show()

skupine = ["DA (< 1.000 kWh)", "DE ( >= 15.000 kWh)", "D - Slovenija"]

vsi_ene = [[] for x in range(3)]
leto = np.arange(2005,2016,1)
reader = DictReader(open("./data/cene_energija.csv", "rt", encoding="utf-8"))
for row in reader:
    for i, skp in enumerate(skupine):
        vsi_ene[i].append(row[skp])

vsi_daj = [[] for x in range(3)]
reader = DictReader(open("./data/cene_dajatve.csv", "rt", encoding="utf-8"))
for row in reader:
    for i, skp in enumerate(skupine):
            vsi_daj[i].append(row[skp])


for i,x in enumerate(vsi_ene):
    vsi_ene[i] = np.array(x, dtype="float")
for i,x in enumerate(vsi_daj):
    vsi_daj[i] = np.array(x, dtype="float")

for i,x in enumerate(vsi_ene):
    print("ENERGIJA, porabniska skupina: ", skupine[i], " korelacija: ",stats.pearsonr(x, subvencija1))
for i,x in enumerate(vsi_daj):
    print("DAJATVE, porabniska skupina: ", skupine[i], " korelacija: ",stats.pearsonr(x, subvencija1))


plt.show()