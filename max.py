from blueqat import Circuit
import numpy as np
from scipy.optimize import minimize

n=4
graph=[(0,1),(0,3),(1,2),(2,3)]


steps=2
init_params = 0.01 * np.random.rand(2,2)

def U_C(state,gamma):
	for edge in graph:
		j=edge[0]
		k=edge[1]
		state.cx[j,k]
		state.rz(gamma)[k]
		state.cx[j,k]

def U_B(state,beta):
	for i in range(n):
		state.rx(beta*2)[i]



def state_preparation(state,gamma,beta):
	state.h[:]
	for i in range(steps):
		U_C(state,gamma[i])
		U_B(state,beta[i])
	return state



def exp_val(state,edge):
	shots=1000
	c=state.run(shots=shots)
	expval=0
	for i in c:
		#print(i[edge[0]])
		#print(i[edge[1]])
		if (i[edge[0]]=='0' and i[edge[1]]=='0') or (i[edge[0]]=='1' and i[edge[1]]=='1'):
			expval+=c[i]/shots
			
		else:
			expval-=c[i]/shots
				
	return expval


c=Circuit()	

def max_cut(params):
	gamma=[]
	beta=[]
	for i in range(len(params)):
		if i%2==0:
			gamma.append(params[i])
		else:
			beta.append(params[i])
	state=Circuit(n)
	circ=state_preparation(state,gamma,beta)
	circ.m[:]
	print(circ.run(shots=1000))
	#print(state.run(shots=1000))
	obj=0
	for edge in graph:
		obj=obj - 0.5 * (1 - exp_val(circ,edge))
	return obj


tol_val=1e-2 # The tolerance value for the optimization procedure

result=minimize(max_cut,init_params, method="Powell" , tol=tol_val)

print(f'The Objective after optimization is {-result.fun}')


		



