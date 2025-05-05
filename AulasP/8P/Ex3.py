import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do problema
m = 2000  # massa (kg)
P = 40000  # potência (W)
theta = np.radians(5)  # ângulo de inclinação (rad)
mu = 0.04  # coeficiente de rolamento
C_res = 0.25  # coeficiente de resistência do ar
A = 2  # área frontal (m²)
rho_ar = 1.225  # densidade do ar (kg/m³)
g = 9.81  # aceleração gravítica (m/s²)
v0 = 1  # velocidade inicial (m/s)
x0 = 0  # posição inicial (m)
distancia_alvo = 2000  # distância a percorrer (m)

# Configuração da simulação
dt = 0.1  # passo de tempo (s)
t_max = 300  # tempo máximo de simulação (s)
n_steps = int(t_max/dt)  # número de passos

# Função de integração trapezoidal corrigida
def integral(f, D, a, b):
    dt_int = D[1] - D[0]  # intervalo de tempo entre pontos
    i_a = int(np.floor((a - D[0]) / dt_int).clip(0, len(f)-1))
    i_b = int(np.ceil((b - D[0]) / dt_int).clip(0, len(f)-1))
    
    if i_b <= i_a:
        return 0.0
    
    sum = 0.0
    for i in range(i_a, i_b):
        if i+1 < len(f):  # Verifica se não estamos no último elemento
            sum += (f[i] + f[i+1]) / 2.0 * dt_int
    return sum

# Arrays para armazenar resultados
t = np.linspace(0, t_max, n_steps)
x = np.zeros(n_steps)
v = np.zeros(n_steps)
a = np.zeros(n_steps)
F_motor = np.zeros(n_steps)

# Condições iniciais
x[0] = x0
v[0] = v0

# Função para calcular a força resultante
def forcas(v_current):
    F_motor = P / max(v_current, 0.1)  # Evita divisão por zero
    P_x = -m * g * np.sin(theta)
    F_rol = -mu * m * g * np.cos(theta)
    F_res = -0.5 * C_res * A * rho_ar * v_current * abs(v_current)
    return F_motor + P_x + F_rol + F_res

# Simulação usando método de Euler
for i in range(n_steps-1):
    F_res = forcas(v[i])
    a[i] = F_res / m
    v[i+1] = v[i] + a[i] * dt
    x[i+1] = x[i] + v[i] * dt
    F_motor[i] = P / max(v[i], 0.1)  # Armazena a força do motor

# Preenche o último valor de F_motor
F_motor[-1] = P / max(v[-1], 0.1)

# Encontrar quando atinge 2km
idx_2km = np.argmax(x >= distancia_alvo)
tempo_2km = t[idx_2km] if idx_2km > 0 else float('inf')

# Cálculo do trabalho realizado pelo motor
trabalho_potencia = P * tempo_2km
trabalho_integral = integral(F_motor*v, t, 0, min(tempo_2km, t[-1]))  # Limita ao tempo máximo

# Resultados
print(f"Tempo para percorrer 2 km: {tempo_2km:.2f} segundos")
print(f"Trabalho calculado pela potência: {trabalho_potencia/1000:.2f} kJ")
print(f"Trabalho calculado pela integral: {trabalho_integral/1000:.2f} kJ")
print(f"Velocidade final: {v[-1]:.2f} m/s ({v[-1]*3.6:.2f} km/h)")

# Gráficos
plt.figure(figsize=(12, 8))

# Posição vs tempo
plt.subplot(2, 1, 1)
plt.plot(t, x, label='Posição')
plt.axhline(y=distancia_alvo, color='r', linestyle='--', label='2 km')
if tempo_2km != float('inf'):
    plt.axvline(x=tempo_2km, color='g', linestyle=':', label=f'Tempo: {tempo_2km:.1f} s')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Posição do Carro ao Longo do Tempo')
plt.legend()
plt.grid(True)

# Velocidade vs tempo
plt.subplot(2, 1, 2)
plt.plot(t, v, label='Velocidade', color='orange')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.title('Velocidade do Carro ao Longo do Tempo')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()