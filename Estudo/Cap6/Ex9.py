import numpy as np
import matplotlib.pyplot as plt

# Dados do problema
m = 1.0
k = 1.0
k_prime = 0.5

# Matriz de rigidez (K)
K = np.array([
    [k + k_prime, -k_prime, 0],
    [-k_prime, 2*k_prime, -k_prime],
    [0, -k_prime, k + k_prime]
])

# Matriz massa M (identidade vezes m)
M = m * np.eye(3)

# Resolver autovalores e autovetores do problema generalizado
# K u = lambda M u  => Frequências ao quadrado = lambda
eigvals, eigvecs = np.linalg.eig(np.linalg.inv(M).dot(K))

# Frequências angulares (raiz dos autovalores)
omega = np.sqrt(eigvals)

# Ordenar frequências e modos em ordem crescente
idx = np.argsort(omega)
omega_sorted = omega[idx]
modes_sorted = eigvecs[:, idx]

# Normalizar modos (amplitude 1)
for i in range(3):
    modes_sorted[:, i] /= np.linalg.norm(modes_sorted[:, i])

print("Frequências angulares (rad/s):", omega_sorted)
print("Modos normais (colunas):\n", modes_sorted)

# Parâmetros de integração
dt = 0.01
t_total = 20
n_steps = int(t_total / dt)

# Método Euler-Cromer para sistema acoplado
def euler_cromer(u0, v0, t_total, dt):
    n_steps = int(t_total / dt)
    u = np.zeros((3, n_steps))
    v = np.zeros((3, n_steps))
    t = np.linspace(0, t_total, n_steps)

    u[:, 0] = u0
    v[:, 0] = v0

    for i in range(n_steps - 1):
        # Calcula aceleração
        a = np.zeros(3)
        a[0] = (-(k + k_prime)*u[0, i] + k_prime*u[1, i]) / m
        a[1] = (k_prime*u[0, i] - 2*k_prime*u[1, i] + k_prime*u[2, i]) / m
        a[2] = (k_prime*u[1, i] - (k + k_prime)*u[2, i]) / m

        # Atualiza velocidades (Euler-Cromer)
        v[:, i+1] = v[:, i] + a * dt

        # Atualiza posições
        u[:, i+1] = u[:, i] + v[:, i+1] * dt

    return t, u

# Simular e plotar para cada modo normal
for i in range(3):
    # Condições iniciais: modo normal i, velocidade zero
    u0 = modes_sorted[:, i]
    v0 = np.zeros(3)

    # Tempo para 3 períodos do modo i
    T = 2 * np.pi / omega_sorted[i]
    t, u = euler_cromer(u0, v0, t_total=3*T, dt=dt)

    plt.figure(figsize=(10, 5))
    plt.plot(t, u[0, :], label='Massa A')
    plt.plot(t, u[1, :], label='Massa B')
    plt.plot(t, u[2, :], label='Massa C')
    plt.title(f'Modo Normal {i+1} - ω = {omega_sorted[i]:.4f} rad/s')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Deslocamento (m)')
    plt.legend()
    plt.grid()
    plt.show()

    # Descrição do modo
    print(f"\nDescrição do Modo {i+1}:")
    if i == 0:
        print("Todas as massas oscilam em fase com mesma amplitude.")
    elif i == 1:
        print("Massa A e C oscilam em oposição de fase, Massa B quase estacionária.")
    else:
        print("Massa B oscila em oposição de fase com A e C, que oscilam em fase entre si.")

