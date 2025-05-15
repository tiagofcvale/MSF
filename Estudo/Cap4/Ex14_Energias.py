import numpy as np
import matplotlib.pyplot as plt

k = 1 # N/m
m = 1 # kg
x0 = 4 # m
v0 = 0 # m/s
dt = 0.01 # s
tf = 5 # s

E_total = 0.5 * k * x0**2 + 0.5 * m * v0**2
print(f"Energia total: {E_total:.2f} J")

# vetores de tempo
t = np.arange(0, tf, dt)
N = len(t)

# Inicialização para o método de Euler-Cromer

x_euler = np.zeros(N)
v_euler = np.zeros(N)
a_euler = np.zeros(N)

x_euler[0] = x0
v_euler[0] = v0

x_euler_cromer = np.zeros(N)
v_euler_cromer = np.zeros(N)
a_euler_cromer = np.zeros(N)

x_euler_cromer[0] = x0
v_euler_cromer[0] = v0

#integração numérica

for i in range(N-1):
    # Metodo de Euler
    a_euler[i] = -k * x_euler[i] / m
    v_euler[i+1] = v_euler[i] + a_euler[i] * dt
    x_euler[i+1] = x_euler[i] + v_euler[i] * dt

    # Metodo de Euler-Cromer
    a_euler_cromer[i] = -k * x_euler_cromer[i] / m
    v_euler_cromer[i+1] = v_euler_cromer[i] + a_euler_cromer[i] * dt
    x_euler_cromer[i+1] = x_euler_cromer[i] + v_euler_cromer[i+1] * dt

# Energia total ao longo do tempo
E_pot_euler = 0.5 * k * x_euler**2
E_kin_euler = 0.5 * m * v_euler**2
E_total_euler = E_pot_euler + E_kin_euler


E_pot_euler_cromer = 0.5 * k * x_euler_cromer**2
E_kin_euler_cromer = 0.5 * m * v_euler_cromer**2
E_total_euler_cromer = E_pot_euler_cromer + E_kin_euler_cromer

# Gráficos
plt.figure(figsize=(12, 6))

# Subplot 1: Energia total (Euler)
plt.subplot(1, 2, 1)
plt.plot(t, E_total_euler, label="Euler", color="blue")
plt.title("Energia Total - Método de Euler")
plt.xlabel("Tempo (s)")
plt.ylabel("Energia (J)")
plt.legend()
plt.grid()

# Subplot 2: Energia total (Euler-Cromer)
plt.subplot(1, 2, 2)
plt.plot(t, E_total_euler_cromer, label="Euler-Cromer", color="green")
plt.title("Energia Total - Método de Euler-Cromer")
plt.xlabel("Tempo (s)")
plt.ylabel("Energia (J)")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()