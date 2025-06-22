import numpy as np
import matplotlib.pyplot as plt

# a)
# Parâmetros
dt = 0.01          # Passo de tempo
t_max = 20         # Tempo total de simulação
steps = int(t_max / dt)  # Número de passos

# Arrays para armazenar resultados
t = np.linspace(0, t_max, steps)
x = np.zeros(steps)
v = np.zeros(steps)

# Condições iniciais
x[0] = 4    # Posição inicial
v[0] = 0    # Velocidade inicial

# Método de Euler-Cromer
for i in range(steps - 1):
    v[i+1] = v[i] - x[i] * dt       # Atualiza velocidade
    x[i+1] = x[i] + v[i+1] * dt     # Atualiza posição com a nova velocidade

# Plot
plt.figure(figsize=(10, 5))
plt.plot(t, x, label='Posição $x(t)$ (Euler-Cromer)', color='blue')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Movimento do Oscilador Harmônico (Euler-Cromer)')
plt.grid(True)
plt.legend()
plt.show()

# b)

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



# Identificar extremos
extremes = []
for i in range(1, len(t) - 1):
    # Verifica se é um máximo ou mínimo local
    if (x[i] > x[i-1] and x[i] > x[i+1]) or (x[i] < x[i-1] and x[i] < x[i+1]):
        xm, ymax = maxminv(t[i-1], t[i], t[i+1], x[i-1], x[i], x[i+1])
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

# Plotar resultados
plt.figure(figsize=(12, 4))
plt.plot(t, x, label='Posição $x(t)$', color='blue')
plt.scatter(*zip(*maxima), color='red', label='Máximos')
plt.scatter(*zip(*minima), color='green', label='Mínimos')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Oscilador Harmônico: Extremos Detectados')
plt.legend()
plt.grid()
plt.show()

# c) Energia mecânica total

# Dados da simulação (substitua pelos seus arrays reais)
# Exemplo com solução analítica para comparação:
t = np.linspace(0, 10 * np.pi, 5000)
x = 4 * np.cos(t)
v = -4 * np.sin(t)  # Derivada de x(t)

# Energias
K = 0.5 * 1 * v**2            # Energia cinética (m = 1 kg)
U = 0.5 * 1 * x**2             # Energia potencial (k = 1 N/m)
E = K + U                      # Energia mecânica total

# Plot
plt.figure(figsize=(10, 5))
plt.plot(t, E, label='Energia mecânica $E(t)$', color='purple')
plt.axhline(y=8, linestyle='--', color='red', label='Energia teórica (8 J)')
plt.xlabel('Tempo (s)')
plt.ylabel('Energia (J)')
plt.title('Conservação de Energia no Oscilador Harmônico')
plt.legend()
plt.grid()
plt.show()

print("Energia mecânica total é constante e igual a {} como esperado.".format(np.mean(E)))