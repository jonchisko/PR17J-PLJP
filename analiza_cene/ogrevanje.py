import numpy as np
import operator
from csv import DictReader
import matplotlib
import matplotlib.pyplot as plt
import pylab


reader = DictReader(open("/Users/jonskoberne/PycharmProjects/energetika/nalogab/cene_koncna.csv", "rt", encoding="utf-8"))
leto = []
vsiD = [[] for x in range(6)]
for row in reader:
    vsiD[0].append(row["D - Slovenija"])
    leto.append(row["leto"])
reader = DictReader(open("/Users/jonskoberne/PycharmProjects/energetika/nalogab/cene_energija.csv", "rt", encoding="utf-8"))
for row in reader:
    vsiD[1].append(row["D - Slovenija"])
reader = DictReader(open("/Users/jonskoberne/PycharmProjects/energetika/nalogab/cene_omreznina.csv", "rt", encoding="utf-8"))
for row in reader:
    vsiD[2].append(row["D - Slovenija"])
reader = DictReader(open("/Users/jonskoberne/PycharmProjects/energetika/nalogab/cene_trosarina.csv", "rt", encoding="utf-8"))
for row in reader:
    value = row["D - Slovenija"]
    if value == "..":
        value = None
    vsiD[3].append(value)
reader = DictReader(open("/Users/jonskoberne/PycharmProjects/energetika/nalogab/cene_ddv.csv", "rt", encoding="utf-8"))
for row in reader:
    vsiD[4].append(row["D - Slovenija"])
reader = DictReader(open("/Users/jonskoberne/PycharmProjects/energetika/nalogab/cene_dajatve.csv", "rt", encoding="utf-8"))
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

"""
nariši še bar plot, ki bo za vsako leto imel za vse porabniske skupine tak stolpic kot je prejsnji graf
lahko vidiš primerjavo cen glede na porabniško skupino!
"""



#korelacija s subvencijami?
#Skupaj OVE + SPTE, subvecnije obnovljivi
#Znesek pomoci (EUR), subvecnije rjavi premog

reader = DictReader(open("/Users/jonskoberne/PycharmProjects/energetika/nalogab/subvencija_obnovljivi_visokizkoristek.csv", "rt", encoding="utf-8"))
sub_obn = []
leto_s = []
for row in reader:
    sub_obn.append(row["Skupaj OVE + SPTE"])
    leto_s.append(row["leto"])
reader = DictReader(open("nalogab/subvecnije_rud_trbov_hrastnik_rjavi_premog.csv", "rt", encoding="utf-8"))
sub_rjv = []
leto_m = []
for row in reader:
    sub_rjv.append(row["Znesek pomoci (EUR)"])
    leto_m.append(row["leto"])

#subvencije data gre od leta 2004 do 2016, vkljucno
#premog data gre od 2001 do 2012 vkljucno
#tedva data imata leta na drugem mestu, ker sem tako dodal skupaj kot vidite - zapomni si!
from scipy import stats
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.metrics import mean_squared_error

sub_data = np.column_stack((np.array(sub_obn, dtype="float"), np.array(leto_s, dtype="float")))
rjv_data = np.column_stack((np.array(sub_rjv, dtype="float"), np.array(leto_m, dtype="float")))

subvencije_skupaj = np.zeros((16, 2))
subvencije_skupaj[0:12, 1] += rjv_data[:, 0]
subvencije_skupaj[3:, 1] += sub_data[:, 0]
subvencije_skupaj[:, 0] = np.arange(2001, 2017,1)
#prikazi subvencije
fig, axes = plt.subplots(figsize=(6,6))
axes.plot(subvencije_skupaj[:,0], subvencije_skupaj[:,1], color="r", label="skupaj")
axes.plot(sub_data[:,1], sub_data[:,0], color="g", label="obnovljivi viri")
axes.plot(rjv_data[:,1], rjv_data[:,0], color="b", label="rjavi premog")
axes.set_xlim(2001,2017)
ticks = np.arange(2001, 2017, 1)
axes.set_xticks(ticks)
axes.set_xticklabels = subvencije_skupaj[:, 0]
axes.set_title("Subvencije")
axes.set_xlabel("Leto")
axes.set_ylabel("EUR")
axes.legend(loc=2)
plt.show()
"""
It looks like sklearn requires the data shape of (row number, column number). If your data shape is (row number, ) like (999, ), 
it does not work. 
By using numpy.reshape, you should change to (999, 1). Ex. data.reshape((999,1)) In my case, it worked with that.
"""
model = LinearRegression()
model.fit(subvencije_skupaj[:,0], subvencije_skupaj[:,1])
hx = model.predict(subvencije_skupaj[:,0])
print(hx)
#izracunaj korelacije?!


korelacije = {}


