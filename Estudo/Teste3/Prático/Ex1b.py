import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do sistema
k = 1.0       # N/m
alpha = 0.05  # N/m²
m = 1.0       # kg

# Função de energia potencial
def Ep(x):
    return 0.5 * k * x**2 + alpha * x**3

# Função de força
def F(x):
    return -k * x - 3 * alpha * x**2

# Implementação do RK4 (conforme fornecido)
def rk4(t, estado, acelera, dt):
    ax1 = acelera(t, estado)
    c1v = ax1 * dt
    ax2 = acelera(t + dt/2., estado + c1v/2.)
    c2v = ax2 * dt
    ax3 = acelera(t + dt/2., estado + c2v/2.)
    c3v = ax3 * dt
    ax4 = acelera(t + dt, estado + c3v)
    c4v = ax4 * dt
    estado_novo = estado + (c1v + 2.*c2v + 2.*c3v + c4v)/6.
    return estado_novo

# Função de aceleração (dv/dt = F/m)
def acelera(t, estado):
    x, v = estado
    return np.array([v, F(x)/m])

# Condições iniciais
x0 = 2.2  # m
v0 = 0.0  # m/s
estado_inicial = np.array([x0, v0])

# Parâmetros da simulação
dt = 0.01       # Passo temporal
t_total = 50    # Tempo total de simulação
n_passos = int(t_total/dt)

# Arrays para armazenar resultados
t = np.zeros(n_passos)
x = np.zeros(n_passos)
v = np.zeros(n_passos)

# Integração numérica usando RK4
estado = estado_inicial.copy()
for i in range(n_passos):
    t[i] = i * dt
    x[i], v[i] = estado
    estado = rk4(t[i], estado, acelera, dt)

# Cálculo da energia mecânica inicial
E0 = Ep(x0) + 0.5 * m * v0**2
print(f"Energia mecânica inicial: {E0:.4f} J")

# Gráficos
plt.figure(figsize=(14, 5))

# Gráfico 1: Posição vs Tempo
plt.subplot(1, 2, 1)
plt.plot(t, x)
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title(f'Posição vs Tempo (x0 = {x0} m, v0 = {v0} m/s)')
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