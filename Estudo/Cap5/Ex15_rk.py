import numpy as np
import matplotlib.pyplot as plt

def maxminv(xm1, xm2, xm3, ym1, ym2, ym3):
    """Encontra extremos usando interpolação quadrática"""
    xab = xm1 - xm2
    xac = xm1 - xm3
    xbc = xm2 - xm3
    
    a = ym1/(xab*xac)
    b = -ym2/(xab*xbc)
    c = ym3/(xac*xbc)
    
    xmla = (b+c)*xm1 + (a+c)*xm2 + (a+b)*xm3
    xm = 0.5*xmla/(a+b+c)
    
    y_extreme = a*(xm-xm2)*(xm-xm3) + b*(xm-xm1)*(xm-xm3) + c*(xm-xm1)*(xm-xm2)
    return xm, y_extreme

def rk4(t, vx, acelera, dt):
    """Integração numérica de equação diferencial de 2ª ordem"""
    ax1 = acelera(t, vx)
    c1v = ax1*dt
    ax2 = acelera(t+dt/2., vx+c1v/2.)
    c2v = ax2*dt
    ax3 = acelera(t+dt/2., vx+c2v/2.)
    c3v = ax3*dt
    ax4 = acelera(t+dt, vx+c3v)
    c4v = ax4*dt
          
    return vx + (c1v + 2.*c2v + 2.*c3v + c4v)/6.

# Parâmetros do pêndulo
g = 9.8
L = 1.0
theta0 = np.radians(5.0)  # 5 graus em radianos
omega0 = 0.0

# Parâmetros da simulação
dt = 0.001
t_max = 10
n_steps = int(t_max/dt)

# Arrays para resultados
t = np.zeros(n_steps)
theta = np.zeros(n_steps)
omega = np.zeros(n_steps)

# Condições iniciais
t[0] = 0
theta[0] = theta0
omega[0] = omega0

# Função de aceleração para o pêndulo
def aceleracao_pendulo(t, omega_val):
    return -(g/L)*np.sin(theta[i-1])  # Usa theta do passo anterior

# Simulação com RK4
for i in range(1, n_steps):
    t[i] = t[i-1] + dt
    omega[i] = rk4(t[i-1], omega[i-1], aceleracao_pendulo, dt)
    theta[i] = theta[i-1] + omega[i]*dt  # Integração da velocidade

# Detecção de máximos
max_indices = []
for i in range(1, n_steps-1):
    if omega[i-1] > 0 and omega[i+1] < 0:  # Passagem por zero descendente
        max_indices.append(i)

# Refinamento dos máximos
max_times = []
max_angles = []
for i in max_indices:
    if 0 < i < n_steps-1:
        t_max, theta_max = maxminv(t[i-1], t[i], t[i+1], theta[i-1], theta[i], theta[i+1])
        max_times.append(t_max)
        max_angles.append(theta_max)

# Cálculo do período
if len(max_times) > 1:
    T = np.mean(np.diff(max_times))
    print(f"Período para θ₀=5°: {T:.4f} s (Precisão: ±{np.std(np.diff(max_times)):.4f} s)")
else:
    print("Não foram detectados períodos completos")

# Gráfico
plt.figure(figsize=(12,6))
plt.plot(t, theta, label='Ângulo (rad)')
plt.scatter(max_times, max_angles, color='red', label='Máximos detectados')
plt.xlabel('Tempo (s)')
plt.ylabel('θ (rad)')
plt.title('Pêndulo Não-Linear (RK4 + maxminv)')
plt.legend()
plt.grid()
plt.show()