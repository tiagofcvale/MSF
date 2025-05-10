import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parâmetros da simulação
dt = 0.001
tf = 5.0
t = np.arange(0, tf, dt)
Nt = len(t)

# Parâmetros físicos
N = 5          # número de esferas
d = 0.1        # diâmetro das esferas (m)
l = 1.0        # comprimento da corda (m) [10*d]
m = 0.3        # massa (kg)
k = 1e7        # constante de rigidez (N/m²)
g = 9.8        # aceleração gravítica (m/s²)

# Inicialização dos arrays
x_arr = np.zeros((N, Nt))
v_arr = np.zeros((N, Nt))
a_arr = np.zeros((N, Nt))

# Condições iniciais
x_arr[:, 0] = np.arange(N) * d  # posições de equilíbrio
x_arr[0, 0] = -0.5              # primeira esfera deslocada (-5d)
x_arr[-1, 0] = 0.5              # última esfera deslocada (5d)

def acc_contact(dx, d):
    """Força de contato entre esferas"""
    if dx < d:
        return (-k * (dx - d)**2) / m
    return 0.0

def acceleration(i, x):
    """Aceleração total da esfera i"""
    a = 0.0
    
    # Forças de contato com vizinhos
    if i > 0:
        a -= acc_contact(x[i] - x[i-1], d)
    if i < N-1:
        a += acc_contact(x[i+1] - x[i], d)
    
    # Força gravítica (pêndulo)
    a -= g * (x[i] - i*d) / l
    
    return a

# Simulação com Euler-Cromer
for n in range(Nt-1):
    # Calcular acelerações
    for i in range(N):
        a_arr[i, n] = acceleration(i, x_arr[:, n])
    
    # Atualizar velocidades
    v_arr[:, n+1] = v_arr[:, n] + a_arr[:, n] * dt
    
    # Atualizar posições
    x_arr[:, n+1] = x_arr[:, n] + v_arr[:, n+1] * dt

# Configuração da animação
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(-1, N)
ax.set_ylim(-0.6, 0.6)
ax.set_xlabel('Índice da Esfera')
ax.set_ylabel('Deslocamento (m)')
ax.set_title('Simulação de 5 Esferas Acopladas')
ax.grid(True)

# Criar os objetos gráficos
balls = [ax.plot([i], [0], 'o', markersize=20, label=f'Esfera {i+1}')[0] for i in range(N)]
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

def init():
    """Inicialização da animação"""
    for ball in balls:
        ball.set_data([], [])
    time_text.set_text('')
    return balls + [time_text]

def update(frame):
    """Atualização do frame"""
    for i, ball in enumerate(balls):
        ball.set_data([i], [x_arr[i, frame]])  # Note os colchetes extras para criar sequências
    time_text.set_text(f'Tempo: {t[frame]:.2f}s')
    return balls + [time_text]

# Criar a animação (com menos frames para melhor performance)
ani = FuncAnimation(fig, update, frames=range(0, Nt, 20),
                    init_func=init, blit=True, interval=50)
#salvar a animação como gif
ani.save('pendulum.gif', writer='imagemagick', fps=30)


plt.legend()
plt.tight_layout()
plt.show()
