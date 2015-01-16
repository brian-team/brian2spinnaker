from brian2 import *
import brian2spinnaker

set_device('spinnaker')

N = 100
tau = 10*ms
Iin = 0.11/ms 
eqs = '''
dV/dt = -V/tau + Iin : 1
'''
G = NeuronGroup(N, eqs, threshold='V>1', reset='V=0')

run(100*ms)

device.build(directory='simple_example')
