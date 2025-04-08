import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# Condições iniciais
x0 = 0
vx0 = 0
g = 9.8
t0 = 0
tf = 10
dt = 0.001
y0 = 0.1


Sx = sp.symbols('x')
f_x = 0.025 * (Sx - 2)**2
f_vx = sp.diff(f_x, Sx)  
f_ax = sp.diff(f_vx, Sx) 

print("A expressão para a aceleração horizontal é: {:.2f}g".format(f_ax))

# Funções para y(x) e dy/dx
def y_func(x: float) -> float:
    return 0.025 * (x - 2)**2 if x < 2.0 else 0.0

def dydx_func(x: float) -> float:
    return 0.05  if x < 2.0 else 0.0

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

    vx[i + 1] = vx[i] + ax[i] * dt
    x[i + 1] = x[i] + vx[i + 1] * dt
    y[i + 1] = y_func(x[i])

    
    if x[i + 1] >= 2.5 and t25 is None:
        t25 = t[i + 1]
        v25 = vx[i + 1]
        break 

# Resultados
print(f"Tempo em que a bola atinge x = 2.5 m: {t25} s")
print(f"Velocidade final da simulação: {v25} m/s")
print("Foi mais devagar que o Ex1")

# Gráficos
fig, ax1 = plt.subplots()
color = 'tab:blue'
ax1.set_xlabel('time (s)')
ax1.set_ylabel('x (m)', color=color)
ax1.plot(t[:i + 2], x[:i + 2], color=color)  # Apenas até x = 2.5
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # Partilhar eixo horizontal

color = 'tab:red'
ax2.set_ylabel('y', color=color)
ax2.plot(t[:i + 2], y[:i + 2], color=color)  # Apenas até x = 2.5
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # Para evitar sobreposição de labels
plt.show()