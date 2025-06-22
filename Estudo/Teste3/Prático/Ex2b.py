import numpy as np
import matplotlib.pyplot as plt

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

# Função de aceleração (inclui força do potencial, amortecimento e força externa)
def acelera(t, x, vx):
    return (-4*alpha*x**3 - b*vx + F0*np.cos(omega_f*t)) / m

# Parâmetros do sistema
m = 1.0       # kg
alpha = 0.15  # N/m^4
b = 0.02      # kg/s
F0 = 7.5      # N
omega_f = 1.0 # rad/s

# Condições iniciais
x0 = 2.0  # m
v0 = 0.0  # m/s

# Parâmetros da simulação
dt = 0.01      # Passo temporal
t_total = 50   # Tempo total de simulação
n_passos = int(t_total/dt)

# Arrays para armazenar resultados
t = np.zeros(n_passos)
x = np.zeros(n_passos)
v = np.zeros(n_passos)


# Vamos simular duas trajetórias com condições iniciais ligeiramente diferentes
x0_1 = 2.000 + 0.001  # m
x0_2 = 2.000 - 0.001  # m
v0_1 = v0_2 = 0.0     # m/s

# Simulação para a primeira condição inicial
x1, v1 = np.zeros(n_passos), np.zeros(n_passos)
x_current, v_current = x0_1, v0_1
for i in range(n_passos):
    x1[i], v1[i] = x_current, v_current
    x_current, v_current = rk4_x_vx(t[i], x_current, v_current, acelera, dt)

# Simulação para a segunda condição inicial
x2, v2 = np.zeros(n_passos), np.zeros(n_passos)
x_current, v_current = x0_2, v0_2
for i in range(n_passos):
    x2[i], v2[i] = x_current, v_current
    x_current, v_current = rk4_x_vx(t[i], x_current, v_current, acelera, dt)

# Calcular a diferença entre as trajetórias
diff = np.abs(x1 - x2)

# Encontrar o tempo onde a diferença ultrapassa um limiar significativo
limiar = 0.1  # 10 cm de diferença
for i in range(n_passos):
    if diff[i] > limiar:
        t_limite = t[i]
        break
else:
    t_limite = t_total

print(f"Tempo de previsão unívoca: {t_limite:.2f} s")

# Gráfico da divergência
plt.figure(figsize=(10, 5))
plt.plot(t, diff)
plt.axhline(y=limiar, color='r', linestyle='--', label=f'Limiar = {limiar} m')
plt.axvline(x=t_limite, color='g', linestyle='--', label=f'Tempo limite = {t_limite:.2f} s')
plt.xlabel('Tempo (s)')
plt.ylabel('Diferença entre trajetórias (m)')
plt.title('Divergência de Trajetórias')
plt.legend()
plt.grid(True)
plt.show()