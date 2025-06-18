import numpy as np
import matplotlib.pyplot as plt

k = 1 #N/m
dk = 0.5 #N/m
m = 1 #kg
xAeq = 1 #m
xBeq = 2 #m

#i)
xA0 = xAeq + 0.3
xB0 = xBeq + 0.3
VAx0 = VBx0 = 0 #m/s

dt = 0.01 #s
tf = 200 #s
t = np.arange(0, tf, dt)
n = len(t)

xA = np.zeros(n)
xB = np.zeros(n)
vA = np.zeros(n)
vB = np.zeros(n)
FA = np.zeros((2, n))
FB = np.zeros((2, n))

for i in range(n-1):
    FA[0,i] = (dk * xA[1,i] -xAeq[1]) - (k + dk) * (xA[0,i] - xAeq[0]) / m
    FB[0,i] = (dk * xB[1,i] -xBeq[1]) - (k + dk) * (xB[0,i] - xBeq[0]) / m

    vA[i+1] = vA[i] + (FA[0,i]/m)*dt
    vB[i+1] = vB[i] + (FB[0,i]/m)*dt

    xA[i+1] = xA[i] + vA[i+1]*dt
    xB[i+1] = xB[i] + vB[i+1]*dt

plt.plot(t, xA, label='xA(t)')
plt.plot(t, xB, label='xB(t)')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Lei do movimento dos dois corpos acoplados')
plt.legend()
plt.grid()
plt.show()

#ii)

xA0 = xAeq + 0.3
xB0 = xBeq - 0.3
VAx0 = VBx0 = 0 #m/s

dt = 0.01 #s
tf = 200 #s
t = np.arange(0, tf, dt)
n = len(t)

xA = np.zeros(n)
xB = np.zeros(n)
vA = np.zeros(n)
vB = np.zeros(n)

for i in range(n-1):
    FA = -k * (xA[i] - xAeq) - dk * (xA[i] - xAeq) + dk * (xB[i] - xBeq)
    FB = -k * (xB[i] - xBeq) - dk * (xB[i] - xBeq) + dk * (xA[i] - xAeq)

    vA[i+1] = vA[i] + (FA/m)*dt
    vB[i+1] = vB[i] + (FB/m)*dt

    xA[i+1] = xA[i] + vA[i+1]*dt
    xB[i+1] = xB[i] + vB[i+1]*dt

plt.plot(t, xA, label='xA(t)')
plt.plot(t, xB, label='xB(t)')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Lei do movimento dos dois corpos acoplados (caso ii)')
plt.legend()
plt.grid()
plt.show()
