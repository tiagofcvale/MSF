import numpy as np
import matplotlib.pyplot as plt

def EulerComResistencia(y0, v0, t0, tf, dt, g, v_terminal):
    # Número de passos
    N = int((tf - t0) / dt + 0.5)  # Arredonda para o inteiro mais próximo
    
    # Inicializa arrays
    t = np.zeros(N+1)
    y = np.zeros(N+1)
    v = np.zeros(N+1)
    a = np.zeros(N+1)
    # Condições iniciais
    t[0] = t0
    y[0] = y0
    v[0] = v0
    a[0] = 0

    k = g / v_terminal**2
    
    for i in range(N):
        t[i+1] = t[i] + dt
        
        acceleration = -g - k * v[i] * abs(v[i])
        
        a[i+1] = acceleration
        v[i+1] = v[i] + acceleration * dt
        y[i+1] = y[i] + v[i] * dt
        
        if y[i+1] < 0: #Quando Bate no chão para
            break
    
    return t[:i+2], y[:i+2], v[:i+2]

y0 = 0, v0 = 50, t0 = 0, tf = 5, dt = 0.001, g = 9.8, vT = 100

t_vals, y_vals, v_vals = EulerComResistencia(y0, v0, t0, tf, dt, g, vT)

plt.plot(t_vals,y_vals,label="Dados")
plt.xlabel("Tempo (s)")
plt.ylabel("Altura (m)")
plt.show()

#b)
tf = 20 #foguete não explode imediatamente
t_vals2, y_vals2, v_vals2 = EulerComResistencia(y0, v0, t0, tf, dt, g, vT)

idxmax = np.argmax(y_vals2)
hmax = y_vals2[idxmax]
smax = t_vals2[idxmax]
print("Altura máxima do foguete caso não explodisse: {:.2f} metros aos {:.2f} segundos".format(hmax,smax))

difh = hmax - y_vals[-1]
print("Altura em que explode: {:.2f} metros".format(y_vals[-1]))
print("A diferença de altura da altura máxima e da altura de explosão é de {:.2f} metros".format(difh))

#Como o foguete antinge a altura máxima antes de explodir, significa que explode depois de atingir a altura máxima.
