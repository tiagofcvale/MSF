import numpy as np
import matplotlib.pyplot as plt

#Condições iniciais
x0 = 0
vx0 = 0
g = 9.8
t0 = 0
tf = 10
dt = 0.001
y0 = 0.1

def y_func(x:float) -> float:
    return 0.1 - 0.05 * x if x < 2.0 else 0.0

def dydx_func(x:float) -> float:
    return -0.05* g if x < 2.0 else 0.0

t = np.arange(t0, tf, dt)

ax = np.zeros(np.size(t))
vx = np.zeros(np.size(t))
vx[0] = vx0

x = np.zeros(np.size(t))
x[0] = x0
y = np.zeros(np.size(t))
y[0] = y0

t25 = None
v25 = None

for i in range(np.size(t) - 1):

    # Aceleração
    ax[i] = -g * dydx_func(x[i])

    # Método de Euler-Cromer
    vx[i + 1] = vx[i] + ax[i] * dt
    x[i + 1] = x[i] + vx[i + 1] * dt
    y[i + 1] = y_func(x[i])

    # Verificar se a bola atinge ou ultrapassa x = 2.5
    if x[i + 1] >= 2.5 and t25 is None:
        t25 = t[i + 1]
        v25 = vx[i + 1]


print("Tempo em que a bola atinge 2.5 m: {:.3f} s".format(t25))
print("Velocidade em que a bola atinge 2.5 m: {:.3f} m/s".format(v25))


fig, ax1 = plt.subplots()
color = 'tab:blue'
ax1.set_xlabel('time (s)')
ax1.set_ylabel('x (m)', color=color)
ax1.plot(t[x<2.5], x[x<2.5], color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # partilhar eixo horizontal

color = 'tab:red'
ax2.set_ylabel('y', color = color)
ax2.plot(t[x<2.5], y[x<2.5], color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # para evitar sobreposição de labels
plt.show()
