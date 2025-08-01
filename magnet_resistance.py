
from scipy.optimize import brentq
import matplotlib.pyplot as plt
import numpy as np

##########################################################
# compute measurements for a given solution (debugging): #
##########################################################

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

############################################################
#  use real world measurements: select magnet measurements #
############################################################

M = {

    # magnet dual 1386 TOP/MAIN (fridge#6)
    'DUAL TOP': np.array([198.0, 338.0, 196.0, 9.7]),
    # S = 1707.06
    # M0 [0.11598891 0.19800127 0.1148173  0.00568228]
    # R0 [0.13392475 0.7280323  0.132328   0.00571495]
    # R = [ 228.6 1242.8 225.9 9.8 ]

    # magnet dual 1386 LOWER/BOTTOM (firdge#6)
    'DUAL BOTTOM': np.array([76.8, 71.5, 6.5]),
    # S = 859.24
    # M0 [0.08938096 0.08321274 0.00756479]
    # R0 [0.90077306 0.09160404 0.0076229 ]
    # R = [ 774.0 78.7 6.5 ]

    # magnet 1935 (fridge#2)
    # '': np.array([x, x, x])

    # magnet 3314 (fridge#5)
    'SINGLE': np.array([355.0, 368.0, 197.0, 28.1])
    # S = 1495.61
    # M0 [0.23736196 0.24605409 0.13171917 0.01878837]
    # R0 [0.38758097 0.43718353 0.1560802  0.01915529]
    # R = [ 579.7 653.9 233.4 28.6 ]

}['SINGLE']

###########
# PROCEED #
###########

# G[i] = -1 means: the high root solution is selected
# G[i] = +1 means: the low root solution is selected
# we start with selecting all low value solutions
G = np.array([1.0] * len(M))

# find max measurement
i = M.argmax()

# compute minimum total resistance
S0 = 4.0 * M[i]


# root function
def F(s):
    T = 0
    for m, g in zip(M, G):
        T += g * np.sqrt(1.0 - 4.0 * m / s)
    return T + 2 - len(M)


# determine which branch contains the solution
G[i] = +1.0 if F(S0) <= 0.0 else -1.0

# compute solution (find root/zero)
S = brentq(F, S0, 10 * S0)

# display solutions:
print(f'S = {S:.2f}')
M0 = M / S

print('M0', M0)
R0 = (1.0 - G * np.sqrt(1.0 - 4.0 * M0)) / 2.0

print('R0', R0)
R = R0 * S

print('R = [ ', end='')
for r in R: print(f"{r:.1f} ", end='')
print(']')

# compute plot range
X = np.linspace(S0, 1.05 * S, 50)

# plot top branch
G[i] = +1.0
Y = [F(x) for x in X]
plt.plot(X, Y, '.-b')

# plot bottom branch
G[i] = -1.0
Y = [F(x) for x in X]
plt.plot(X, Y, '.-b')

# plot solution
plt.axvline(x=S, color='k', linestyle='-.')
plt.axhline(y=0, color='r', linestyle='-')

# Customizing
plt.xlabel('m')
plt.ylabel('F(m)')
plt.title('total loop resistance')

# Displaying the plot
plt.show()
