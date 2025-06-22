import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do sistema
m = 1.0       # kg
alpha = 0.15  # N/m^4
b = 0.02      # kg/s
F0 = 7.5      # N
omega_f = 1.0 # rad/s

# Função de aceleração (inclui força do potencial, amortecimento e força externa)
def acelera(t, x, vx):
    return (-4*alpha*x**3 - b*vx + F0*np.cos(omega_f*t)) / m

# Implementação do RK4 (conforme fornecido)
def rk4_x_vx(t, x, vx, acelera, dt):
    ax1 = acelera(t, x, vx)
    c1v = ax1*dt
    c1x = vx*dt
    ax2 = acelera(t+dt/2., x+c1x/2., vx+c1v/2.)
    c2v = ax2*dt
    c2x = (vx+c1v/2.)*dt
    ax3 = acelera(t+dt/2., x+c2x/2., vx+c2v/2.)
    c3v = ax3*dt
    c3x = (vx+c2v/2.)*dt
    ax4 = acelera(t+dt, x+c3x, vx+c3v)
    c4v = ax4*dt
    c4x = (vx+c3v)*dt
    xp = x + (c1x + 2.*c2x + 2.*c3x + c4x)/6.
    vxp = vx + (c1v + 2.*c2v + 2.*c3v + c4v)/6.
    return xp, vxp

# Condições iniciais
x0 = 2.0  # m
v0 = 0.0  # m/s

# Parâmetros da simulação
dt = 0.01      # Passo temporal
t_total = 50   # Tempo total de simulação
n_passos = int(t_total/dt)

# Arrays para armazenar resultados
t = np.zeros(n_passos)
x = np.zeros(n_passos)
v = np.zeros(n_passos)

# Integração numérica usando RK4
x_current, v_current = x0, v0
for i in range(n_passos):
    t[i] = i * dt
    x[i], v[i] = x_current, v_current
    x_current, v_current = rk4_x_vx(t[i], x_current, v_current, acelera, dt)

# Gráficos
plt.figure(figsize=(14, 5))

# Gráfico 1: Posição vs Tempo
plt.subplot(1, 2, 1)
plt.plot(t, x)
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Posição vs Tempo')
plt.grid(True)

# Gráfico 2: Espaço de Fase
plt.subplot(1, 2, 2)
plt.plot(x, v)
plt.xlabel('Posição (m)')
plt.ylabel('Velocidade (m/s)')
plt.title('Espaço de Fase')
plt.grid(True)

plt.tight_layout()
plt.show()