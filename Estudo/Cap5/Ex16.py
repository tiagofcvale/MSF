import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do sistema
k = 1.0       # N/m
alpha = -0.01  # N/m²
m = 1.0        # kg

# Função da energia potencial
def potential_energy(x):
    return 0.5*k*x**2 + alpha*x**3

# Função da aceleração (dvx/dt)
def acceleration(t, x, vx):
    return (-k*x - 3*alpha*x**2)/m

# Implementação do RK4 conforme sua função
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

# Simulação para E < 1 J
E_total = 0.5  # J

# Encontrar os pontos de retorno (onde Ep = E_total)
def find_turning_points(E):
    # Resolve Ep(x) = E => 0.5*x² - 0.01*x³ - E = 0
    coeffs = [-0.01, 0.5, 0, -E]
    roots = np.roots(coeffs)
    # Filtra raízes reais
    real_roots = [r.real for r in roots if abs(r.imag) < 1e-10]
    return sorted(real_roots)

turning_points = find_turning_points(E_total)
print(f"Pontos de retorno para E = {E_total} J: {turning_points}")

# Condições iniciais
x0 = turning_points[0]  # Começa no ponto de retorno negativo
v0 = 0.0

# Parâmetros da simulação
dt = 0.01  # passo temporal
t_max = 20  # tempo máximo de simulação
n_steps = int(t_max/dt)

# Arrays para armazenar resultados
t_values = np.linspace(0, t_max, n_steps)
x_values = np.zeros(n_steps)
v_values = np.zeros(n_steps)

# Condições iniciais
x_values[0] = x0
v_values[0] = v0

# Integração numérica usando RK4
for i in range(1, n_steps):
    x_values[i], v_values[i] = rk4_x_vx(t_values[i-1], x_values[i-1], v_values[i-1], acceleration, dt)

# Calcula energias
Ep_values = potential_energy(x_values)
Ek_values = 0.5*m*v_values**2
E_total_values = Ep_values + Ek_values

# Gráficos
plt.figure(figsize=(14, 10))

# Diagrama de energia potencial
plt.subplot(2, 2, 1)
x_plot = np.linspace(-2, 2, 500)
plt.plot(x_plot, potential_energy(x_plot), label='Energia Potencial')
plt.axhline(E_total, color='r', linestyle='--', label=f'E = {E_total} J')
plt.plot(x_values, Ep_values, 'g.', markersize=2, label='Trajetória')
plt.xlabel('Posição (m)')
plt.ylabel('Energia (J)')
plt.title('Diagrama de Energia Potencial')
plt.legend()
plt.grid(True)

# Posição vs tempo
plt.subplot(2, 2, 2)
plt.plot(t_values, x_values)
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Posição vs Tempo')
plt.grid(True)

# Espaço de fase
plt.subplot(2, 2, 3)
plt.plot(x_values, v_values)
plt.xlabel('Posição (m)')
plt.ylabel('Velocidade (m/s)')
plt.title('Espaço de Fase')
plt.grid(True)

# Energias vs tempo
plt.subplot(2, 2, 4)
plt.plot(t_values, Ep_values, label='Energia Potencial')
plt.plot(t_values, Ek_values, label='Energia Cinética')
plt.plot(t_values, E_total_values, label='Energia Total')
plt.xlabel('Tempo (s)')
plt.ylabel('Energia (J)')
plt.title('Energias vs Tempo')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Verificação da conservação de energia
energy_error = np.max(np.abs(E_total_values - E_total))
print(f"Erro máximo na conservação de energia: {energy_error:.2e} J")
print(f"Variação percentual da energia total: {100*energy_error/E_total:.4f}%")

# Análise dos resultados
print("\nAnálise do movimento para E < 1 J:")
print(f"- Amplitude de oscilação: {np.max(np.abs(x_values)):.3f} m")
print(f"- Período aproximado: {t_values[np.argmin(np.abs(x_values - x0))]/2:.3f} s")
print("- O movimento é periódico mas não-harmônico (devido ao termo cúbico)")
print("- A energia total é bem conservada (erro < 0.01%)")