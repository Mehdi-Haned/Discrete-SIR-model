import numpy as np
import matplotlib.pyplot as plt
import random

plt.style.use(["science", "notebook", "grid"])

##==============================================================================

# Simulation functions

def simulation(tmax, S0 = 999, I0 = 1, R0 = 0, inf = 0.3, rec = 0.01):
  '''
  tmax: Only mandatory variable. Maximum amount of time in days the simulation
    is run for
  S0: initial susceptable population
  I0: initial infected population
  R0: initial recovered population
  inf: chance that a susceptable person becoms infected when they meet 
    an infected person
  rec: chance an infected person will recover (and become immune) on a
    given day
  '''
  
  S,I,R = (np.zeros(tmax+1, dtype='int'), 
           np.zeros(tmax+1, dtype='int'), 
           np.zeros(tmax+1, dtype='int'))
  
  S[0], I[0], R[0] = S0, I0, R0
  
  for i in range(1, tmax+1):
    '''
    At the start of each day, each of my compartments is going to start with
      the population of the previous day and then modify it according to the
      parameters.
    '''
    S[i], I[i], R[i] = S[i-1], I[i-1], R[i-1]
    
    if i>7: # no recoveries for the first week
      for j in range(I[i-1]):
        r = random.random()
        if r <= rec:
          I[i] -= 1
          R[i] += 1
    
    rs = random.randint(0, S[i])
    ri = random.randint(0, I[i])
    ref = min(rs, ri)    
    
    for j in range(ref):
      r = random.random()
      if r <= inf:
        I[i] += 1
        S[i] -= 1
  
  return S, I, R

def average_out(A):
  '''
  Takes an array conatining multiple simulations and averages them ut into 
    a single array conatining the average of the simulations for all time
    steps
  '''
  ans = []
  for i in A:
    ans.append(np.mean(i))
  return np.array(ans)
    
##==============================================================================

# Parameters

# how long the simulation is run for and how many there are
tmax = 200
nsims = 50

# initial population
N = 10_000

i0 = 2
r0 = 0
s0 = N - (i0 + r0)

# Simualation parameters
inf_rate = 0.6
rec_rate = 1/14

##==============================================================================

# The multiple simulations

(ssims, isims, rsims) = (np.zeros((tmax+1, nsims)), 
                         np.zeros((tmax+1, nsims)), 
                         np.zeros((tmax+1, nsims)))

for i in range(nsims):
  data = simulation(tmax, S0 = s0, R0 = r0, I0 = i0,
                    inf = inf_rate, rec = rec_rate)
  ssims[:,i] = data[0]
  isims[:,i] = data[1]
  rsims[:,i] = data[2]

S,I,R = np.transpose(ssims), np.transpose(isims), np.transpose(rsims)

t = np.arange(0,tmax+1,1)

width = 0.15

for i in range(nsims):
  plt.plot(t, S[i], c = 'b', lw = width)
  plt.plot(t, I[i], c = 'r', lw = width)
  plt.plot(t, R[i], c = 'g', lw = width)
#  plt.plot(t, R[i]+I[i]+S[i], c = 'k', lw = width)
# last one is to test that the population is constant


##==============================================================================

#Average Simulations

width2 = 3

avs, avi, avr = average_out(ssims), average_out(isims), average_out(rsims)

plt.plot(t, avs, c = 'b', lw = width2, label = 'Susceptable')
plt.plot(t, avi, c = 'r', lw = width2, label = 'Infected')
plt.plot(t, avr, c = 'g', lw = width2, label = 'Recovered')
#plt.plot(t, avi+avr+avs, c = 'k', lw = width2)
# last one is to test that the population is constant

##==============================================================================

#plotting

plt.grid()

plt.title(f'SIR model with {nsims} simulations and their averages for {tmax} \
days')

plt.xlabel(f'Time [days] \n\
{inf_rate*100}% chance of getting infected on interaction \n\
{rec_rate*100}% chance of an infected person recovering on a given day')

plt.ylabel('Number of People')
plt.legend()
plt.grid()
plt.subplots_adjust(left=0.15, right=0.9, top=0.85, bottom=0.155)

plt.show()
