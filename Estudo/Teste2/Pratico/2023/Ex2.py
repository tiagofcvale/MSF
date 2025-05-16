import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do sistema
m = 2000  # massa (kg)
P = 40000  # Potência em Watts (40 kW)
theta = np.radians(5)  # inclinação em radianos
g = 9.81  # gravidade
v0 = 1.0  # velocidade inicial (m/s)

# Resistências
mu = 0.04  # coef. rolamento
Cres = 0.25  # coef. arrasto do ar
A = 2.0  # área frontal (m2)
rho_ar = 1.225  # densidade do ar (kg/m3)

# Configuração da simulação
dt = 0.1  # passo de tempo (s)
t_max = 600  # tempo máximo (s)
n_steps = int(t_max/dt)
t = np.linspace(0, t_max, n_steps)

# Arrays para armazenar resultados
v = np.zeros(n_steps)
dist = np.zeros(n_steps)
v[0] = v0

for i in range(n_steps - 1):
    F_rol = mu * m * g * np.cos(theta)
    F_ar = 0.5 * Cres * rho_ar * A * v[i]**2
    F_rampa = m * g * np.sin(theta)
    if v[i] < 0.1:  # evitar divisão por zero
        v[i] = 0.1
    dvdt = (P/v[i] - F_rol - F_ar - F_rampa) / m
    v[i+1] = v[i] + dvdt * dt
    dist[i+1] = dist[i] + v[i] * dt
    if dist[i+1] >= 2000:
        break

# Truncar arrays até ao ponto de 2000 m
t = t[:i+2]
dist = dist[:i+2]
v = v[:i+2]

# Tempo para percorrer 2 km
t_2km = t[-1]
print(f"b) Tempo para percorrer 2 km na subida: {t_2km:.1f}s")

# Gráficos

#distancia km
plt.figure(figsize=(12, 5))


plt.plot(t, dist/1000, label='Distância (km)')
plt.axhline(2, color='g', linestyle='--', label='2 km')
plt.xlabel('Tempo (s)')
plt.ylabel('Distância (km)')
plt.title('Distância Percorrida')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

#Velocidade km/h

plt.plot(t, v, label='Velocidade (m/s)')
plt.axhline(v[-1], color='r', linestyle='--', label='Velocidade terminal')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.title('Evolução da Velocidade')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

#Trabalho (kJ)

plt.plot(t, P*t/1000, label='Trabalho (kJ)')
plt.xlabel('Tempo (s)')
plt.ylabel('Trabalho (kJ)')
plt.title('Trabalho Realizado')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

#Trabalho realizado no total

trabalho_total = P * t_2km / 1000
print(f"Trabalho total realizado: {trabalho_total:.2f} kJ")

# --- Fase 2: descida com travagem regenerativa ---

P_descida = -10000  # Potência regenerativa (W)
v0_descida = 20.0   # Velocidade inicial (m/s)

v_desc = np.zeros(n_steps)
dist_desc = np.zeros(n_steps)
v_desc[0] = v0_descida

for i in range(n_steps - 1):
    F_rol = mu * m * g * np.cos(theta)
    F_ar = 0.5 * Cres * rho_ar * A * v_desc[i]**2
    F_rampa = m * g * np.sin(theta)
    if v_desc[i] < 0.1:
        v_desc[i] = 0.1
    dvdt = (P_descida/v_desc[i] - F_rol - F_ar + F_rampa) / m  # +F_rampa pois agora é a favor do movimento
    v_desc[i+1] = v_desc[i] + dvdt * dt
    dist_desc[i+1] = dist_desc[i] + v_desc[i] * dt
    if dist_desc[i+1] >= 2000:
        break

# Truncar arrays até ao ponto de 2000 m
t_desc = t[:i+2]
dist_desc = dist_desc[:i+2]
v_desc = v_desc[:i+2]

# Tempo para percorrer 2 km na descida
t2km_desc = t_desc[-1]
print(f"\nDescida: Tempo para percorrer 2 km: {t2km_desc:.1f}s")

# Trabalho realizado pelo motor (negativo = energia recuperada)
trabalho_descida = P_descida * t2km_desc / 1000  # em kJ
print(f"Trabalho realizado pelo motor na descida: {trabalho_descida:.2f} kJ")

# Gráficos
plt.figure(figsize=(12, 5))
plt.plot(t_desc, dist_desc/1000, label='Distância (km) descida')
plt.axhline(2, color='g', linestyle='--', label='2 km')
plt.xlabel('Tempo (s)')
plt.ylabel('Distância (km)')
plt.title('Distância Percorrida na Descida')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

plt.plot(t_desc, v_desc, label='Velocidade (m/s) descida')
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.title('Evolução da Velocidade na Descida')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

#e)

# Energia consumida na subida (em kJ, já calculada)
energia_gasta_subida = trabalho_total  # positivo

# Energia recuperada na descida (em kJ, metade do trabalho negativo)
energia_recuperada_descida = -0.5 * trabalho_descida  # negativo, então fica positivo

# Diferença de energia na bateria (final - inicial)
delta_energia_bateria = -energia_gasta_subida + energia_recuperada_descida

print(f"\nDiferença de energia na bateria após subida e descida: {delta_energia_bateria:.2f} kJ")