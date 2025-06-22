import numpy as np
import matplotlib.pyplot as plt

def maxminv(xm1,xm2,xm3,ym1,ym2,ym3):  
    # Máximo ou mínimo usando o polinómio de Lagrange
    # Dados (input): (x0,y0), (x1,y1) e (x2,y2) 
    # Resultados (output): xm, ymax 
    xab=xm1-xm2
    xac=xm1-xm3
    xbc=xm2-xm3

    a=ym1/(xab*xac)
    b=-ym2/(xab*xbc)
    c=ym3/(xac*xbc)

    xmla=(b+c)*xm1+(a+c)*xm2+(a+b)*xm3
    xm=0.5*xmla/(a+b+c)

    xta=xm-xm1
    xtb=xm-xm2
    xtc=xm-xm3

    ymax=a*xtb*xtc+b*xta*xtc+c*xta*xtb
    return xm, ymax

# Parâmetros do sistema
m = 0.25   # kg
k = 1.0    # N/m
b = 0.1    # kg/s
x0 = 0.4   # m
v0 = 0.0   # m/s

# Frequências
gamma = b / (2 * m)
omega0 = np.sqrt(k / m)
omegad = np.sqrt(omega0**2 - gamma**2)

# Solução analítica
def x(t):
    return np.exp(-gamma * t) * (x0 * np.cos(omegad * t) + (gamma * x0 / omegad) * np.sin(omegad * t))

# Gerar dados de tempo e posição
t = np.linspace(0, 20, 1000)  # 1000 pontos para boa resolução
x_vals = x(t)

# Função para encontrar extremos usando interpolação de Lagrange
def find_extrema(t, x):
    extrema = []
    for i in range(1, len(t)-1):
        # Verifica se é um máximo ou mínimo local
        if (x[i] > x[i-1] and x[i] > x[i+1]) or (x[i] < x[i-1] and x[i] < x[i+1]):
            # Usa os 3 pontos para interpolação quadrática
            xm, ym = maxminv(t[i-1], t[i], t[i+1], x[i-1], x[i], x[i+1])
            extrema.append((xm, ym))
    return np.array(extrema)

# Encontrar todos os extremos
extrema = find_extrema(t, x_vals)

# Separar máximos e mínimos
maxima = []
minima = []
for xm, ym in extrema:
    if ym > 0:
        maxima.append((xm, ym))
    else:
        minima.append((xm, ym))

maxima = np.array(maxima)
minima = np.array(minima)

# Plot do movimento com extremos marcados
plt.figure(figsize=(12, 6))
plt.plot(t, x_vals, label='Movimento')
plt.scatter(maxima[:,0], maxima[:,1], c='r', label='Máximos')
plt.scatter(minima[:,0], minima[:,1], c='g', label='Mínimos')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Extremos Locais do Movimento Amortecido')
plt.grid(True)
plt.legend()
plt.show()

# Resultados numéricos
print("Primeiros máximos encontrados:")
for i, (t_max, x_max) in enumerate(maxima[:5]):
    print(f"Max {i+1}: t = {t_max:.3f} s, x = {x_max:.5f} m")

print("\nPrimeiros mínimos encontrados:")
for i, (t_min, x_min) in enumerate(minima[:5]):
    print(f"Min {i+1}: t = {t_min:.3f} s, x = {x_min:.5f} m")

# Verificação teórica do primeiro máximo
T_d = 2*np.pi/omegad  # Período amortecido
t_first_max_theory = 0  # Primeiro máximo ocorre em t=0
x_first_max_theory = x0

print(f"\nVerificação teórica do primeiro máximo:")
print(f"t = {t_first_max_theory} s, x = {x_first_max_theory} m")

#c) 
# Implementação do RK4 fornecida
def rk4(t, vx, acelera, dt):
    ax1 = acelera(t, vx)
    c1v = ax1*dt
    ax2 = acelera(t+dt/2., vx+c1v/2.)
    c2v = ax2*dt
    ax3 = acelera(t+dt/2., vx+c2v/2.)
    c3v = ax3*dt
    ax4 = acelera(t+dt, vx+c3v)
    c4v = ax4*dt
    vxp = vx + (c1v + 2.*c2v + 2.*c3v + c4v)/6.
    return vxp

# Função da aceleração (dv/dt)
def aceleracao(t, vx):
    x = x_sim[-1] if len(x_sim) > 0 else x0  # Pega a última posição calculada
    return (-k*x - b*vx)/m

# Simulação do movimento
dt = 0.01
t_max = 20
n_steps = int(t_max/dt)

t_sim = np.linspace(0, t_max, n_steps)
x_sim = np.zeros(n_steps)
v_sim = np.zeros(n_steps)

# Condições iniciais
x_sim[0] = x0
v_sim[0] = v0

# Integração numérica
for i in range(1, n_steps):
    v_sim[i] = rk4(t_sim[i-1], v_sim[i-1], aceleracao, dt)
    x_sim[i] = x_sim[i-1] + v_sim[i]*dt  # Integração da posição

# Função para encontrar máximos locais
def find_maxima(t, x):
    maxima = []
    for i in range(1, len(t)-1):
        if x[i] > x[i-1] and x[i] > x[i+1]:
            maxima.append((t[i], x[i]))
    return np.array(maxima)

# Encontrar máximos
maxima = find_maxima(t_sim, x_sim)

#c)´

# Implementação RK4 modificada para integrar posição e velocidade
def rk4_step(t, x, vx, acelera, dt):
    # Primeiro estágio
    ax1 = acelera(t, x, vx)
    v1 = vx
    k1x = v1 * dt
    k1v = ax1 * dt
    
    # Segundo estágio
    ax2 = acelera(t + dt/2, x + k1x/2, vx + k1v/2)
    v2 = vx + k1v/2
    k2x = v2 * dt
    k2v = ax2 * dt
    
    # Terceiro estágio
    ax3 = acelera(t + dt/2, x + k2x/2, vx + k2v/2)
    v3 = vx + k2v/2
    k3x = v3 * dt
    k3v = ax3 * dt
    
    # Quarto estágio
    ax4 = acelera(t + dt, x + k3x, vx + k3v)
    v4 = vx + k3v
    k4x = v4 * dt
    k4v = ax4 * dt
    
    # Atualização
    x_new = x + (k1x + 2*k2x + 2*k3x + k4x)/6
    vx_new = vx + (k1v + 2*k2v + 2*k3v + k4v)/6
    
    return x_new, vx_new

# Função da aceleração corrigida
def aceleracao(t, x, vx):
    return (-k*x - b*vx)/m

# Simulação do movimento
dt = 0.001  # Passo temporal menor para maior precisão
t_max = 20
n_steps = int(t_max/dt)

t_sim = np.zeros(n_steps)
x_sim = np.zeros(n_steps)
v_sim = np.zeros(n_steps)

# Condições iniciais
t_sim[0] = 0
x_sim[0] = x0
v_sim[0] = v0

# Integração numérica
for i in range(1, n_steps):
    t_sim[i] = t_sim[i-1] + dt
    x_sim[i], v_sim[i] = rk4_step(t_sim[i-1], x_sim[i-1], v_sim[i-1], aceleracao, dt)

# Função para encontrar máximos locais
def find_maxima(t, x):
    maxima = []
    for i in range(1, len(t)-1):
        if x[i] > x[i-1] and x[i] > x[i+1]:
            maxima.append((t[i], x[i]))
    return np.array(maxima)

# Encontrar máximos
maxima = find_maxima(t_sim, x_sim)

# Implementação do ajuste linear manual
def linear_fit(x, y):
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x*y)
    sum_x2 = np.sum(x**2)
    
    denom = n*sum_x2 - sum_x**2
    a = (n*sum_xy - sum_x*sum_y)/denom
    b = (sum_x2*sum_y - sum_x*sum_xy)/denom
    
    # Cálculo do erro
    y_pred = a*x + b
    residuals = y - y_pred
    std_err = np.sqrt(np.sum(residuals**2)/(n-2))
    a_err = std_err * np.sqrt(n/denom)
    
    return a, b, a_err

# Ajuste linear do log das amplitudes
t_maxima = maxima[:,0]
log_amplitudes = np.log(maxima[:,1])
slope, intercept, slope_err = linear_fit(t_maxima, log_amplitudes)

# Valor teórico
gamma_theory = b/(2*m)

# Gráfico
plt.figure(figsize=(12, 6))
plt.plot(t_maxima, log_amplitudes, 'bo', markersize=4, label='Dados simulados')
plt.plot(t_maxima, slope*t_maxima + intercept, 'r-', 
         label=f'Ajuste: ln(A) = {slope:.5f}±{slope_err:.5f}t + {intercept:.3f}')
plt.axline((0, np.log(x0)), slope=-gamma_theory, color='g', linestyle='--', 
           label=f'Teórico: ln(A) = -{gamma_theory:.1f}t + ln({x0})')
plt.xlabel('Tempo (s)')
plt.ylabel('ln(Amplitude) (ln(m))')
plt.title('Decaimento Exponencial das Amplitudes Máximas')
plt.grid(True)
plt.legend()
plt.show()

# Resultados
print("Resultados do ajuste linear manual:")
print(f"Declive (experimental): {slope:.6f} ± {slope_err:.6f} s⁻¹")
print(f"Declive teórico: -γ = -{gamma_theory} s⁻¹")
print(f"Diferença: {abs(slope + gamma_theory):.2e} s⁻¹")
print(f"Diferença relativa: {abs((slope + gamma_theory)/gamma_theory)*100:.4f}%")