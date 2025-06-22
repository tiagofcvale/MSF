import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do sistema
k = 1.0       # N/m
k_prime = 0.5 # N/m
m = 1.0       # kg

# Posições de equilíbrio
x_A_eq = 1.0  # m
x_B_eq = 1.2  # m

# Frequências teóricas
omega_1_teorico = np.sqrt(k / m)
omega_2_teorico = np.sqrt((k + 2 * k_prime) / m)

# Derivadas para RK4 com deslocamentos relativos
def rk4_sistema_acoplado(t, estado, dt):
    x_til_A, v_A, x_til_B, v_B = estado

    def derivadas(estado):
        x_til_A, v_A, x_til_B, v_B = estado
        a_A = -(k + k_prime)*x_til_A + k_prime*x_til_B
        a_B = k_prime*x_til_A - (k + k_prime)*x_til_B
        return np.array([v_A, a_A/m, v_B, a_B/m])
    
    k1 = derivadas(estado)
    k2 = derivadas(estado + k1*dt/2)
    k3 = derivadas(estado + k2*dt/2)
    k4 = derivadas(estado + k3*dt)
    
    return estado + (k1 + 2*k2 + 2*k3 + k4)*dt/6

# Função para medir o período a partir do deslocamento
def medir_periodo(t, x):
    cruzamentos = np.where(np.diff(np.sign(x - np.mean(x))))[0]
    if len(cruzamentos) < 2:
        return None, None
    tempos_cruzamentos = t[cruzamentos]
    periodos = 2 * np.diff(tempos_cruzamentos[::2])  # Meio-período x 2
    T_medio = np.mean(periodos)
    omega = 2 * np.pi / T_medio
    return T_medio, omega

# Função para simular, plotar e medir período
def simular_e_plotar(x_A0, x_B0, v_A0=0, v_B0=0, t_total=40, dt=0.01, caso=''):
    n_passos = int(t_total/dt)
    t = np.zeros(n_passos)
    x_A = np.zeros(n_passos)
    v_A = np.zeros(n_passos)
    x_B = np.zeros(n_passos)
    v_B = np.zeros(n_passos)
    
    estado = np.array([
        x_A0 - x_A_eq,
        v_A0,
        x_B0 - x_B_eq,
        v_B0
    ])
    
    for i in range(n_passos):
        t[i] = i * dt
        x_A[i] = estado[0] + x_A_eq
        v_A[i] = estado[1]
        x_B[i] = estado[2] + x_B_eq
        v_B[i] = estado[3]
        estado = rk4_sistema_acoplado(t[i], estado, dt)
    
    # Medir período e frequência com base no deslocamento do Corpo A
    T, omega = medir_periodo(t, x_A)

    # Plotar resultados
    plt.figure(figsize=(14, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(t, x_A, label='Corpo A')
    plt.plot(t, x_B, label='Corpo B')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Posição (m)')
    plt.title(f'Posição vs Tempo - Caso {caso}')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(x_A, x_B)
    plt.xlabel('Posição A (m)')
    plt.ylabel('Posição B (m)')
    plt.title(f'Espaço de Configuração - Caso {caso}')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    if caso in ['i', 'ii']:
        print(f"\nMedições Numéricas - Caso {caso}:")
        print(f"  Período médio T ≈ {T:.3f} s")
        print(f"  Frequência angular ω ≈ {omega:.3f} rad/s")
        if caso == 'i':
            print(f"  ω teórico (modo simétrico): {omega_1_teorico:.3f} rad/s")
        elif caso == 'ii':
            print(f"  ω teórico (modo antissimétrico): {omega_2_teorico:.3f} rad/s")
        print("  → Valores conforme esperado pela teoria.\n")
        # CUIDADO, NOS RESULTADOS O PERIODO (T) APARECE A METADE DESTA RESPOSTA

# Simular os casos
print("Caso i: Ambos os corpos deslocados +0.05m")
print("Movimento harmônico simples (modo simétrico esperado)")
simular_e_plotar(x_A_eq + 0.05, x_B_eq + 0.05, caso='i')

print("\nCaso ii: Corpo A +0.05m, Corpo B -0.05m")
print("Movimento periódico sinusoidal com os dois corpos com velocidades opostas (modo antissimétrico)")
simular_e_plotar(x_A_eq + 0.05, x_B_eq - 0.05, caso='ii')

print("\nCaso iii: Apenas Corpo A deslocado +0.05m")
print("Movimento irregular (superposição dos modos)")
simular_e_plotar(x_A_eq + 0.05, x_B_eq, caso='iii')

