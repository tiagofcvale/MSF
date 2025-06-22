import numpy as np
import matplotlib.pyplot as plt

# Função fornecada para cálculo dos coeficientes de Fourier
def abfourier(tp, xp, it0, it1, nf):
    dt = tp[1] - tp[0]
    per = tp[it1] - tp[it0]
    ome = 2*np.pi/per

    s1 = xp[it0]*np.cos(nf*ome*tp[it0])
    s2 = xp[it1]*np.cos(nf*ome*tp[it1])
    st = xp[it0+1:it1]*np.cos(nf*ome*tp[it0+1:it1])
    soma = np.sum(st)
    
    q1 = xp[it0]*np.sin(nf*ome*tp[it0])
    q2 = xp[it1]*np.sin(nf*ome*tp[it1])
    qt = xp[it0+1:it1]*np.sin(nf*ome*tp[it0+1:it1])
    somq = np.sum(qt)
    
    intega = ((s1+s2)/2 + soma)*dt
    af = 2/per*intega
    integq = ((q1+q2)/2 + somq)*dt
    bf = 2/per*integq
    return af, bf

# Parâmetros do sistema (mesmos do item b)
k = 1.0
alpha = 0.05
m = 1.0

def Ep(x):
    return 0.5*k*x**2 + alpha*x**3

def F(x):
    return -k*x - 3*alpha*x**2

# Implementação do RK4 (igual ao item b)
def rk4(t, estado, acelera, dt):
    ax1 = acelera(t, estado)
    c1v = ax1*dt
    ax2 = acelera(t+dt/2., estado+c1v/2.)
    c2v = ax2*dt
    ax3 = acelera(t+dt/2., estado+c2v/2.)
    c3v = ax3*dt
    ax4 = acelera(t+dt, estado+c3v)
    c4v = ax4*dt
    estado_novo = estado + (c1v + 2.*c2v + 2.*c3v + c4v)/6.
    return estado_novo

def acelera(t, estado):
    x, v = estado
    return np.array([v, F(x)/m])

# Simulação do movimento (igual ao item b)
x0 = 2.2
v0 = 0.0
dt = 0.01
t_total = 50
n_passos = int(t_total/dt)

t = np.zeros(n_passos)
x = np.zeros(n_passos)
v = np.zeros(n_passos)

estado = np.array([x0, v0])
for i in range(n_passos):
    t[i] = i*dt
    x[i], v[i] = estado
    estado = rk4(t[i], estado, acelera, dt)

# Encontrar um período completo (procura pelo primeiro retorno)
tol_periodo = 0.05
for i in range(1, len(x)):
    if abs(x[i] - x0) < tol_periodo and v[i]*v0 >= 0:
        it1 = i
        break
else:
    it1 = len(x)-1  # se não encontrar, usa todo o intervalo

# Análise de Fourier
nf_max = 20  # número máximo de harmônicos a calcular
af = np.zeros(nf_max+1)
bf = np.zeros(nf_max+1)

for nf in range(nf_max+1):
    af[nf], bf[nf] = abfourier(t, x, 0, it1, nf)

# Cálculo das amplitudes
amplitude = np.sqrt(af**2 + bf**2)

# Gráfico do espectro de Fourier
plt.figure(figsize=(10, 5))
plt.bar(range(nf_max+1), amplitude, width=0.5)
plt.xlabel('Ordem harmônica (n)')
plt.ylabel('Amplitude (m)')
plt.title('Espectro de Fourier do Movimento')
plt.xticks(range(0, nf_max+1, 2))
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(-0.5, nf_max+0.5)
plt.show()

# Resultados dos coeficientes
print("Coeficientes de Fourier:")
print(f"Componente fundamental (n=1): a1 = {af[1]:.4f}, b1 = {bf[1]:.4f}")
print(f"Segunda harmônica (n=2): a2 = {af[2]:.4f}, b2 = {bf[2]:.4f}")
print(f"Terceira harmônica (n=3): a3 = {af[3]:.4f}, b3 = {bf[3]:.4f}")

# Reconstrução do sinal com os primeiros N harmônicos
N_reconst = 5  # número de harmônicos para reconstrução
t_fine = np.linspace(0, t[it1], 500)
x_reconst = np.zeros_like(t_fine)

for nf in range(N_reconst+1):
    omega = 2*np.pi*nf/(t[it1]-t[0])
    x_reconst += af[nf]*np.cos(omega*t_fine) + bf[nf]*np.sin(omega*t_fine)

plt.figure(figsize=(10, 5))
plt.plot(t[:it1], x[:it1], 'b-', label='Sinal original', alpha=0.7)
plt.plot(t_fine, x_reconst, 'r--', label=f'Reconstrução com {N_reconst} harmônicos')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Comparação do sinal original com a reconstrução de Fourier')
plt.legend()
plt.grid(True)
plt.show()