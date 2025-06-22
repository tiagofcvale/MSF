import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do sistema
k = 1.0       # N/m
k_prime = 0.5 # N/m
m = 1.0       # kg
b = 0.05      # kg/s
F0 = 0.005    # N
omega_d = 1.0 # rad/s

# Posições de equilíbrio
x_A_eq = 1.0  # m
x_B_eq = 1.2  # m

# Derivadas com amortecimento e forçamento externo
def rk4_sistema_amortecido_forcado(t, estado, dt):
    x_til_A, v_A, x_til_B, v_B = estado

    def derivadas(t, estado):
        x_til_A, v_A, x_til_B, v_B = estado
        a_A = (
            - (k + k_prime) * x_til_A
            + k_prime * x_til_B
            - b * v_A
            + F0 * np.cos(omega_d * t)
        ) / m
        a_B = (
            - (k + k_prime) * x_til_B
            + k_prime * x_til_A
            - b * v_B
        ) / m
        return np.array([v_A, a_A, v_B, a_B])

    k1 = derivadas(t, estado)
    k2 = derivadas(t + dt/2, estado + k1 * dt/2)
    k3 = derivadas(t + dt/2, estado + k2 * dt/2)
    k4 = derivadas(t + dt,   estado + k3 * dt)

    return estado + (k1 + 2*k2 + 2*k3 + k4) * dt / 6

# Simulação
def simular_sistema(t_total=140, dt=0.01):
    n_passos = int(t_total/dt)
    t = np.zeros(n_passos)
    x_A = np.zeros(n_passos)
    x_B = np.zeros(n_passos)
    
    estado = np.array([
        0.05,  # x̃_A(0) = 1.05 - 1.0
        0.0,   # v_A(0)
        0.05,  # x̃_B(0) = 1.25 - 1.2
        0.0    # v_B(0)
    ])
    
    for i in range(n_passos):
        t[i] = i * dt
        x_A[i] = estado[0] + x_A_eq
        x_B[i] = estado[2] + x_B_eq
        estado = rk4_sistema_amortecido_forcado(t[i], estado, dt)

    # Plot
    plt.figure(figsize=(12, 5))
    plt.plot(t, x_A, label='Corpo A')
    plt.plot(t, x_B, label='Corpo B')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Posição (m)')
    plt.title('Sistema com Amortecimento e Forçamento Externo')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Executar simulação
simular_sistema()

#b)

# Derivadas com amortecimento e forçamento externo variável (omega_d)
def rk4_sistema_amortecido_forcado(t, estado, dt, omega_d):
    def derivadas(t, estado):
        x_til_A, v_A, x_til_B, v_B = estado
        a_A = (
            - (k + k_prime) * x_til_A
            + k_prime * x_til_B
            - b * v_A
            + F0 * np.cos(omega_d * t)
        ) / m
        a_B = (
            - (k + k_prime) * x_til_B
            + k_prime * x_til_A
            - b * v_B
        ) / m
        return np.array([v_A, a_A, v_B, a_B])

    k1 = derivadas(t, estado)
    k2 = derivadas(t + dt/2, estado + k1 * dt/2)
    k3 = derivadas(t + dt/2, estado + k2 * dt/2)
    k4 = derivadas(t + dt,   estado + k3 * dt)

    return estado + (k1 + 2*k2 + 2*k3 + k4) * dt / 6

# Simulação para um dado omega_d, retorna amplitude após transiente
def medir_amplitudes(omega_d, t_total=100, dt=0.01):
    n_passos = int(t_total / dt)
    estado = np.array([0.05, 0.0, 0.05, 0.0])  # condições iniciais
    x_A = np.zeros(n_passos)
    x_B = np.zeros(n_passos)

    for i in range(n_passos):
        x_A[i] = estado[0] + x_A_eq
        x_B[i] = estado[2] + x_B_eq
        estado = rk4_sistema_amortecido_forcado(i*dt, estado, dt, omega_d)

    # Amplitude medida apenas na parte final do sinal (estado estacionário)
    amostra_final = slice(int(n_passos*0.75), n_passos)
    amp_A = (np.max(x_A[amostra_final]) - np.min(x_A[amostra_final])) / 2
    amp_B = (np.max(x_B[amostra_final]) - np.min(x_B[amostra_final])) / 2
    return amp_A, amp_B

# Varredura de omega_d
omegas = np.linspace(0.1, 2.5, 50)
amplitudes_A = []
amplitudes_B = []

for omega in omegas:
    amp_A, amp_B = medir_amplitudes(omega)
    amplitudes_A.append(amp_A)
    amplitudes_B.append(amp_B)

# Plotando gráfico de amplitudes
plt.figure(figsize=(10, 6))
plt.plot(omegas, amplitudes_A, label='Amplitude Corpo A')
plt.plot(omegas, amplitudes_B, label='Amplitude Corpo B')
plt.xlabel('Frequência de Forçamento ω_d (rad/s)')
plt.ylabel('Amplitude (m)')
plt.title('Amplitude no Regime Estacionário vs Frequência de Forçamento')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
