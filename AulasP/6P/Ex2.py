import numpy as np
import matplotlib.pyplot as plt

#Constantes:
G = 4*np.pi**2 #Constante gravitacional (AU³/(kg*ano²))
mTerra = 3.003 * 10**-6 #Massa Terra
mSol = 1 #Massa sol
rx = 1 #AU
vy = 2*np.pi #Velocidade da Terra (AU/ano)
dt = 0.0001
tf = 2 #Ano


def euler_cromer(r0, v0, dt, tf):
    N = int(tf / dt)
    x = np.zeros(N)
    y = np.zeros(N)
    vx = np.zeros(N)
    vy = np.zeros(N)
    t = np.linspace(0, tf, N)
    ax = np.zeros(N)
    ay = np.zeros(N)


    x[0], y[0] = r0, 0
    vx[0], vy[0] = 0, v0 

    for i in range(N-1):
        t[i+1]=t[i]+dt
        r=np.sqrt(x[i]**2+y[i]**2)

        ax[i]=-G/r**3*x[i]
        ay[i]=-G/r**3*y[i]

        vx[i+1]=vx[i]+ax[i]*dt
        vy[i+1]=vy[i]+ay[i]*dt

        x[i+1]=x[i]+vx[i+1]*dt
        y[i+1]=y[i]+vy[i+1]*dt


    return t, x, y

t,x,y = euler_cromer(rx, vy, dt, tf)

plt.plot(x,y,label="Órbita da Terra",color="blue")
plt.xlabel("x (AU)")
plt.ylabel("y (AU)")
plt.title("Órbita da Terra em torno do Sol")
plt.legend()
plt.show()