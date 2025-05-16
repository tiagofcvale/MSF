import numpy as np
import matplotlib.pyplot as plt

# Dados iniciais
t0 = 0.0
tf = 3  # tempo máximo de simulação
dt = 0.0001
r0 = np.array([0.0, 0.0, 0.0])  # (x, y, z)
v0_mod = 100 * 1000 / 3600  # 100 km/h em m/s (≈27.78 m/s)
angulo = 16  # graus
v0 = np.array([
    v0_mod * np.cos(np.radians(angulo)),  # vx (horizontal - direção da baliza)
    0.0,                                  # vy (lateral)
    v0_mod * np.sin(np.radians(angulo))   # vz (vertical)
])
w = np.array([0.0, 0.0, -10.0])  # rotação em torno de z (backspin)
g = 9.8
r_bola = 0.11  # raio da bola
A = np.pi * r_bola**2  # área da seção transversal
m = 0.45  # massa da bola
dAr = 1.225  # densidade do ar
D = 0.0127  # coeficiente de arrasto (m^-1)

t = np.arange(t0, tf, dt)
a = np.zeros([3, np.size(t)])
v = np.zeros([3, np.size(t)])
v[:, 0] = v0
r = np.zeros([3, np.size(t)])
r[:, 0] = r0

x_baliza = 20  # posição x da baliza (20 m do ponto de chute)
y_baliza = None
z_baliza = None

for i in range(np.size(t) - 1):
    v_norm = np.linalg.norm(v[:, i])
    
    # Força de resistência do ar (F_res = -m*D*|v|*v)
    F_res = -m * D * v_norm * v[:, i]
    
    # Força de Magnus (F_magnus = 0.5 * A * dAr * r_bola * (w × v))
    F_magnus = 0.5 * A * dAr * r_bola * np.cross(w, v[:, i])
    
    # Força peso (F_g = [0, 0, -m*g])
    F_g = np.array([0, 0, -m * g])
    
    # Soma das forças
    F_total = F_res + F_magnus + F_g
    a[:, i] = F_total / m
    
    # Integração numérica (Euler)
    v[:, i + 1] = v[:, i] + a[:, i] * dt
    r[:, i + 1] = r[:, i] + v[:, i] * dt

    # Verifica se passou pela baliza (x=20m)
    if r[0, i] < x_baliza <= r[0, i + 1]:
        frac = (x_baliza - r[0, i]) / (r[0, i + 1] - r[0, i])
        y_baliza = r[1, i] + frac * (r[1, i + 1] - r[1, i])
        z_baliza = r[2, i] + frac * (r[2, i + 1] - r[2, i])
    
    # Critério de parada quando a bola atinge o chão (z=0)
    if r[2, i + 1] <= 0:
        break

# Truncar arrays até ao impacto
t = t[:i + 2]
r = r[:, :i + 2]
v = v[:, :i + 2]
a = a[:, :i + 2]

# Gráficos
plt.figure(figsize=(12, 5))

# Vista lateral (X-Z)
plt.subplot(1, 2, 1)
plt.plot(r[0, :], r[2, :], 'b-', label='Trajetória')
plt.axvline(x=x_baliza, color='r', linestyle='--', label='Baliza (20m)')
plt.axhline(2.44, color='g', linestyle=':', label='Altura do travessão')
plt.xlabel('Distância (m)')
plt.ylabel('Altura (m)')
plt.title('Vista lateral (X-Z)')
plt.legend()
plt.grid(True)

# Vista superior (X-Y)
plt.subplot(1, 2, 2)
plt.plot(r[0, :], r[1, :], 'b-', label='Trajetória')
plt.axvline(x=x_baliza, color='r', linestyle='--', label='Baliza (20m)')
plt.axhline(3.75, color='g', linestyle=':', label='Limite lateral')
plt.axhline(-3.75, color='g', linestyle=':')
plt.xlabel('Distância (m)')
plt.ylabel('Desvio lateral (m)')
plt.title('Vista superior (X-Y)')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Resultados
if y_baliza is not None and z_baliza is not None:
    print(f"Posição ao passar a baliza (x=20m):")
    print(f"Desvio lateral (y): {y_baliza:.3f} m")
    print(f"Altura (z): {z_baliza:.3f} m")
    
    # Verificação de golo (-3.75m < y < 3.75m e 0 < z < 2.44m)
    if -3.75 < y_baliza < 3.75 and 0 < z_baliza < 2.44:
        print("Resultado: É golo!")
    else:
        print("Resultado: Não é golo!")
else:
    print("A bola não chegou à baliza.")
    print(f"Distância máxima alcançada: {r[0, -1]:.2f} m")