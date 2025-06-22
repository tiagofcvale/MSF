import numpy as np
import matplotlib.pyplot as plt

# Parâmetros
g = 9.8
L = 0.5
omega0 = np.sqrt(g / L)
theta0 = 0.1
omega_initial = 0.5
dt = 0.01
t_max = 10
steps = int(t_max / dt)

# Arrays para armazenar resultados
t = np.linspace(0, t_max, steps)
theta = np.zeros(steps)
omega = np.zeros(steps)

# Condições iniciais
theta[0] = theta0
omega[0] = omega_initial

# Método de Euler
#for i in range(1, steps):
#    theta[i] = theta[i-1] + omega[i-1] * dt
#    omega[i] = omega[i-1] - (g / L) * theta[i-1] * dt

# Método de Euler-Cromer (Verlet simplificado)
for i in range(1, steps):
    omega[i] = omega[i-1] - (g / L) * theta[i-1] * dt  # Atualiza velocidade primeiro
    theta[i] = theta[i-1] + omega[i] * dt               # Depois atualiza posição

# Solução analítica
theta_analytical = theta0 * np.cos(omega0 * t) + (omega_initial / omega0) * np.sin(omega0 * t)

# Plot
plt.plot(t, theta, label='Numérico')
plt.plot(t, theta_analytical, label='Analítico', linestyle='--')
plt.xlabel('Tempo (s)')
plt.ylabel('Ângulo (rad)')
plt.legend()
plt.grid()
plt.show()

#b)

def maxminv(xm1, xm2, xm3, ym1, ym2, ym3):
    xab = xm1 - xm2
    xac = xm1 - xm3
    xbc = xm2 - xm3

    a = ym1 / (xab * xac)
    b = -ym2 / (xab * xbc)
    c = ym3 / (xac * xbc)

    xmla = (b + c) * xm1 + (a + c) * xm2 + (a + b) * xm3
    xm = 0.5 * xmla / (a + b + c)

    xta = xm - xm1
    xtb = xm - xm2
    xtc = xm - xm3

    ymax = a * xtb * xtc + b * xta * xtc + c * xta * xtb
    return xm, ymax

# Gerar dados (substitua pelos seus dados reais)
# Identificar extremos
extremes = []
for i in range(1, len(t) - 1):
    # Verifica se é um máximo ou mínimo local
    if (theta[i] > theta[i-1] and theta[i] > theta[i+1]) or (theta[i] < theta[i-1] and theta[i] < theta[i+1]):
        xm, ymax = maxminv(t[i-1], t[i], t[i+1], theta[i-1], theta[i], theta[i+1])
        extremes.append((xm, ymax))

# Separar máximos e mínimos
maxima = [ (tm, xm) for tm, xm in extremes if xm > 0 ]
minima = [ (tm, xm) for tm, xm in extremes if xm < 0 ]

# Calcular amplitude e período
if maxima:
    A = np.mean([xm for _, xm in maxima])
    times = [tm for tm, _ in maxima]
    periods = np.diff(times)
    T = np.mean(periods)
else:
    A, T = 0, 0

print(f"Amplitude: {A:.6f} m")  # Deve ser ≈4.000000
print(f"Período: {T:.6f} s")    # Deve ser ≈6.283185