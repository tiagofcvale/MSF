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

t0 = 0.0
tf = 300.0
dt = 0.001

k = 1 #N/m
b = 0.05 #kg/s
F_0 = 7.5 #N
wf = 0.5 #rad/s

x0 = 4 #m
v0 = 0.0 #m/s

m = 1.0
k = 1.0
b = 0.05

#inicializar dominio do tempo
t = np.arange(t0, tf, dt)

a = np.zeros(np.size(t))
v = np.zeros(np.size(t))
x = np.zeros(np.size(t))
x[0] = x0
v[0] = v0

for i in range(np.size(t) - 1):
    a[i] =  -(k * x[i] + b * v[i] - F_0 * np.cos(wf * t[i])) / m
    v[i + 1] = v[i] + a[i] * dt
    x[i + 1] = x[i] + v[i + 1] * dt

plt.plot(t, x, 'b-')
plt.xlabel('Tempo decorrido, t[s]')
plt.ylabel('Posição, x[m]')
plt.show()

#b)
t_max = np.array([])
x_max = np.array([])
T = np.array([])

for i in range(0, np.size(t) - 2, 2):
    tm, xm = maxminv(t[i], t[i + 1], t[i + 2], x[i], x[i + 1], x[i + 2])

    if t[i] < tm < t[i + 2]:
        if xm > np.maximum(x[i], x[i + 2]):
            t_max = np.append(t_max, tm)
            x_max = np.append(x_max, xm)
            if t_max.size > 1:
                T = np.append(T, t_max[-1] - t_max[-2])

plt.plot(t_max, x_max, '-b', label='Máximos locais')
plt.xlabel('Tempo decorrido, t[s]')
plt.ylabel('Posição, x[m]')
plt.plot(T, x_max[:-1], '-r', label='Períodos')
plt.legend()
plt.show()

# c) Amplitude em regime estacionário vs frequência forçada

t0 = 0.0
tf = 100.0
dt = 0.001
t = np.arange(t0, tf, dt)
wf_array = np.arange(0.2, 2.01, 0.04)  # mais pontos para melhor curva

amplitudes = []

for wf in wf_array:
    a = np.zeros_like(t)
    v = np.zeros_like(t)
    x = np.zeros_like(t)
    x[0] = x0
    v[0] = v0

    for j in range(len(t) - 1):
        a[j] = -(k * x[j] + b * v[j] - F_0 * np.cos(wf * t[j])) / m
        v[j + 1] = v[j] + a[j] * dt
        x[j + 1] = x[j] + v[j + 1] * dt

    # Considera só os últimos 20% do tempo para garantir regime estacionário
    x_regime = x[int(0.8*len(x)):]
    amp = (np.max(x_regime) - np.min(x_regime)) / 2
    amplitudes.append(amp)

plt.figure(figsize=(8,5))
plt.plot(wf_array, amplitudes, 'o-')
plt.xlabel('Frequência angular forçada $\\omega_f$ (rad/s)')
plt.ylabel('Amplitude em regime estacionário (m)')
plt.title('Amplitude vs Frequência Forçada')
plt.grid(True)
plt.show()

# Frequência de maior amplitude
idx_max = np.argmax(amplitudes)
print(f"Maior amplitude: {amplitudes[idx_max]:.3f} m ocorre para ωf = {wf_array[idx_max]:.2f} rad/s")

# Pergunta 1:
print("\nPergunta 1:")
print("A força externa realiza trabalho, pois fornece energia ao sistema para manter o movimento contra o amortecimento.")
print("O trabalho pode ser medido pela energia dissipada pelo amortecedor (b*v^2) ou pela área sob a curva F_ext * v(t) ao longo do tempo.")