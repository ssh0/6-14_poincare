#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# written by Shotaro Fujimoto, May 2014.

import SetParameter as sp

parameters = [{'a': 0.2}, {'b': 0.4}, {'c': 0.6}]


def clicked():
    quit()
    print 'clicked'


def quit():
    window.quit()

window = sp.SetParameter()
window.show_setting_window(parameters, {'click': clicked})
