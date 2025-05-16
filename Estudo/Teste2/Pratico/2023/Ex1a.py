import numpy as np
import matplotlib.pyplot as plt

t0 = 0.0
tf = 5
dt = 0.001
r0 = np.array([0.0, 3.0])  # (x, y)
v0 = np.array([30.0, 0.0]) # (vx, vy)
g = 9.8
R = 0.034 # raio da bola de ténis
A = np.pi*R**2
m = 0.057
dAr = 1.225
vT = 20 # velocidade terminal
D = g/vT**2 # coeficiente de arrasto

t = np.arange(t0, tf, dt)
a = np.zeros([2, np.size(t)])
v = np.zeros([2, np.size(t)])
v[:,0] = v0
r = np.zeros([2, np.size(t)])
r[:,0] = r0

for i in range(np.size(t)-1):
    v_norm = np.linalg.norm(v[:,i])
    a[0,i] = -D*v[0,i]*v_norm
    a[1,i] = -g - D*v[1,i]*v_norm
    v[:,i+1] = v[:,i] + a[:,i]*dt
    r[:,i+1] = r[:,i] + v[:,i]*dt
    if r[1,i+1] <= 0:  # bola tocou o solo
        break

# Trunca os arrays até ao impacto
t = t[:i+2]
r = r[:,:i+2]
v = v[:,:i+2]
a = a[:,:i+2]

# Gráfico XY
plt.plot(r[0,:], r[1,:], 'r--')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Trajetória da bola no plano XY')
plt.grid()
plt.show()

# Distância onde a bola cai
x_impacto = r[0,-1]
print(f"A bola cai a {x_impacto:.2f} m da linha de base.")

# Verificação do serviço válido
def servico_valido(r):
    # Passa sobre a rede (x=12m, y>1m)
    idx_rede = np.where(r[0,:] >= 12)[0][0]
    passa_rede = r[1,idx_rede] > 1
    # Cai dentro da área de serviço (12m < x < 18.4m)
    x_impacto = r[0,-1]
    dentro_area = 12 < x_impacto < 18.4
    return passa_rede and dentro_area

if servico_valido(r):
    print("Serviço Válido!")
else:
    print("Serviço Inválido!")
    