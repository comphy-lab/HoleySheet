# To out theta over time

import numpy as np
import os
import subprocess as sp
from scipy.optimize import fsolve

def getting_facet1(filename):
    exe = ["./getFacet1", filename]
    p = sp.Popen(exe, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    temp1 = stderr.decode("utf-8")
    lines = temp1.splitlines()
    x = []
    y = []
    for line in lines:
        values = line.split()
        if len(values) == 2:  
            try:
                x_val = float(values[0])
                y_val = float(values[1])
                x.append(x_val)
                y.append(y_val)
            except ValueError:
                continue
    # Convert lists to numpy arrays
    x = np.array(x)
    y = np.array(y)
    theta = np.arctan2(y, x)
    sorted_indices = np.argsort(theta)
    return np.array(x)[sorted_indices], np.array(y)[sorted_indices], np.array(theta)[sorted_indices]

# ----------------------------------------------------------------------------------------------------------------------

def getting_facet2(filename):
    exe = ["./getFacet2", filename]
    p = sp.Popen(exe, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    temp1 = stderr.decode("utf-8")
    lines = temp1.splitlines()
    x = []
    y = []
    for line in lines:
        values = line.split()
        if len(values) == 2:  
            try:
                x_val = float(values[0])
                y_val = float(values[1])
                x.append(x_val)
                y.append(y_val)
            except ValueError:
                continue
    # Convert lists to numpy arrays
    x = np.array(x)
    y = np.array(y)
    theta = np.arctan2(y, x)
    sorted_indices = np.argsort(theta)
    return np.array(x)[sorted_indices], np.array(y)[sorted_indices], np.array(theta)[sorted_indices]

# ----------------------------------------------------------------------------------------------------------------------

def func(theta):
    # Interpolate r_fit1 and r_fit2 at the given theta
    r1 = np.interp(theta, theta_fit, r_fit1)
    r2 = np.interp(theta, theta_fit, r_fit2)
    return r1 - r2 - 2e-2

def fitradius(r, theta, theta_fit):
    degree = 10
    coefficients = np.polyfit(theta, r, degree)
    return np.polyval(coefficients, theta_fit)

nGFS = 10000
tsnap = 0.1
    
for ti in range(1):
    t = tsnap*ti
    place = "intermediate/snapshot-%5.4f" % t

    if not os.path.exists(place):
        print("%s File not found!" % place)
    else:
            x1, y1, theta1 = getting_facet1(place) 
            x2, y2, theta2 = getting_facet2(place) 
            r1 = np.sqrt(x1*x1+y1*y1)
            r2 = np.sqrt(x2*x2+y2*y2) 
            theta_fit = np.linspace(0, np.pi/2, 1000)
            r_fit1 = fitradius(r1, theta1, theta_fit)
            r_fit2 = fitradius(r2, theta2, theta_fit)
            

            theta_sol = fsolve(func, 1.3)
            print(theta_sol)
            # print("x: %4.3f" % (x))
            
            f = open("out_theta_time.txt", "a")
            f.write("%4.6f"  % (t))
            f.write("\t")
            f.write("%4.6f"  % (theta_sol))
            f.write("\t")
            f.write("\n")

f.close()