
from scipy.optimize import brentq
import matplotlib.pyplot as plt
import numpy as np

##############################################################
### compute measurements for a given solution (debugging): ###
##############################################################

# R = np.array([300.0, 300.0, 300.0, 3000.0])
# R = np.array([300.0, 600.0, 300.0, 10.0])

# print('R', R)
# S = np.sum(R)
# print('S', S)
# R0 = R / S
# print('R0', R0)
# M0 = R0*(1.0-R0)
# print('M0', M0)
# M = S*M0
# print('M', M)

#####################################
###  use real world measurements: ###
#####################################

M = np.array([198.0, 338.0, 196.0, 9.7]) # magnet 3314 (fridge 5)
M = np.array([355.0, 368.0, 197.0, 28.1])


###############
### PROCEED ###
###############

# G[i] = -1 means: the high root solution is selected
# G[i] = +1 means: the low root solution is selected
# we start with selecting all low value solutions
G = np.array([1.0]*len(M))

# find max measurement
i = M.argmax()

# compute minimum total resistance
S0 = 4.0 * M[i]

# compute solution range
X = np.linspace(S0, 1.5*S0, 50)

# root function
def F(s):
    T = 0
    for m, g in zip(M, G):
        T += g*np.sqrt(1.0-4.0*m/s)
    return T+2-len(M)

# plot top branch
Y = [F(x) for x in X]
plt.plot(X, Y, '.-b')

# plot bottom branch
G[i] = -1.0
Y = [F(x) for x in X]
plt.plot(X, Y, '.-b')

# determine which branch contains the solution
if F(S0) < 0: G[i] = +1.0

# compute solution (find root/zero)
S = brentq(F, S0, 2*S0)

# display solutions:
print('S', S)
M0 = M / S
print('M0', M0)
R0 = (1.0-np.sqrt(1.0-4.0*M0))/2.0
print('R0', R0)
R = R0*S
print('R [ ', end='')
for r in R: print(f"{r:.1f} ", end='')
print(']')

# plot solution
plt.axvline(x=S, color='k', linestyle='-')
plt.axhline(y=0, color='r', linestyle='-')

# Customizing
plt.xlabel('m')
plt.ylabel('F(m)')
plt.title('total loop resistance')

# Displaying the plot
plt.show()
