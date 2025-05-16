import numpy as np
import matplotlib.pyplot as plt

# Dados iniciais
t0 = 0.0
tf = 5  # tempo máximo de simulação (aumentado para garantir que chegue à baliza)
dt = 0.001
v0_mod = 100 * 1000 / 3600  # 100 km/h em m/s (≈27.78 m/s)
angulo = 16  # graus
v0 = np.array([
    v0_mod * np.cos(np.radians(angulo)),  # vx (horizontal)
    v0_mod * np.sin(np.radians(angulo))   # vy (vertical)
])
r0 = np.array([0.0, 0.0])  # (x, y) - bola chutada do solo
g = 9.8
m = 0.45  # massa corrigida para bola de futebol
dAr = 1.225
D = 0.0127  # coeficiente de arrasto corrigido (m^-1)

t = np.arange(t0, tf, dt)
a = np.zeros([2, np.size(t)])
v = np.zeros([2, np.size(t)])
v[:, 0] = v0
r = np.zeros([2, np.size(t)])
r[:, 0] = r0

x_baliza = 20  # posição da baliza em metros
y_baliza = None

for i in range(np.size(t) - 1):
    v_norm = np.linalg.norm(v[:, i])
    # Força de resistência do ar (F_res = -m*D*|v|*v)
    a[0, i] = -D * v_norm * v[0, i]
    a[1, i] = -g - D * v_norm * v[1, i]
    
    v[:, i + 1] = v[:, i] + a[:, i] * dt
    r[:, i + 1] = r[:, i] + v[:, i] * dt

    # Verifica se passou pela baliza
    if r[0, i] < x_baliza <= r[0, i + 1]:
        frac = (x_baliza - r[0, i]) / (r[0, i + 1] - r[0, i])
        y_baliza = r[1, i] + frac * (r[1, i + 1] - r[1, i])
    
    # Critério de parada quando a bola atinge o chão (y=0)
    if r[1, i + 1] <= 0:
        break

# Truncar arrays até ao impacto
t = t[:i + 2]
r = r[:, :i + 2]
v = v[:, :i + 2]
a = a[:, :i + 2]

# Gráfico XY
plt.figure(figsize=(10, 5))
plt.plot(r[0, :], r[1, :], 'r-', label='Trajetória')
plt.axvline(x_baliza, color='b', linestyle=':', label='Baliza (20m)')
plt.axhline(2.44, color='g', linestyle='--', label='Altura do travessão')
plt.xlabel('Distância (m)')
plt.ylabel('Altura (m)')
plt.title('Trajetória da bola de futebol (ângulo de 16°)')
plt.legend()
plt.grid(True)
plt.show()

if y_baliza is not None:
    print(f"Altura da bola ao passar pela baliza (x={x_baliza} m): {y_baliza:.3f} m")
    
    if 0 < y_baliza < 2.4:
        print("É golo!")
    else:
        print("Não é golo!")
else:
    print(f"A bola não chegou à baliza. Distância máxima: {r[0,-1]:.2f} m")