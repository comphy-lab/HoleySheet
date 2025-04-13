# To get facets for bubbles in sheets # Add theta point as well.

import numpy as np
import os
import subprocess as sp
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.ticker import StrMethodFormatter
import sys
from scipy.optimize import fsolve

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['text.usetex'] = True
# matplotlib.rcParams['text.latex.preamble'] = [r'']

def gettingFacets1(filename):
    exe = ["./getFacet1", filename]
    p = sp.Popen(exe, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    temp1 = stderr.decode("utf-8")
    temp2 = temp1.split("\n")
    segs = []
    skip = False
    if (len(temp2) > 1e2):
        for n1 in range(len(temp2)):
            temp3 = temp2[n1].split(" ")
            if temp3 == ['']:
                skip = False
                pass
            else:
                if not skip:
                    temp4 = temp2[n1+1].split(" ")
                    r1, z1 = np.array([float(temp3[1]), float(temp3[0])])
                    r2, z2 = np.array([float(temp4[1]), float(temp4[0])])
                    ##segs.append((r1,z1))
                    segs.append(((r1, z1),(r2, z2)))
                    segs.append(((-r1, z1),(-r2, z2)))
                    segs.append(((r1, -z1),(r2, -z2)))
                    segs.append(((-r1, -z1),(-r2, -z2)))
                    skip = True
    return segs

def gettingFacets2(filename):
    exe = ["./getFacet2", filename]
    p = sp.Popen(exe, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    temp1 = stderr.decode("utf-8")
    temp2 = temp1.split("\n")
    segs = []
    skip = False
    if (len(temp2) > 1e2):
        for n1 in range(len(temp2)):
            temp3 = temp2[n1].split(" ")
            if temp3 == ['']:
                skip = False
                pass
            else:
                if not skip:
                    temp4 = temp2[n1+1].split(" ")
                    r1, z1 = np.array([float(temp3[1]), float(temp3[0])])
                    r2, z2 = np.array([float(temp4[1]), float(temp4[0])])
                    ##segs.append((r1,z1))
                    segs.append(((r1, z1),(r2, z2)))
                    segs.append(((-r1, z1),(-r2, z2)))
                    segs.append(((r1, -z1),(r2, -z2)))
                    segs.append(((-r1, -z1),(-r2, -z2)))
                    skip = True
    return segs

def gettingfield(filename, zmin, zmax, rmax, nr, Ohs, Ohp, Oha):
    exe = ["./getData", filename, str(zmin), str(0), str(zmax), str(rmax), str(nr), str(Ohs), str(Ohp), str(Oha)]
    p = sp.Popen(exe, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    temp1 = stderr.decode("utf-8")
    temp2 = temp1.split("\n")
    # print(temp2) #debugging
    Rtemp, Ztemp, D2temp, veltemp, Utemp, Vtemp, taupTemp = [],[],[],[],[],[],[]

    for n1 in range(len(temp2)):
        temp3 = temp2[n1].split(" ")
        if temp3 == ['']:
            pass
        else:
            Ztemp.append(float(temp3[0]))
            Rtemp.append(float(temp3[1]))
            D2temp.append(float(temp3[2]))
            veltemp.append(float(temp3[3]))
            Utemp.append(float(temp3[4]))
            Vtemp.append(float(temp3[5]))
            taupTemp.append(float(temp3[6]))

    R = np.asarray(Rtemp)
    Z = np.asarray(Ztemp)
    D2 = np.asarray(D2temp)
    vel = np.asarray(veltemp)
    U = np.asarray(Utemp)
    V = np.asarray(Vtemp)
    taup = np.asarray(taupTemp)
    nz = int(len(Z)/nr)

    # print("nr is %d %d" % (nr, len(R))) # debugging
    print("nz is %d" % nz)

    R.resize((nz, nr))
    Z.resize((nz, nr))
    D2.resize((nz, nr))
    vel.resize((nz, nr))
    U.resize((nz, nr))
    V.resize((nz, nr))
    taup.resize((nz, nr))

    return R, Z, D2, vel, U, V, taup, nz
# ----------------------------------------------------------------------------------------------------------------------

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



nGFS = 5000
Ldomain = 4
GridsPerR = 64
nr = int(GridsPerR*Ldomain)
Ohs, Ohp, Oha = 1e-2, 1e-2, 1e-4

rmin, rmax, zmin, zmax = [-Ldomain, Ldomain, -Ldomain/2, Ldomain/2]
lw = 2

folder = 'Video_02.1'  # output folder
if not os.path.isdir(folder):
    os.makedirs(folder)

for ti in range(nGFS):
    t = 0.1*ti
    place = "intermediate/snapshot-%5.4f" % t
    name = "%s/%8.8d.png" %(folder, int(t*1000))

    if not os.path.exists(place):
        print("%s File not found!" % place)
    else:
        if os.path.exists(name):
            print("%s Image present!" % name)
        else:
            segs1 = gettingFacets1(place)
            segs2 = gettingFacets2(place)
            if (len(segs1) == 0):
                print("Problem in the available file %s" % place)
            else:

                #R, Z, taus, vel, U, V, taup, nz = gettingfield(place, zmin, zmax, rmax, nr, Ohs, Ohp, Oha)
                
                #zminp, zmaxp, rminp, rmaxp = Z.min(), Z.max(), R.min(), R.max()

                # print(zminp, zmaxp, rminp, rmaxp)

                # Part to plot
                AxesLabel, TickLabel = [50, 35]
                fig, ax = plt.subplots()
                fig.set_size_inches(19.20, 10.80)

                ax.plot([0, 0], [zmin, zmax],'-.',color='grey',linewidth=lw)

                ax.plot([rmin, rmin], [zmin, zmax],'-',color='black',linewidth=lw)
                ax.plot([rmin, rmax], [zmin, zmin],'-',color='black',linewidth=lw)
                ax.plot([rmin, rmax], [zmax, zmax],'-',color='black',linewidth=lw)
                ax.plot([rmax, rmax], [zmin, zmax],'-',color='black',linewidth=lw)

                ## Drawing Facets
                line_segments1 = LineCollection(segs1, linewidths=3.25, colors='green', linestyle='solid')
                line_segments2 = LineCollection(segs2, linewidths=3.25, colors='purple', linestyle='solid')
                ax.add_collection(line_segments1)
                ax.add_collection(line_segments2)
                ax.set_title('$t/\\tau_\gamma$ = %4.3f' % t, fontsize=TickLabel)
                #plt.scatter(segs[0], segs[1])
                #print("The line collection array: ",segs)

                x1, y1, theta1 = getting_facet1(place) 
                x2, y2, theta2 = getting_facet2(place) 
                r1 = np.sqrt(x1*x1+y1*y1)
                r2 = np.sqrt(x2*x2+y2*y2) 
                theta_fit = np.linspace(0, np.pi/2, 1000)
                r_fit1 = fitradius(r1, theta1, theta_fit)
                r_fit2 = fitradius(r2, theta2, theta_fit)
                

                theta_sol = fsolve(func, 1.3)
                print(theta_sol)
                theta_sol[theta_sol < 0] = 0
                f = open("out_theta_time.txt", "a")
                f.write("%4.6f"  % (t))
                f.write("\t")
                f.write("%4.6f"  % (theta_sol))
                f.write("\t")
                f.write("\n")
            
                # Add lines
                theta_x_line = np.linspace(0, 2, 100)
                theta_y_line = theta_x_line / np.tan(theta_sol)
                ax.plot(theta_x_line, theta_y_line, color='black')
                ## Copied Lines
                ax.set_aspect('equal')
                ax.set_xlim(rmin, rmax)
                ax.set_ylim(zmin, zmax)

                ax.axis('off')
                # plt.show()
                plt.savefig(name, bbox_inches="tight", dpi=250)
                plt.close()
f.close()