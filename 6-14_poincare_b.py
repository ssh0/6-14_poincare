#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# written by Shotaro Fujimoto, May 2014.
"""外力を受けた減衰振り子のシミュレーション
θとdθ/dtをtの関数としてプロットする。
"""

from math import *
import numpy as np
import matplotlib.pylab as plt
import SetParameter as sp
import runge_kutta as RK

# --- parameters ---
omega0 = 1
omega = 2
T = pi                  # <-- (2*pi)/omega (time period)
tmax = 10. * T
dt = 0.1                # stepsize in a time period


def assignment():
    """ Assign the values to variables."""
    global theta, ang_vel, gamma, A
    theta = float(window.entry[0].get())
    ang_vel = float(window.entry[1].get())
    gamma = float(window.entry[2].get())
    A = float(window.entry[3].get())
    window.quit()
    plot(function=force)


def force(t, *y):
    theta = y[0]
    ang_vel = y[1]
    return np.array([ang_vel,
                     -gamma * ang_vel -
                   (omega0 ** 2 + 2 * A * cos(omega * t)) * sin(theta)
    ])


def plot(function):
    """ Show an animation of Poincare plot.

    --- arguments ---
    y: A list of initial values
    function: function which is argument of Runge-Kutta solver
    """
    y = np.array([theta, ang_vel])
    h = dt
    rk4 = RK.RK4(function)

    def calc(y, t, h):
        y = rk4.solve(y, t, h)
        # -pi <= theta <= pi
        while y[0] > pi:
            y[0] = y[0] - 2 * pi
        while y[0] < -pi:
            y[0] = y[0] + 2 * pi
        return y

    t = np.arange(0, tmax, dt)
    res_theta = np.zeros(len(t), np.float32)
    res_ang_vel = np.zeros(len(t), np.float32)

    for i, _t in enumerate(t):
        res_theta[i] = y[0]
        res_ang_vel[i] = y[1]
        y = calc(y, _t, h)

    fig = plt.figure()
    fig.subplots_adjust(hspace=0.4)

    ax1 = fig.add_subplot(211)
    ax1.plot(t, res_theta, label=r'$\theta$')
    ax1.set_xlim(0, tmax)
    plt.xlabel(r'$t$', fontsize=16)
    plt.ylabel(r'$\theta$', fontsize=16)
    plt.title(r'$t\ -\ \theta$')
    plt.legend(loc="best")

    ax2 = fig.add_subplot(212)
    ax2.plot(t, res_ang_vel, label=r'$d\theta /dt$')
    ax2.set_xlim(0, tmax)
    plt.xlabel(r'$t$', fontsize=16)
    plt.ylabel(r'$d\theta /dt$', fontsize=16)
    plt.title(r'$t\ -\ d\theta /dt$')
    plt.legend(loc="best")

    plt.show()

if __name__ == '__main__':

    default_params = [
        {'theta': 0.1}, {'ang_vel': 0.0}, {'gamma': 0.2}, {'A': 0.85}]

    window = sp.SetParameter()
    window.show_setting_window(default_params, {'Run!': assignment})
