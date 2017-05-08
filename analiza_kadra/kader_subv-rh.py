import numpy as np
import operator
from csv import DictReader
import matplotlib
import matplotlib.pyplot as plt
import pylab

headersRH = ["Leto","Doktor znanosti","Magisterij","Fakulteta, visoka šola","Višja šola","Srednja šola - 4.letna","Delovodska šola - visokokvalificirana","Srednja šola - 3.letna","Ožji profil","Skupaj zaposleni"]
headersSUBV = ["leto","Kolicine (GWh)","Znesek pomoci (SIT)","Znesek pomoci (EUR)","Visina pomoci (EUR/MWh)","Kolicina domacega energenta (tone)"]


dataSUBV = np.genfromtxt("data/subvecnije_rud_trbov_hrastnik_rjavi_premog.csv", delimiter=',', skip_header=True)
dataRH = np.genfromtxt("data/RHRASTNIK-kader-leta.csv", delimiter='\t', skip_header=True)
color = ["r", "b", "g", "y", "purple", "orange", "magenta", "cyan", "brown", "black"]


plt.style.use('ggplot')
fig = plt.figure()
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
labels = headersRH[1:]
for x in range(9):
    ax1.plot(dataRH[:,0], dataRH[:,x+1], color=color[x], label=labels[x])
ax1.plot(dataRH[:,0], dataSUBV[:,-2]*10, color="black", label="Visina pomoci (EUR/10MWh)",linewidth=4.0)
ax1.set_xlim([2001, 2012])
ticks = np.arange(2001, 2012, 1)
ax1.set_xticks(ticks)
ax1.set_xticklabels(np.array(dataRH[:,0], dtype="int"))
ax1.set_xlabel('Leto')
ax1.set_ylabel('Št zaposlenih')
ax1.set_title('Število zaposlenih po izobraženosti Rudnik Hrastnik, višina subvencije na EUR/10MWh')
ax1.legend(loc = 'upper center', bbox_to_anchor = (0.7, 1), ncol = 3, fancybox = True, shadow = True)
plt.show()

