import numpy as np
import matplotlib.pyplot as plt

#Constantes:
G = 4*np.pi**2 #Constante gravitacional (AU³/(kg*ano²))
mTerra = 3.003 * 10**-6 #Massa Terra
mSol = 1 #Massa sol
rx = 1 #AU
vy = 2*np.pi #Velocidade da Terra (AU/ano)
dt = 0.00001
tf = 2 #Ano

#a)
#Simule a órbita da Terra á volta do sol, usando o método de Euler, sabendo
#que a força de atração da Terra exercida pelo Sol é Fgav = -G*mTerra*mSol/r²

def euler_orbitra(r0, v0, dt, tf):
    #N = Número de passos
    N = int(tf / dt)
    t = np.linspace(0, tf, N)


    a = np.zeros((np.size(t), 2))
    a[0, :] = np.array([0.0, 0.0])

    r = np.zeros((np.size(t), 2))
    r[0, :] = np.array([r0, 0.0])

    v = np.zeros((np.size(t), 2))
    v[0, :] = np.array([0.0, v0])


    for i in range(N-1):

        a[i, :] = -G*r[i,:] / np.linalg.norm(r[i,:])**3
        v[i+1,:] = v[i,:] + a[i, : ]*dt
        r[i+1,:] = r[i,:] + v[i,:]*dt


    return t, r

t,r = euler_orbitra(rx, vy, dt, tf)

plt.plot(r[:,0], r[:,1], label="Órbita da Terra", color="blue")
plt.scatter(0, 0, color="yellow", label="Sol")
plt.scatter(rx, 0, color="red", label="Terra")
plt.xlabel("x (AU)")
plt.ylabel("y (AU)")
plt.title("Órbita da Terra em torno do Sol")
plt.legend()
plt.show()