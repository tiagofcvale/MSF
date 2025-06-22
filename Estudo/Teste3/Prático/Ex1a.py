import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do sistema
k = 1.0       # N/m
alpha = 0.05  # N/m²
m = 1.0       # kg

# Função de energia potencial
def Ep(x):
    return 0.5 * k * x**2 + alpha * x**3

# Função de aceleração (F = ma)
def acelera(t, estado):
    x, vx = estado  # estado = [x, vx]
    ax = (-k * x - 3 * alpha * x**2) / m
    return np.array([vx, ax])

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

# Simulação do movimento
def simular(x0, v0, dt=0.01, t_total=50):
    t = np.arange(0, t_total, dt)
    x = np.zeros_like(t)
    v = np.zeros_like(t)
    
    estado = np.array([x0, v0])  # Estado inicial [x, v]
    
    for i in range(len(t)):
        x[i], v[i] = estado
        estado = rk4(t[i], estado, acelera, dt)
    
    return t, x, v

# (a) Diagrama de energia potencial
x_vals = np.linspace(-8, 4, 1000)
plt.figure(figsize=(10, 6))
plt.plot(x_vals, Ep(x_vals), label='$E_p(x) = \\frac{1}{2}kx^2 + \\alpha x^3$')
plt.xlabel('x (m)')
plt.ylabel('Energia Potencial (J)')
plt.title('Diagrama de Energia Potencial')
plt.grid(True)

# Energias de referência
plt.axhline(y=7, color='r', linestyle='--', label='E = 7 J')
plt.axhline(y=8, color='g', linestyle='--', label='E = 8 J')
plt.legend()

# Análise para diferentes energias
def analisar_energia(x0, E_target):
    v0 = np.sqrt(2*(E_target - Ep(x0))/m)
    t, x, v = simular(x0, v0)
    
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(t, x)
    plt.title(f'Posição x Tempo (E = {E_target} J)')
    plt.xlabel('Tempo (s)')
    plt.ylabel('x (m)')
    
    plt.subplot(1, 2, 2)
    plt.plot(x, v)
    plt.title(f'Espaço de Fases (E = {E_target} J)')
    plt.xlabel('x (m)')
    plt.ylabel('v (m/s)')
    plt.tight_layout()
    plt.show()

# Caso E < 7J (usando x0 = 2m)
analisar_energia(x0=2.0, E_target=6.0)

# Caso E > 8J (usando x0 = 3m)
analisar_energia(x0=3.0, E_target=9.0)

plt.show()