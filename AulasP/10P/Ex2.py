import numpy as np
import matplotlib.pyplot as plt

L = 1.0 #m
g = 9.81 #m/s^2	

teta = 0.1 #rad
t0 = 0.0 #s
tf = 10.0 #s
dt = 0.001 #s
v0 = 0.0 #m/s

t = np.arange(t0, tf, dt)
n = len(t)
ainst = np.zeros(np.size(t))
vang = np.zeros(np.size(t))
ang = np.zeros(np.size(t))

ang[0] = teta
vang[0] = v0

for i in range(n - 1):
    ainst[i] = -g/L * np.sin(ang[i])
    vang[i + 1] = vang[i] + ainst[i] * dt
    ang[i + 1] = ang[i] + vang[i + 1] * dt

plt.subplot(2, 1, 1)
plt.plot(t, ang, label='Angulo', color='blue')
plt.subplot(2, 1, 2)
plt.plot(t, ainst, label='Aceleração', color='orange')
plt.title('Angulo')
plt.xlabel('Tempo (s)')
plt.ylabel('Angulo (rad)')
plt.grid()
plt.show()

def maxminv(xm1,xm2,xm3,ym1,ym2,ym3):  
    # Máximo ou mínimo usando o polinómio de Lagrange
    # Dados (input): (x0,y0), (x1,y1) e (x2,y2) 
    # Resultados (output): xm, ymax 
    xab=xm1-xm2
    xac=xm1-xm3
    xbc=xm2-xm3

    a=ym1/(xab*xac)
    b=-ym2/(xab*xbc)
    c=ym3/(xac*xbc)

    xmla=(b+c)*xm1+(a+c)*xm2+(a+b)*xm3
    xm=0.5*xmla/(a+b+c)

    xta=xm-xm1
    xtb=xm-xm2
    xtc=xm-xm3

    ymax=a*xtb*xtc+b*xta*xtc+c*xta*xtb
    return xm, ymax

angmax = np.zeros(np.size(t))
angmax[0] = teta

tmax = []
angmax = []
tmin = []
angmin = []

for i in range(1, n-1):
    # Máximo local
    if ang[i] > ang[i-1] and ang[i] > ang[i+1]:
        tm, angm = maxminv(t[i-1], t[i], t[i+1], ang[i-1], ang[i], ang[i+1])
        tmax.append(tm)
        angmax.append(angm)
    # Mínimo local
    if ang[i] < ang[i-1] and ang[i] < ang[i+1]:
        tm, angm = maxminv(t[i-1], t[i], t[i+1], ang[i-1], ang[i], ang[i+1])
        tmin.append(tm)
        angmin.append(angm)

plt.subplot(2, 1, 1)
plt.plot(t, ang, label='Angulo', color='blue')
plt.plot(tmax, angmax, 'ro', label='Maximo')
plt.plot(tmin, angmin, 'go', label='Minimo')
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(t, ainst, label='Aceleração', color='orange')
plt.title('Angulo')
plt.xlabel('Tempo (s)')
plt.ylabel('Angulo (rad)')
plt.grid()
plt.show()

deltaTcomp = tmax[1] - tmax[0]
print("Período computacional: {:.4f}".format(deltaTcomp))

deltaTan = 2*np.pi*np.sqrt(L/g)
print("Período analitico: {:.4f}".format(deltaTan))