import numpy as np
import matplotlib.pyplot as plt


L = 1.0 #m
g = 9.81 #m/s^2	


#a)
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

# Plotar os resultados

plt.subplot(2, 1, 1)
plt.plot(t, ang, label='Angulo', color='blue')
plt.subplot(2, 1, 2)
plt.plot(t, ainst, label='Aceleração', color='orange')
plt.title('Angulo')
plt.xlabel('Tempo (s)')
plt.ylabel('Angulo (rad)')
plt.grid()
plt.show()

#b)
A = 0.1 #m
phi = 0.0 #rad
ang_a = A * np.cos(np.sqrt(g/L) * t + phi)
plt.subplot(2, 1, 1)
plt.plot(t, ang_a, label='Angulo b', color='blue')
plt.subplot(2, 1, 2)
plt.plot(t, ang, label='Angulo a', color='blue')
plt.title('Angulo')
plt.xlabel('Tempo (s)')
plt.ylabel('Angulo (rad)')
plt.grid()
plt.show()

#c)

teta = 0.3 #rad
t0 = 0.0 #s
tf = 10.0 #s
dt = 0.001 #s
v0 = 0.0 #m/s
teta2 = 0.5 #rad

t = np.arange(t0, tf, dt)
n = len(t)
ainst = np.zeros(np.size(t))
ainst2 = np.zeros(np.size(t))

vang = np.zeros(np.size(t))
vang2 = np.zeros(np.size(t))

ang = np.zeros(np.size(t))
ang2 = np.zeros(np.size(t))

ang2[0] = teta2
ang[0] = teta
vang[0] = v0
vang2[0] = v0

for i in range(n - 1):
    ainst[i] = -g/L * np.sin(ang[i])
    vang[i + 1] = vang[i] + ainst[i] * dt
    ang[i + 1] = ang[i] + vang[i + 1] * dt

    ainst2[i] = -g/L * np.sin(ang2[i])
    vang2[i + 1] = vang2[i] + ainst2[i] * dt
    ang2[i + 1] = ang2[i] + vang2[i + 1] * dt

# Plotar os resultados
plt.title('Angulo')
plt.plot(t, ang, label='Angulo 0.3 rad', color='blue')
plt.plot(t, ang2, label='Angulo 0.5 rad', color='orange')
plt.xlabel('Tempo (s)')
plt.ylabel('Angulo (rad)')
plt.legend()
plt.grid()
plt.show()

