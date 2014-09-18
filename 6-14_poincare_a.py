#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# written by Shotaro Fujimoto, May 2014.
"""外力を受けた減衰振り子のシミュレーション
外力の周期ごとにθ-dθ/dtのプロットを表示する。
初めのntransient回の計算結果は表示しない。
"""

from math import *
import numpy as np
import matplotlib.pylab as plt
import SetParameter as sp
import runge_kutta as RK

# --- parameters ---
omega0 = 1
omega = 2
T = pi                 # <-- (2*pi)/omega (time period)
nstep = 1000
dt = T / nstep           # stepsize in a time period
ntransient = 100
nplot = 100
nmax = ntransient + nplot


def assignment():
    """ Assign the values to variables."""
    global theta, ang_vel, gamma, A
    theta = float(window.entry[0].get())
    ang_vel = float(window.entry[1].get())
    gamma = float(window.entry[2].get())
    A = float(window.entry[3].get())
    window.quit()
    plot(y=np.array([theta, ang_vel]), function=force)


def force(t, *y):
    theta = y[0]
    ang_vel = y[1]
    return np.array([ang_vel,
                     -gamma * ang_vel -
                   (omega0 ** 2 + 2 * A * cos(omega * t)) * sin(theta)
    ])


def plot(y, function):
    """ Show an animation of Poincare plot.

    --- arguments ---
    y: A list of initial values
    function: function which is argument of Runge-Kutta solver
    """
    h = dt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid()
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)
    plt.ion()

    for i in range(nmax + 1):
        for j in range(nstep):
            rk4 = RK.RK4(function)
            y = rk4.solve(y, j * h, h)
            # -pi <= theta <= pi
            while y[0] > pi:
                y[0] = y[0] - 2 * pi
            while y[0] < -pi:
                y[0] = y[0] + 2 * pi

        if ntransient <= i < nmax:          # <-- draw the poincare plots
            plt.scatter(y[0], y[1], s=2.0, marker='o', color='blue')
            time_text.set_text('n = %d' % i)
            plt.draw()

        if i == nmax:                       # <-- to stop the interactive mode
            plt.ioff()
            plt.scatter(y[0], y[1], s=2.0, marker='o', color='blue')
            time_text.set_text('n = %d' % i)
            plt.show()

if __name__ == '__main__':

    default_params = [
        {'theta': 0.3}, {'ang_vel': 0.0}, {'gamma': 0.2}, {'A': 0.85}]

    window = sp.SetParameter()
    window.show_setting_window(default_params, {'Run!': assignment})
