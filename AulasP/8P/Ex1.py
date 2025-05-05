import numpy as np
import matplotlib.pyplot as plt

t0 = 0.0
tf = 0.5
dt = 0.01

r0 = np.array([0.0,2.0,3.0])
v0 = np.array([160.0,20.0,-20.0])

g=9.8
v_T = 120.0
D = g/v_T**2

N = int((tf-t0)/dt) + 1
t= np.linspace(t0, tf, N)

a=np.zeros([np.size(t),3])
a_res = np.zeros([np.size(t),3])
a_grv=np.zeros([np.size(t),3])

v=np.zeros([np.size(t),3])
v[0,:] = v0

r=np.zeros([np.size(t),3])
r[0,:] = r0

for i in range(np.size(t)-1):
    a_grv[i,:] = -g*np.array([0.0,0.0,1.0])
    a_res[i,:] = -D*np.linalg.norm(v[i,:]) * v[i,:]
    a[i,:] = a_grv[i,:] + a_res[i,:]
    v[i +1,:] = v[i,:] + a[i,:] * dt
    r[i +1,:] = r[i,:] + v[i,:] * dt

    #Tirar para obter o movimento completo
    if r[i + 1, 2] <= 0:  # z <= 0
        print(f"Bola atinge o chão em t = {t[i+1]:.3f} s")
        print(f"Posição: x = {r[i+1,0]:.3f} m, y = {r[i+1,1]:.3f} m, z = {r[i+1,2]:.3f} m")
        break

plt.plot(t,r,label='Posição')
plt.xlabel("Tempo (s)")
plt.ylabel("Posição (m)")
plt.legend()
plt.show()


#Ex2

M = 0.057 # kg
v_norm = np.linalg.norm(v,axis=1)
E_p = M * g * r[0:i,2]
E_c = 0.5*M * v_norm[0:i]**2
E_m = E_p + E_c

print("Energia potencial: ", E_p[-1])
print("Energia cinética: ", E_c[-1])
print("Energia mecânica: ", E_m[-1])

#f: função a integrar
#D: domínio da função
#a: limite inferior da integral
#b: limite superior da integral
def integral(f,D,a,b):
    dt = (D[1]-D[0]) / len(f)
    i_a = int((a-D[0]) / dt)
    i_b = int((b-D[0]) / dt)
    sum = 0.0
    for i in range(i_a,i_b):
        sum += (f[i] + f[i+1]) / 2.0 * dt
    return sum

t1 = 0.2
t2 = 0.4
D = np.array([t[0],t[-1]])
F_res = M*a_res
F_dot_v = np.sum(F_res * v, axis=1)
W0 = integral(F_dot_v,D,t0,t0)
W1 = integral(F_dot_v,D,t0,t1)
W2 = integral(F_dot_v,D,t0,t2)

print("Trabalho total: ", W0)
print("Trabalho entre t0 e t1: ", W1)
print("Trabalho entre t0 e t2: ", W2)


