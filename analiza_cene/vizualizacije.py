import numpy as np
import operator
from csv import DictReader
import matplotlib
import matplotlib.pyplot as plt
import pylab
from collections import defaultdict
import matplotlib.patches as mpatches
import operator

reader = DictReader(open("./data/cene_koncna.csv", "rt", encoding="utf-8"))
leto = []
vsiD = [[] for x in range(6)]
for row in reader:
    vsiD[0].append(row["D - Slovenija"])
    leto.append(row["leto"])
reader = DictReader(open("./data/cene_energija.csv", "rt", encoding="utf-8"))
for row in reader:
    vsiD[1].append(row["D - Slovenija"])
reader = DictReader(open("./data/cene_omreznina.csv", "rt", encoding="utf-8"))
for row in reader:
    vsiD[2].append(row["D - Slovenija"])
reader = DictReader(open("./data/cene_trosarina.csv", "rt", encoding="utf-8"))
for row in reader:
    value = row["D - Slovenija"]
    if value == "..":
        value = None
    vsiD[3].append(value)
reader = DictReader(open("./data/cene_ddv.csv", "rt", encoding="utf-8"))
for row in reader:
    vsiD[4].append(row["D - Slovenija"])
reader = DictReader(open("./data/cene_dajatve.csv", "rt", encoding="utf-8"))
for row in reader:
    vsiD[5].append(row["D - Slovenija"])

data1 = np.column_stack((np.array(leto, dtype="float"), np.array(vsiD[0], dtype="float"), np.array(vsiD[1], dtype="float"), np.array(vsiD[2], dtype="float"),
                         np.array(vsiD[3], dtype="float"), np.array(vsiD[4], dtype="float"), np.array(vsiD[5], dtype="float")))

#vsi deli cene prikazani + končna cena
plt.style.use('ggplot')
fig = plt.figure()
axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
color = ["r", "b", "g", "y", "purple", "orange"]
lb = ["končna", "energija", "omrežnina", "trošarina", "ddv", "dajatve"]
for x in range(6):
    axes.plot(data1[:,0], data1[:,x+1], color=color[x], label=lb[x])
axes.set_xlim([2005, 2015])
ticks = np.arange(2005, 2016, 1)
axes.set_xticks(ticks)
axes.set_xticklabels(np.array(data1[:,0], dtype="int"))
axes.set_xlabel('Leto')
axes.set_ylabel('EUR/MWh')
axes.set_title('Gibanje cene')
axes.legend(loc=2)
plt.show()

#gibanje koncne cene glede na povprecno koncno ceno
avg = np.mean(data1[:,1])
std = np.std(data1[:,1])
fig, axes = plt.subplots(figsize=(10,10))
axes.plot([data1[0,0]-1, data1[-1,0]+1], [avg, avg], color="b", label="povprečje")
axes.fill_between([data1[0,0]-1, data1[-1,0]+1], [avg+std, avg+std], [avg-std, avg-std], color="b", alpha=0.1, label="odklon")
pozitivno = data1[:, 1].copy()
negativno = data1[:, 1].copy()
pozitivno[pozitivno<avg] = np.nan
negativno[negativno>=avg] = np.nan
axes.bar(data1[:, 0], pozitivno-avg, bottom=avg, color="g", label="dvig", alpha=0.8)
axes.bar(data1[:, 0], negativno-avg, bottom=avg, color="r", label="padec", alpha=0.8)
axes.set_ylim(100, 175)
axes.set_title("Odstopanje od povprečne končne cene")
ticks = np.array(data1[:,0], dtype="int")
axes.set_xticks(ticks)
axes.set_xticklabels(ticks)
axes.set_ylabel("EUR")
axes.set_xlabel("Leto")
axes.legend(loc=1)
plt.show()

#deli cene prikazani s površino, absolutna vrednost
fig = plt.figure()
axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])
color = ["r", "b", "g", "purple", "orange"]
lb = ["energija", "omrežnina", "trošarina", "ddv", "dajatve"]
new_x_0 = np.zeros((11))
for x in range(0,5):
    data1[np.isnan(data1[:,x+2]), x+2] = 0
    to_plot = data1[:,x+2]+new_x_0
    if(lb[x]=="trošarina"):
        axes.plot(data1[2:, 0], to_plot[2:], color=color[x], label=lb[x])
        axes.fill_between(data1[2:, 0], to_plot[2:], new_x_0[2:], color=color[x], alpha=0.6)
    else:
        axes.plot(data1[:,0], to_plot, color=color[x], label=lb[x])
        axes.fill_between(data1[:,0], to_plot, new_x_0, color=color[x], alpha=0.6)
    new_x_0 = to_plot
axes.set_xlim([2005, 2015])
ticks = np.arange(2005, 2016, 1)
axes.set_xticks(ticks)
axes.set_xticklabels(np.array(data1[:,0], dtype="int"))
axes.set_xlabel('Leto')
axes.set_ylabel('EUR/MWh')
axes.set_title('Gibanje cene, sestava')
axes.legend(loc=2)
plt.show()

#deleži delov cene
fig, axes = plt.subplots(figsize=(12,4))
color = ["r", "b", "g", "purple", "orange"]
lb = ["energija", "omrežnina", "trošarina", "ddv", "dajatve"]
new_x_0 = np.zeros((11))
for x in range(5):
    data1[np.isnan(data1[:, x + 2]), x + 2] = 0
    axes.bar(data1[:,0], data1[:,x+2]/data1[:,1], bottom=new_x_0, label=lb[x], color=color[x], alpha=0.7)
    for year, value, new_x in zip(data1[:,0], (data1[:,x+2]/data1[:,1]), new_x_0):
        axes.text(year, value/3+new_x, str(value)[:4], fontweight="bold", fontsize=7)
    new_x_0 += data1[:,x+2]/data1[:,1]


axes.set_xlim([2005, 2015])
ticks = np.arange(2005, 2016, 1)
axes.set_xticks(ticks)
axes.set_xticklabels(np.array(data1[:,0], dtype="int"))
axes.set_xlabel('Leto')
axes.set_ylabel('delež')
axes.set_title('Gibanje cene, delež')
axes.legend(loc=2)
plt.show()



#1)nariši še bar plot, ki bo za vsako leto imel za vse porabniske skupine tak stolpic kot je prejsnji graf
#lahko vidiš primerjavo cen glede na porabniško skupino!
skupina = defaultdict(lambda :defaultdict(list))
sk_imena = []
#preberi iz tabel
"""reader = DictReader(open("./data/cene_koncna.csv", "rt", encoding="utf-8"))
for row in reader:
    for keys in row:
        if keys != "leto":
            sk_imena.append(keys)
            skupina[keys]["koncna"].append(row[keys])"""
reader = DictReader(open("./data/cene_ddv.csv", "rt", encoding="utf-8"))
i = 0
for row in reader:
    for keys in row:
        if keys != "leto":
            if i == 0:
                sk_imena.append(keys)
            skupina[keys]["ddv"].append(row[keys])
    i+=1
reader = DictReader(open("./data/cene_energija.csv", "rt", encoding="utf-8"))
for row in reader:
    for keys in row:
        if keys != "leto":
            skupina[keys]["energija"].append(row[keys])
reader = DictReader(open("./data/cene_omreznina.csv", "rt", encoding="utf-8"))
for row in reader:
    for keys in row:
        if keys != "leto":
            skupina[keys]["omreznina"].append(row[keys])

reader = DictReader(open("./data/cene_dajatve.csv", "rt", encoding="utf-8"))
for row in reader:
    for keys in row:
        if keys != "leto":
            skupina[keys]["dajatve"].append(row[keys])

reader = DictReader(open("./data/cene_trosarina.csv", "rt", encoding="utf-8"))
for row in reader:
    for keys in row:
        if keys != "leto":
            ar = row[keys]
            if ar == "..":
                ar = np.nan
            skupina[keys]["trosarina"].append(ar)



#convertaj vse skupaj v numpy ar
for sk in sk_imena:
    for k in skupina[sk]:
        skupina[sk][k] = np.array(skupina[sk][k], dtype="float")

fig, axes = plt.subplots()
leta = np.arange(2005, 2016,1)
axes.set_xticks(leta)
axes.set_xticklabels(leta)
col = ["red","g","b","orange", "magenta"]
lb = ["ddv", "energija", "omrežnina", "dajatve", "trošarina"]
width = 0.15
offset = 0
for sk in sk_imena:
    i = 0
    nov_bot = np.zeros((len(skupina[sk]["trosarina"])))
    for i, k in enumerate(skupina[sk]):
        vrednost = skupina[sk][k]
        vrednost[np.isnan(vrednost)] = 0
        #skupina
        if i == len(skupina[sk])-1:
            axes.text(leta[0] + offset - 0.04, 200, sk, fontsize=5, rotation=90)
        axes.bar(leta+offset, vrednost, width=width, bottom=nov_bot, color=col[i], alpha=0.5, edgecolor="black", label=k)
        for le, vr, nb in zip(leta, vrednost, nov_bot):
            axes.text(le+offset-0.04, vr/2+nb, str(vr)[:2], fontweight="bold", fontsize=5, rotation=90)
        nov_bot += vrednost
        i+=1
    offset += 0.15
patches = [mpatches.Patch(color=x, label=lb[i]) for i,x in enumerate(col)]
plt.legend(handles=patches, loc=2)
axes.set_ylabel("EUR/MWh")
axes.set_xlabel("Leto")
axes.set_title("Gibanje vseh po vseh skupinah")
plt.show()

#IDENTIČEN GRAF LE DA DELEŽI
fig, axes = plt.subplots()
leta = np.arange(2005, 2016,1)
axes.set_xticks(leta)
axes.set_xticklabels(leta)
col = ["red","g","b","purple", "magenta"]
lb = ["ddv", "energija", "omrežnina", "dajatve", "trošarina"]
width = 0.15
offset = 0
for sk in sk_imena:
    i = 0
    nov_bot = np.zeros((len(skupina[sk]["trosarina"])))
    končna = np.zeros((len(skupina[sk]["trosarina"])))
    for k in skupina[sk]:
        v = skupina[sk][k]
        v[np.isnan(v)] = 0
        končna+=skupina[sk][k]
    for i, k in enumerate(skupina[sk]):
        vrednost = skupina[sk][k]/končna
        vrednost[np.isnan(vrednost)] = 0
        #skupina
        if i == len(skupina[sk])-1:
            axes.text(leta[0] + offset - 0.04, 0.5, sk, fontsize=5, rotation=90)

        axes.bar(leta+offset, vrednost, width=width, bottom=nov_bot, color=col[i], alpha=0.5, edgecolor="black", label=k)
        for le, vr, nb in zip(leta, vrednost, nov_bot):
            axes.text(le+offset-0.04, vr/3+nb, str(vr)[:4], fontweight="bold", fontsize=5, rotation=90)
        nov_bot += vrednost
        i+=1
    offset += 0.15
patches = [mpatches.Patch(color=x, label=lb[i]) for i,x in enumerate(col)]
plt.legend(handles=patches, loc=2)
axes.set_ylabel("EUR/MWh")
axes.set_xlabel("Leto")
axes.set_title("Gibanje vseh po vseh skupinah")
plt.show()
#4)prikaz koliko energije dobimo na subvencijo :) eur/MWh   (une subvecnionirane so v kWh, rjavi premog pa v GWh)
# /subvencionirane pa trbovlje
"""
KAJ JE SPTE?
Je samostojna proizvodna enota za pridobivanje toplotne in električne energije, ki jo imenujemo tudi kogeneracija. Omogoča proizvodnjo električne energije, katero lahko v celoti oddamo v elektrodistribucijsko omrežje ali jo porabimo za lastno rabo. Proizvedeno toplotno energijo uporabimo za ogrevanje ali pripravo sanitarne vode in za razne tehnološke procese v industriji.

KDAJ SE ODLOČITI ZA SPTE?
Največja prednost kogeneracije je v zanesljivosti oskrbe z energijo in neodvisnosti njene proizvodnje od javnega omrežja. Takšni sistemi so odlična naložba za objekte, kjer je treba ogrevati prostore večjih površin.

Kogeneracije različnih nazivnih električnih moči od 30 do 500 kWe se uporabljajo v različnih panogah, kot so:

industrijski obrati,
zdravstvene ustanove,
šole, vrtci, domovi za ostarele,
trgovski in športni centri,
stanovanjska poslopja (hiše, bloki).
Prednosti SPTE enote so:

nizki stroški električne in toplotne energije,
nižji obratovalni stroški,
večji energijski izkoristki,
večja zanesljivost oskrbe z energijo,
koriščenje energije neodvisno od javnega omrežja,
proizvodnja okolju prijazne energije,
nižanje emisij toplogrednih plinov (CO2) ter emisij ostalih plinastih onesnaževal (CO, SO2 in NOX),
uporaba ekološkega vira goriv (zemeljski plin, biomasa).

OVE - obnovljivi viri
"""
reader = DictReader(open("./data/subvecnije_rud_trbov_hrastnik_rjavi_premog.csv", "rt", encoding="utf-8"))
eurMWh_rjavi = []
leto_rjavi = []
for row in reader:
    eurMWh_rjavi.append(row["Visina pomoci (EUR/MWh)"])
    leto_rjavi.append(row["leto"])

reader = DictReader(open("./data/subvecnija_obnovljivi_visokizkoristek_proizvodnja.csv", "rt", encoding="utf-8"))
leto_sub = []
slovarkWh = defaultdict(list)
for row in reader:
    leto_sub.append(row["leto"])
    for keys in row.keys():
        if keys != "leto":
            slovarkWh[keys].append(row[keys])

reader = DictReader(open("./data/subvencija_obnovljivi_visokizkoristek.csv", "rt", encoding="utf-8"))
slovarKes = defaultdict(list)
for row in reader:
    for keys in row.keys():
        if keys != "leto":
            vstavi = row[keys]
            if(vstavi == ".."):
                vstavi = np.nan
            slovarKes[keys].append(vstavi)

#slovarKes
#slovarkWh
#leto_sub
#eurMWh_rjavi
#leto_rjavi

#spremeni prvo v MWh
for x in slovarkWh:
    #manjkajočo dej v None
    ar = np.array(slovarkWh[x])
    ar[ar==".."] = np.nan
    slovarkWh[x] = np.array(ar, dtype="float")/1000

#izracunaj EUR/MWh
for x in slovarkWh:
    #warning je ker je nekje deljenje z nic
    slovarkWh[x] = np.array(slovarKes[x], dtype="float")/slovarkWh[x]

#izris
fig, axes = plt.subplots()
rjaviMWh = np.array(eurMWh_rjavi, dtype="float")
leta = np.arange(2001,2017, 1)
axes.plot(leta[:12], rjaviMWh, lw=3, ls="--", label="premogovnik Trbovlje")
axes.set_xlim(min(leta), max(leta))
for x in slovarkWh:
    if x == "OVE Skupaj":
        axes.plot(leta[3:, ], slovarkWh[x], color="blue", alpha=1, ls="--", lw=3, label="OVE skupaj")
    elif x == "SPTE Skupaj":
        axes.plot(leta[3:, ], slovarkWh[x], color="green", alpha=1, ls="--", lw=3, label="SPTE skupaj")
    else:
        col = "green"
        if "OVE" in x:
            col = "blue"
        axes.plot(leta[3:, ], slovarkWh[x], color=col, alpha=0.2, lw=1)
axes.set_title("Koliko subvencioniramo na MWh")
axes.set_xlabel("Leto")
axes.set_ylabel("EUR/MWh")
axes.set_xticks(np.arange(2001,2017,1))
axes.set_xticklabels(np.arange(2001,2017,1))
#ugotovil da so sončne zelo visoko, plotam še enkrat
axes.plot(leta[3:, ], slovarkWh["OVE - Soncne elektrarne"], color="red", alpha=0.7, lw=1, ls=":", label="Sončne elektrarne (OVE)")
axes.legend(loc=2)
plt.show()

avgkwh = []
for x in slovarkWh:
    #prvo nadomesti nan z 0 ...
    value = slovarkWh[x]
    value[np.isnan(value)] = 0
    avgkwh.append((x, np.sum(value)/len(value)))
avgkwh.append(("rudnik trbovlje", np.sum(rjaviMWh)/len(rjaviMWh)))
print(avgkwh)
avgkwh.sort(key=lambda x: x[1])

fig, axes = plt.subplots()
y_pos = np.arange(len(avgkwh[-10:]))
ele = [x for x,y in avgkwh[-10:]]
value = [y for x,y in avgkwh[-10:]]
axes.barh(y_pos, value, align="center", color="b")
axes.set_yticks(y_pos)
axes.set_yticklabels(ele,rotation=45, size=5)
axes.set_title("Povprečna subvencija EUR/MWh")
plt.show()

#korelacija s subvencijami?
#Skupaj OVE + SPTE, subvecnije obnovljivi
#Znesek pomoci (EUR), subvecnije rjavi premog

reader = DictReader(open("./data/subvencija_obnovljivi_visokizkoristek.csv", "rt", encoding="utf-8"))
sub_obn = []
leto_s = []
for row in reader:
    sub_obn.append(row["Skupaj OVE + SPTE"])
    leto_s.append(row["leto"])
reader = DictReader(open("./data/subvecnije_rud_trbov_hrastnik_rjavi_premog.csv", "rt", encoding="utf-8"))
sub_rjv = []
leto_m = []
for row in reader:
    sub_rjv.append(row["Znesek pomoci (EUR)"])
    leto_m.append(row["leto"])

reader = DictReader(open("./data/investicije_leto.csv", "rt", encoding="utf-8"))
invest = []
leto_in = []
for row in reader:
    invest.append(row["SKUPAJ"])
    leto_in.append(row["leto"])

#subvencije data gre od leta 2004 do 2016, vkljucno
#premog data gre od 2001 do 2012 vkljucno
#tedva data imata leta na drugem mestu, ker sem tako dodal skupaj kot vidite - zapomni si!
from scipy import stats
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import mean_squared_error

sub_data = np.column_stack((np.array(sub_obn, dtype="float"), np.array(leto_s, dtype="float")))
rjv_data = np.column_stack((np.array(sub_rjv, dtype="float"), np.array(leto_m, dtype="float")))
invest_data = np.column_stack((np.array(invest, dtype="float"), np.array(leto_in, dtype="float")))

skupaj = np.zeros((16, 2))
subvencije_skupaj = np.zeros((16, 2))
subvencije_skupaj[0:12, 1] += rjv_data[:, 0]
subvencije_skupaj[3:, 1] += sub_data[:, 0]
subvencije_skupaj[:, 0] = np.arange(2001, 2017,1)
skupaj[:, :] += subvencije_skupaj[:,:]
skupaj[3:-1, 1] += invest_data[:, 0]

#prikazi subvencije in investicije
fig, axes = plt.subplots(1, 3, figsize=(5,5))

for i in range(3):
    axes[i].plot(subvencije_skupaj[:,0], subvencije_skupaj[:,1], color="r", label="skupaj subvencije")
    axes[i].plot(sub_data[:,1], sub_data[:,0], color="g", label="obnovljivi viri")
    axes[i].plot(rjv_data[:,1], rjv_data[:,0], color="b", label="rjavi premog")
    #axes[i].set_xlim(2001, 2017)
    ticks = np.arange(2001, 2017, 1)
    axes[i].set_xticks(ticks)
    axes[i].set_xticklabels(np.array(subvencije_skupaj[:, 0], dtype="int"), rotation=90)

    axes[i].set_xlabel("Leto")
    axes[i].set_ylabel("EUR")

    if i > 0:
        if i == 2:
            axes[i].set_title("Subvencije, investicije(log)")
        else:
            axes[i].set_title("Subvencije, investicije")
        axes[i].plot(invest_data[:,1], invest_data[:,0], color="orange", label="investicije")
        axes[i].plot(skupaj[:, 0], skupaj[:, 1], color="purple", label="skupaj")
        axes[i].legend(loc=1)
    else:
        axes[i].set_title("Subvencije")
        axes[i].legend(loc=2)
axes[2].set_yscale("log")

plt.show()


"""
to do this night

2)nariši še kako so se cene gibale skozi leto za vsako leto. Torej končno povprečno ceno za vsa leta prikaži gibanje skozi vsa štiri
četrtletja

3) nariši le bar plot EUR/MWh za OVE SPTE
5)korelacija cene in subvencij+investicij?! napoved cene iz gibanja teh dveh?!

x)če bo čas nariši kot uvod premikanje dobave premoga zadnjih x desetletji :)

#####
It looks like sklearn requires the data shape of (row number, column number). If your data shape is (row number, ) like (999, ), 
it does not work. 
By using numpy.reshape, you should change to (999, 1). Ex. data.reshape((999,1)) In my case, it worked with that.

model = LinearRegression()
model.fit(subvencije_skupaj[:,0], subvencije_skupaj[:,1])
hx = model.predict(subvencije_skupaj[:,0])
print(hx)
#izracunaj korelacije?!


korelacije = {}"""


