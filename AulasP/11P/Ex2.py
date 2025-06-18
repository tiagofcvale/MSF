import numpy as np
import matplotlib.pyplot as plt

def rk4_x_vx(t,x,vx,acelera,dt):
    """
    Integração numérica de equação diferencial de 2ª ordem:
			d2x/dt2 = ax(t,x,vx)    com dx/dt= vx    de valor inicial
	Erro global:  proporcional a dt**4
    acelera=dvx/dt=Força(t,x,vx)/massa      : acelera é uma FUNÇÃO
    input:  t = instante de tempo
            x(t) = posição
            vx(t) = velocidade
            dt = passo temporal 
    output: xp = x(t+dt)
		    vxp = vx(t+dt)
    """
    ax1=acelera(t,x,vx)
    c1v=ax1*dt
    c1x=vx*dt
    ax2=acelera(t+dt/2.,x+c1x/2.,vx+c1v/2.)
    c2v=ax2*dt
    c2x=(vx+c1v/2.)*dt			# predicto:  vx(t+dt) * dt
    ax3=acelera(t+dt/2.,x+c2x/2.,vx+c2v/2.)
    c3v=ax3*dt
    c3x=(vx+c2v/2.)*dt
    ax4=acelera(t+dt,x+c3x,vx+c3v)
    c4v=ax4*dt
    c4x=(vx+c3v)*dt
      
    xp=x+(c1x+2.*c2x+2.*c3x+c4x)/6.
    vxp=vx+(c1v+2.*c2v+2.*c3v+c4v)/6.
    return xp,vxp

# Parâmetros do problema
m = 1.0      # kg
k = 0.2      # N/m
alpha = 1.0  # N/m^3
b = 0.01     # kg/s
F0 = 5.0     # N
wf = 0.6     # rad/s

# Condições iniciais
x0 = 1.0     # m
v0 = 0.0     # m/s

# Tempo de simulação
t0 = 0.0
tf = 50.0
dt = 0.001
t = np.arange(t0, tf+dt, dt)
n = len(t)

# Arrays para posição e velocidade
x = np.zeros(n)
v = np.zeros(n)
x[0] = x0
v[0] = v0

# Função aceleração
# Função acelera recebe (t, x, v)
def acelera(ti, xi, vi):
    return (-k*xi - 4*alpha*xi**3 - b*vi + F0*np.cos(wf*ti)) / m

# Integração RK4 para sistema de 2ª ordem (x, v)
for i in range(n-1):
    x[i+1], v[i+1] = rk4_x_vx(t[i], x[i], v[i], acelera, dt)

# Gráfico
plt.figure(figsize=(10,5))
plt.plot(t, x, label='x(t)')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição x (m)')
plt.title('Oscilador quártico forçado (RK4)')
plt.grid(True)
plt.legend()
plt.show()

#c) Agora com x0 ligeiramente diferente
t0 = 0.0
tf = 100.0  # agora até 100 s
dt = 0.001
t = np.arange(t0, tf+dt, dt)
n = len(t)

# Condições iniciais
x0 = 1.0001   # posição inicial ligeiramente diferente
v0 = 0.0      # velocidade inicial

# Arrays para posição e velocidade
x = np.zeros(n)
v = np.zeros(n)
x[0] = x0
v[0] = v0

# Integração RK4 para sistema de 2ª ordem (x, v)
for i in range(n-1):
    x[i+1], v[i+1] = rk4_x_vx(t[i], x[i], v[i], acelera, dt)

# Gráfico
plt.figure(figsize=(10,5))
plt.plot(t, x, label='x(t) com x0=1.0001 m')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição x (m)')
plt.title('Oscilador quártico forçado (RK4) - x0=1.0001 m')
plt.grid(True)
plt.legend()
plt.show()

#d)
# Gráfico do espaço de fase
plt.figure(figsize=(8,5))
plt.plot(x, v, label='Espaço de fase')
plt.xlabel('Posição x (m)')
plt.ylabel('Velocidade v (m/s)')
plt.title('Espaço de fase do oscilador quártico forçado')
plt.grid(True)
plt.legend()
plt.show()

print("A velocidade é maxima nos atratores e longe é minima")
print("As duas trajetorias iniciam com uma fase praticamente identica")