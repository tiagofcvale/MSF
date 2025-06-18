import numpy as np
import matplotlib.pyplot as plt

comprimentos = np.arange(0.5, 10.5, 0.5)
g = 9.81 # m/s^2
teta = 0.1 # rad
t0 = 0.0 # s
tf = 10.0 # s
dt = 0.001 # s
v0 = 0.0 # m/s

t = np.arange(t0, tf, dt)
n = len(t)

for idx, L in enumerate(comprimentos):
    ainst = np.zeros(n)
    vang = np.zeros(n)
    ang = np.zeros(n)
    ang[0] = teta
    vang[0] = v0

    for i in range(n - 1):
        ainst[i] = -g/L * np.sin(ang[i])
        vang[i + 1] = vang[i] + ainst[i] * dt
        ang[i + 1] = ang[i] + vang[i + 1] * dt

# Calcular períodos para cada comprimento
periodos = np.array([2 * np.pi * np.sqrt(L / g) for L in comprimentos])

# Gráfico log-log
plt.figure(figsize=(6, 4))
plt.plot(np.log(comprimentos), np.log(periodos), 'o', label='log(T) vs log(L)')
plt.xlabel('log(Comprimento L [m])')
plt.ylabel('log(Período T [s])')
plt.title('log(T) em função de log(L) para o pêndulo')
plt.grid(True)
plt.legend()
plt.tight_layout()


#ajuste linear
x = np.log(comprimentos)
y = np.log(periodos)

p,b = np.polyfit(x, y, 1, cov=True)


plt.plot(x, p[0] * x + p[1], 'b-', label='Ajuste Linear')
plt.legend()
plt.show()

#Calcular declive
declive = p[0]
print("Declive: {:.2f}".format(declive))

