import math
import numpy as np
import scipy as sp


#Constantes
e0 = 8.8541878128 * 10**-12
u0 = 12.566370614 * 10**-7

#variable inavariable
Q = 3

#Vecteur position
pos = np.array([[2.], [3.], [4.]])

#Variables dans S
V = 0.6
t = 10.

x, y, z = pos

#fonctions
def get_module(x, y, z):
    return math.sqrt(x**2 + y**2 + z**2)

def get_gamma():
    return 1/(math.sqrt(1.0 - (V**2)))

def transform_x(x):
    return get_gamma() * (x - (V*t))

def transform_t(t):
    return get_gamma() * (t - (V * x))

#Variables dans S'
xp = transform_x(x)
yp = y
zp = z
tp = transform_t(t)


#Champ électrique dans S:
def get_champ_elec(x, y, z):
    Etr = Q / (4 * math.pi * e0 * get_module(x, y, z)**3)
    return np.array([[x * Etr], [y * Etr], [z * Etr]])
    
#Champ électrique dans S':
def get_champ_elecprime(x, y, z):   
    Eptr = Q / (4 * math.pi * e0 * get_module(x, y, z)**3)
    return np.array([[x * Eptr], [y * Eptr * get_gamma()], [z * Eptr * get_gamma()]])

#Champ magnétique dans S:
def get_champ_mag(x, y, z):
    Btr = (u0 * Q * get_gamma() * V) / (4 * math.pi * (get_gamma()**2 * (transform_x(x) + V * transform_t(t))**2))
