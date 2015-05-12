__author__ = 'eric'
# -*- coding: utf-8 -*-

import time


def AmaxB(A, B):
    a = time.strptime(A, '%H:%M:%S')
    b = time.strptime(B, '%H:%M:%S')

    if a >= b:
        return True
    else:
        return False
