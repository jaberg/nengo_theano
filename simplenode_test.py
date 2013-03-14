"""This is a test file to test the SimpleNode object"""

import nef_theano as nef
import numpy as np
import matplotlib.pyplot as plt
import math
import random

net=nef.Network('SimpleNode Test')

class TrainingInput(nef.simplenode.SimpleNode):
    def init(self):
        self.input_vals = np.arange(-1, 1, .2)
        self.period_length = 2
        self.choose_time = 0.0

    def origin_test1(self):
        if (self.t >= self.choose_time):
            self.index = random.randint(0,9) # choose an input randomly from the set
            if (self.index < 5): # specify the correct response for this input
                self.correct_response = [.5]
            else:
                self.correct_response = [-.5]
            # update the time to next change the input again
            self.choose_time = self.t + self.period_length
        return [self.input_vals[self.index]]

    def origin_test2(self):
        return self.correct_response

    def origin_test3(self):
        return [.93, -1, -.1]

    def reset(self, **kwargs):
        self.choose_time = 0.0
        nef.SimpleNode.reset(self, **kwargs)

net.add(TrainingInput('SNinput'))

net.make('A', neurons=300, dimensions=1)
net.make('B', neurons=300, dimensions=1)
net.make('C', neurons=300, dimensions=3)

net.connect('SNinput:test1', 'A')
net.connect('SNinput:test2', 'B')
net.connect('SNinput:test3', 'C')

timesteps = 500
dt_step = 0.01
t = np.linspace(dt_step, timesteps*dt_step, timesteps)
pstc = 0.01
I1p = net.make_probe(net.nodes['SNinput'].origin['test1'].decoded_output, dt_sample=dt_step, pstc=pstc)
I2p = net.make_probe(net.nodes['SNinput'].origin['test2'].decoded_output, dt_sample=dt_step, pstc=pstc)
I3p = net.make_probe(net.nodes['SNinput'].origin['test3'].decoded_output, dt_sample=dt_step, pstc=pstc)
Ap = net.make_probe(net.nodes['A'].origin['X'].decoded_output, dt_sample=dt_step, pstc=pstc)
Bp = net.make_probe(net.nodes['B'].origin['X'].decoded_output, dt_sample=dt_step, pstc=pstc)
Cp = net.make_probe(net.nodes['C'].origin['X'].decoded_output, dt_sample=dt_step, pstc=pstc)

print "starting simulation"
net.run(timesteps*dt_step)

# plot the results
plt.ion(); plt.close(); 
plt.subplot(411); plt.title('SNinput'); 
plt.hold(1)
plt.plot(I1p.get_data()); plt.plot(I2p.get_data()); plt.plot(I3p.get_data())
plt.legend(['test1','test2','test3'])
plt.subplot(412); plt.title('A'); 
plt.plot(Ap.get_data())
plt.subplot(413); plt.title('B'); 
plt.plot(Bp.get_data())
plt.subplot(414); plt.title('C'); 
plt.plot(Cp.get_data())
