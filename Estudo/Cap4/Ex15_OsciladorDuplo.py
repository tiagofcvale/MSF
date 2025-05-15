import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do sistema
k = 1  # N/m
x_eq = 2  # m
m = 1  # kg

# Definindo a função de energia potencial
def potential_energy(x):
    return 0.5 * k * (np.abs(x) - x_eq)**2

# Criando um array de valores de x
x = np.linspace(-5, 5, 500)

# Calculando a energia potencial para cada x
Ep = potential_energy(x)

# Plotando o gráfico
plt.figure(figsize=(8, 6))
plt.plot(x, Ep, 'b-', linewidth=2)
plt.title('Diagrama de Energia Potencial do Oscilador Duplo', fontsize=14)
plt.xlabel('Posição x (m)', fontsize=12)
plt.ylabel('Energia Potencial $E_p$ (J)', fontsize=12)

# Marcando os pontos de equilíbrio
plt.plot(x_eq, 0, 'ro', markersize=8, label=f'$x_{{eq}} = {x_eq}$ m')
plt.plot(-x_eq, 0, 'ro', markersize=8)

plt.legend(fontsize=12)
plt.show()

# PARTE 2: Simulação com E_total = 1J 

def Fx(x):
    if x > 0:
        return -k * (x - x_eq)  # Região x > 0
    else:
        return k * (-x - x_eq)  # Região x < 0


E_total = 1  # J
dt = 0.01
t1 = np.arange(0, 10, dt)
x1 = np.zeros_like(t1)
v1 = np.zeros_like(t1)

x1[0] = x_eq + np.sqrt(2 * E_total / k)
v1[0] = 0.0

for i in range(1, len(t1)):
    a = Fx(x1[i-1]) / m
    v1[i] = v1[i-1] + a * dt
    x1[i] = x1[i-1] + v1[i-1] * dt

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(t1, x1, label='x(t)', color='blue')
plt.axhline(x_eq, color='green', linestyle='--', label='x_eq = 2 m')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Movimento (E = 1J)')
plt.legend()
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(t1, v1, label='v(t)', color='orange')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.title('Velocidade (E = 1J)')
plt.grid()
plt.legend()
plt.show()

print("Vai executar movimento oscilatório como um oscilador harmónico simples, à volta do ponto de equilíbrio mais perto à posição inicial")

# PARTE 3: SOLUÇÃO PARA E_total = 0.75J 


E_total = 0.75

# 1. Amplitude e pontos de retorno (relativos a Xeq = 0)
A = np.sqrt(2 * E_total / k)  # 1.225 m
print(f"Amplitude: A = {A:.3f} m (relativa a Xeq = 0)")

# 2. Frequência (oscilador harmônico simples)
omega = np.sqrt(k / m)  # 1 rad/s
freq = omega / (2 * np.pi)
print(f"Frequência angular: ω = {omega:.3f} rad/s")
print(f"Frequência: f = {freq:.3f} Hz")

# 3. Lei do movimento analítica (Xeq = 0)
def x_analitico(t):
    return A * np.cos(omega * t)  # x(t) = 1.225 cos(t)

def v_analitico(t):
    return -A * omega * np.sin(omega * t)

# 4. Simulação numérica com condições iniciais x₀=1.225m, v₀=0m/s
t2 = np.arange(0, 10, dt)
x2 = np.zeros(np.size(t2))
v2 = np.zeros(np.size(t2))

x2[0] = A  
v2[0] = 0  

for i in range(1, len(t2)):
    F = -k * x2[i-1]  
    v2[i] = v2[i-1] + (F/m) * dt
    x2[i] = x2[i-1] + v2[i-1] * dt

# 5. Gráficos comparativos
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(t2, x_analitico(t2), label='Analítico: 1.225 cos(t)', color='blue')
plt.plot(t2, x2, '--', label='Numérico (Euler)', color='red')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Lei do Movimento (E=0.75J)')
plt.legend()
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(x2, v2, label='Diagrama de Fase', color='green')
plt.xlabel('Posição (m)')
plt.ylabel('Velocidade (m/s)')
plt.title('Espaço de Fase')
plt.grid()
plt.legend()
plt.show()

#PARTE 4: Simulação com E_total = 1.5J

E_total = 1.5

# 1. Amplitude e pontos de retorno (relativos a Xeq = 0)
A = np.sqrt(2 * E_total / k)  # 1.225 m
print(f"Amplitude: A = {A:.3f} m (relativa a Xeq = 0)")

# 2. Frequência (oscilador harmônico simples)
omega = np.sqrt(k / m)  # 1 rad/s
freq = omega / (2 * np.pi)
print(f"Frequência angular: ω = {omega:.3f} rad/s")
print(f"Frequência: f = {freq:.3f} Hz")

# 3. Lei do movimento analítica (Xeq = 0)
def x_analitico(t):
    return A * np.cos(omega * t)  # x(t) = 1.225 cos(t)

def v_analitico(t):
    return -A * omega * np.sin(omega * t)

# 4. Simulação numérica com condições iniciais x₀=1.225m, v₀=0m/s
t2 = np.arange(0, 10, dt)
x2 = np.zeros(np.size(t2))
v2 = np.zeros(np.size(t2))

x2[0] = A  
v2[0] = 0  

for i in range(1, len(t2)):
    F = -k * x2[i-1]  
    v2[i] = v2[i-1] + (F/m) * dt
    x2[i] = x2[i-1] + v2[i-1] * dt

# 5. Gráficos comparativos
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(t2, x_analitico(t2), label='Analítico: 1.225 cos(t)', color='blue')
plt.plot(t2, x2, '--', label='Numérico (Euler)', color='red')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Lei do Movimento (E=0.75J)')
plt.legend()
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(x2, v2, label='Diagrama de Fase', color='green')
plt.xlabel('Posição (m)')
plt.ylabel('Velocidade (m/s)')
plt.title('Espaço de Fase')
plt.grid()
plt.legend()
plt.show()

print("Com  x0= 1.732m/s, vx0 = 0m/s temos  𝑥(𝑡) = 1.732 cos(𝜔𝑡) com 𝜔 = 1rad/s.")