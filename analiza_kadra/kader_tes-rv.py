import numpy as np
import operator
from csv import DictReader
import matplotlib
import matplotlib.pyplot as plt
import pylab

headers = ["Leto","Doktor znanosti","Magisterij","Fakulteta, visoka šola","Višja šola","Srednja šola - 4.letna","Delovodska šola - visokokvalificirana","Srednja šola - 3.letna","Ožji profil","Skupaj zaposleni"]
dataTES = np.genfromtxt("data/TES-kader-leta.csv", delimiter='\t', skip_header=True)
dataRV = np.genfromtxt("data/RVELENJE-kader-leta.csv", delimiter='\t', skip_header=True)
color = ["r", "b", "g", "y", "purple", "orange", "magenta", "cyan", "brown", "black"]

plt.style.use('ggplot')
fig = plt.figure()
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
labels = headers[1:]
for x in range(9):
    ax1.plot(dataTES[:,0], dataTES[:,x+1], color=color[x], label=labels[x])
ax1.set_xlim([2001, 2014])
ticks = np.arange(2001, 2014, 1)
ax1.set_xticks(ticks)
ax1.set_xticklabels(np.array(dataTES[:,0], dtype="int"))
ax1.set_xlabel('Leto')
ax1.set_ylabel('Št zaposlenih')
ax1.set_title('Število zaposlenih po izobraženosti TEŠ')

ax1.legend(loc = 'upper center', bbox_to_anchor = (0.5, 0.65), ncol = 3, fancybox = True, shadow = True)
plt.show()

plt.style.use('ggplot')
fig = plt.figure()
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
labels = headers[1:]
for x in range(9):
    ax1.plot(dataRV[:,0], dataRV[:,x+1], color=color[x], label=labels[x])
ax1.set_xlim([2001, 2014])
ticks = np.arange(2001, 2014, 1)
ax1.set_xticks(ticks)
ax1.set_xticklabels(np.array(dataRV[:,0], dtype="int"))
ax1.set_xlabel('Leto')
ax1.set_ylabel('Št zaposlenih')
ax1.set_title('Število zaposlenih po izobraženosti Premogovnik velenje')

ax1.legend(loc = 'upper center', bbox_to_anchor = (0.75, 1.0), ncol = 3, fancybox = True, shadow = True)
plt.show()

plt.style.use('ggplot')
fig = plt.figure()
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])
labels = ["TEŠ","Premogovnik Velenje"]
ax1.plot(dataTES[:,0], dataTES[:,-1], color="r", label=labels[0])
ax1.plot(dataRV[:,0], dataRV[:,-1], color="b", label=labels[1])
ax1.set_xlim([2001, 2014])
ticks = np.arange(2001, 2014, 1)
ax1.set_xticks(ticks)
ax1.set_xticklabels(np.array(dataTES[:,0], dtype="int"))
ax1.set_xlabel('Leto')
ax1.set_ylabel('Št zaposlenih')
ax1.set_title('Število zaposlenih')

ax1.legend(loc = 'upper center', bbox_to_anchor = (0.5, 1.0), ncol = 3, fancybox = True, shadow = True)
plt.show()

labels = headers[1:-1]

sizes = []
for i in range(8):
    sizes.append(np.mean(dataTES[:, i+1][np.isnan(dataTES[:, i+1]) == False]))

fig1, ax1 = plt.subplots()
explode = (0.5, 0.2, 0, 0, 0, 0, 0, 0)
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('Povprečen delež kadra 2001-2014 v TEŠ')
plt.show()

labels = headers[1:-1]

sizes = []
for i in range(8):
    sizes.append(np.mean(dataRV[:, i+1][np.isnan(dataRV[:, i+1]) == False]))

fig1, ax1 = plt.subplots()
explode = (0.5, 0.2, 0, 0, 0, 0, 0, 0)
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('Povprečen delež kadra 2001-2014 v premogovniku velenje')
plt.show()

i=0;