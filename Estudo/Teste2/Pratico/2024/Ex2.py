import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do sistema conforme enunciado
k = 2  # J/m^4
m = 0.5  # kg

# Função de energia potencial conforme enunciado: Ep = k(x-0.5)^2(x+0.5)^2
def potential_energy(x):
    return k * (x - 0.5)**2 * (x + 0.5)**2

# Força conforme enunciado: Fx = -4kx^3 + kx
def Fx(x):
    return -4*k*x**3 + k*x

# a) Diagrama de energia potencial
x = np.linspace(-1, 1, 500)
Ep = potential_energy(x)

plt.figure(figsize=(8, 6))
plt.plot(x, Ep, 'b-', linewidth=2, label='Energia Potencial')
plt.axhline(0.25, color='r', linestyle='--', label='E = 0.25 J')
plt.axhline(0.125, color='g', linestyle='--', label='E = 0.125 J')
plt.title('Diagrama de Energia Potencial do Oscilador Quártico', fontsize=14)
plt.xlabel('Posição x (m)', fontsize=12)
plt.ylabel('Energia Potencial $E_p$ (J)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()

# RESPOSTA a)
print("RESPOSTA a):")
print("Para E < 0.125 J: oscila em um dos poços (x ≈ ±0.5 m)")
print("Para 0.125 J < E < 0.25 J: oscila entre os dois poços, mais lento no centro")
print("Para E > 0.25 J: movimento não limitado")

# b) Cálculo numérico do movimento com x0 = 1 m, v0 = 0 m/s
x0 = 1.0  # m (conforme enunciado)
v0 = 0.0  # m/s (conforme enunciado)
t0 = 0    # s
tf = 4   # s (aumentado para melhor visualização)
dt = 0.001  # reduzido para maior precisão

t = np.arange(t0, tf, dt)
x_num = np.zeros_like(t)
v_num = np.zeros_like(t)

x_num[0] = x0
v_num[0] = v0

# Usando método de Verlet para melhor conservação de energia
for i in range(1, len(t)):
    a = Fx(x_num[i-1]) / m
    x_num[i] = x_num[i-1] + v_num[i-1]*dt + 0.5*a*dt**2
    a_new = Fx(x_num[i]) / m
    v_num[i] = v_num[i-1] + 0.5*(a + a_new)*dt


# Gráficos de posição e velocidade
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(t, x_num, 'b-', label='x(t)')
plt.axhline(0.5, color='g', linestyle='--', label='x_eq = ±0.5 m')
plt.axhline(-0.5, color='g', linestyle='--')
plt.xlabel('Tempo (s)', fontsize=12)
plt.ylabel('Posição x (m)', fontsize=12)
plt.title('Posição vs Tempo', fontsize=12)
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(t, v_num, 'r-', label='v(t)')
plt.xlabel('Tempo (s)', fontsize=12)
plt.ylabel('Velocidade v (m/s)', fontsize=12)
plt.title('Velocidade vs Tempo', fontsize=12)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# c) Gráfico das energias
E_kin = 0.5 * m * v_num**2
E_pot = potential_energy(x_num)
E_total = E_kin + E_pot

plt.figure(figsize=(10, 6))
plt.plot(t, E_total, 'k-', label='Energia Total')
plt.plot(t, E_kin, 'r-', label='Energia Cinética')
plt.plot(t, E_pot, 'b-', label='Energia Potencial')
plt.title('Energias do Oscilador Quártico', fontsize=14)
plt.xlabel('Tempo (s)', fontsize=12)
plt.ylabel('Energia (J)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True)
plt.show()

# Verificação da energia inicial
E0 = potential_energy(x0)
print(f"\nEnergia inicial: {E0:.4f} J")
print(f"Variação máxima de energia total: {np.max(E_total)-np.min(E_total):.2e} J")

#Etotal = 1.125 J 
#Ep em 0.5m

Ep05 = k*(0.5 - 0.5)**2 * (0.5 + 0.5)**2 # = 0
#Ekin = 1.125 J

#1.125 = 0.5 * m * v^2
v = np.sqrt(2*1.125/0.5)

print(f"Velocidade em x = 0.5 m: +/-{v:.4f} m/s")


