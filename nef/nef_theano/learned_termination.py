try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

import numpy as np
import theano
import theano.tensor as TT

from . import neuron

class LearnedTermination(object):
    """This is the superclass learned_termination that attaches
    to an ensemble."""

    def __init__(self, pre, post, error, initial_weight_matrix,
                 dt=1e-3, pstc=5e-3):
        """
        :param Ensemble pre: the pre-synaptic ensemble
        :param Ensemble ensemble:
            the post-synaptic ensemble (to which this termination is attached)
        :param Origin error: the source of the error signal that directs learning
        :param np.array weight_matrix:
            the connection weight matrix between pre and post
        """
        self.dt = dt
        self.pstc = pstc

        self.pre = pre
        self.post = post
        self.error = error

        # initialize weight matrix
        self.initial_weight_matrix = initial_weight_matrix.astype('float32')
        self.weight_matrix = theano.shared(
            self.initial_weight_matrix, name='learned_termination.weight_matrix')

    def reset(self):
        self.weight_matrix.set_value(self.initial_weight_matrix)
    
    def learn(self):
        """The learning function, to be implemented by learning subclasses.

        :returns:
            The updated value for the weight matrix, as a Theano variable.
        """
        raise NotImplementedError()

    def update(self):
        """The updates to the weight matrix calculation.
        
        :returns: an ordered dictionary with the new weight_matrix.
        
        """
        # multiply the output by the attached ensemble's radius
        # to put us back in the right range
        return OrderedDict( {self.weight_matrix: self.learn()} ) 


#TODO: This should be in the tests that need it, not in the main code?
class NullLearnedTermination(LearnedTermination):
    """This is a stub learning termination for architecture testing"""
    def learn(self):
        return self.weight_matrix
