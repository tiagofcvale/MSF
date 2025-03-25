import numpy as np
import matplotlib.pyplot as plt

def minimos_quadrados(X, Y, N):
    sumX = np.sum(X)
    sumY = np.sum(Y)
    sumX2 = np.sum(X ** 2)
    sumY2 = np.sum(Y ** 2)
    sumXY = np.sum(X * Y)

    m = (N * sumXY - sumX * sumY) / ((N * sumX2) - ((sumX)**2)) #declive

    b = (sumX2 * sumY - sumX * sumXY) / (N * sumX2 - (sumX**2)) #ordenada na origem

    r2 = (N * sumXY - sumX * sumY)**2 / ((N* sumX2 - (sumX)**2)*(N * sumY2 - (sumY)**2)) #coeficiente de correlação linear

    dm = abs(m)*(np.sqrt((( 1 / r2 ) - 1)/(N - 2))) 

    db = dm*np.sqrt(sumX2 / N)
    return m,b,r2,dm,db


t_vals = np.array([0,1,2,3,4,5,6,7])
N_vals = np.array([11,20,33,54,83,134,244,425])
N = len(t_vals)

#a)
m,b,r2,dm,db = minimos_quadrados(t_vals,N_vals,N)
x = np.array([np.min(t_vals), np.max(t_vals)])
y = m*x+b

plt.scatter(t_vals,N_vals,label="Original")
plt.plot(x,y,label="Regressão dos minimos quadrados",color="red")
plt.legend()
plt.show()

#b)
t_log = np.log(t_vals)
N_log = np.log(N_vals)
N = len(t_log)

m,b,r2,dm,db = minimos_quadrados(t_vals,N_log,N)

x = np.array([np.min(t_vals), np.max(t_vals)])
y = m*x+b
plt.scatter(t_vals,N_log,label="log")
plt.plot(x,y,label="Regressão dos minimos quadrados",color="red")
plt.legend()
plt.show()

#c)
plt.scatter(t_vals,N_vals,label="Dados")
plt.loglog(t_vals,N_vals,label="Exponecial",color="red")
plt.legend()
plt.show()

"""Pelos resultados das alíneas a) e b) podemos concluir
que a relação entre o tempo e o número de bactérias é
exponencial"""