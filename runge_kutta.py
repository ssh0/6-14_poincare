#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# written by Shotaro Fujimoto, May 2014.

import numpy as np


class RK4(object):

    def __init__(self, function):
        """ Initialize function."""
        self.function = function
        
    def solve(self, y, t, h):
        """ Solve the system ODEs.

        --- arguments ---
        y: A list of initial values
        t: Time (float)
        h: Stepsize (float)
        """
        f = self.function
        k1 = h * f(t, *y)
        k2 = h * f(t+0.5*h, *[y[i]+0.5*h*k1[i] for i in range(len(y))])
        k3 = h * f(t+0.5*h, *[y[i]+0.5*h*k2[i] for i in range(len(y))])
        k4 = h * f(t+1.0*h, *[y[i]+0.5*h*k3[i] for i in range(len(y))])

        y = np.array([y[i] + (k1[i]+2*k2[i]+2*k3[i]+k4[i])/6.0
                      for i in range(len(y))
                      ])
        return y
