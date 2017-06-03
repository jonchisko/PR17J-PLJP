import numpy as np
import operator
from csv import DictReader
import matplotlib
import matplotlib.pyplot as plt
import pylab

headersRV = ["Leto","Doktor znanosti","Magisterij","Fakulteta, visoka šola","Višja šola","Srednja šola - 4.letna","Delovodska šola - visokokvalificirana","Srednja šola - 3.letna","Ožji profil","Skupaj zaposleni"]
headersIZKOP = ["leto","1000t"]

dataIZKOP = np.genfromtxt("data/RVELENJE-izkop-leta.csv", delimiter='\t', skip_header=True)
dataRV = np.genfromtxt("data/RVELENJE-kader-leta.csv", delimiter='\t', skip_header=True)
color = ["r", "b", "g", "y", "purple", "orange", "magenta", "cyan", "brown", "black"]


plt.style.use('ggplot')
fig = plt.figure()
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
labels = ["Izkop na zaposlenega"]
ax1.plot(dataRV[0:11,0], dataIZKOP[0:11,-1]/dataRV[0:11,-1], color="r", label=labels[0])
ax1.set_xlim([2001, 2011])
ticks = np.arange(2001, 2011, 1)
ax1.set_xticks(ticks)
ax1.set_xticklabels(np.array(dataRV[:,0], dtype="int"))
ax1.set_xlabel('Leto')
ax1.set_ylabel('Izkop na zasposlenega (1000t)')
ax1.set_title('Izkop na zaposlenega')
plt.show()