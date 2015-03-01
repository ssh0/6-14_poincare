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
        y = np.array(y)
        k1 = h * f(t, y)
        k2 = h * f(t + 0.5*h, y + 0.5*h*k1)
        k3 = h * f(t + 0.5*h, y + 0.5*h*k2)
        k4 = h * f(t + 1.0*h, y + 0.5*h*k3)

        y = y + (k1 + 2*k2 + 2*k3 + k4)/6.0
        return y
