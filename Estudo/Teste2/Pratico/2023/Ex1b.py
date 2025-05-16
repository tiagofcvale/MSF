import numpy as np
import matplotlib.pyplot as plt

t0 = 0.0
tf = 0.5
dt = 0.001
r0 = np.array([0.0, 3.0, 0.0])
v0 = np.array([30.0, 0.0, 0.0])
w = np.array([0.0, 0.0, -60.0]) # rad/s (spin em torno do eixo Z)
g = 9.8
R = 0.11
A = np.pi*R**2
m = 0.45
dAr = 1.225
vT = 100*1000/3600
D = g/vT**2

t = np.arange(t0, tf, dt)
a = np.zeros([3, np.size(t)])
v = np.zeros([3, np.size(t)])
v[:,0] = v0
r = np.zeros([3, np.size(t)])
r[:,0] = r0

impact_idx = None
for i in range(np.size(t)-1):
    v_norm = np.linalg.norm(v[:,i])
    # Magnus force (já incluída)
    a[0,i] = -D*v[0,i]*v_norm + A*dAr*R*w[2]*v[2,i]/(2*m)
    a[1,i] = -g - D*v[1,i]*v_norm
    a[2,i] = -D*v[2,i]*v_norm - A*dAr*R*w[2]*v[0,i]/(2*m)
    v[:,i+1] = v[:,i] + a[:,i]*dt
    r[:,i+1] = r[:,i] + v[:,i]*dt
    if r[1,i+1] <= 0 and impact_idx is None:
        impact_idx = i+1
        break

# Truncar arrays até ao impacto
if impact_idx is not None:
    t = t[:impact_idx+1]
    r = r[:,:impact_idx+1]
    v = v[:,:impact_idx+1]
    a = a[:,:impact_idx+1]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(r[0,:], r[2,:], r[1,:], 'r--')
ax.set_xlabel('X')
ax.set_ylabel('Z')
ax.set_zlabel('Y')
plt.show()

print("Tempo de impacto (txzero) = {:.3f} s".format(t[-1]))
print("   x = {:.2f} m".format(r[0,-1]))
print("   y = {:.2f} m".format(r[1,-1]))
print("   z = {:.2f} m".format(r[2,-1]))

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