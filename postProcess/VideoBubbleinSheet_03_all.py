# To get facets for bubbles in sheets

import numpy as np
import os
import subprocess as sp
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.ticker import StrMethodFormatter
import sys

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

def gettingFacets(filename):
    exe = ["./getFacet", filename]
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
# ----------------------------------------------------------------------------------------------------------------------


nGFS = 1000
Ldomain = 4
GridsPerR = 64
nr = int(GridsPerR*Ldomain)

rmin, rmax, zmin, zmax = [-Ldomain, Ldomain, -Ldomain/2, Ldomain/2]
lw = 2

folder = 'Video_all'  # output folder

if not os.path.isdir(folder):
    os.makedirs(folder)

for ti in range(nGFS):
    t = 0.1*ti
    place = "snapshot-%5.4f" % t
    place2 = "intermediate/snapshot-%5.4f" % 0e0
    name = "%s/%8.8d.png" %(folder, int(t*1000))

    if not os.path.exists(place):
        print("%s File not found!" % place)
    else:
        if os.path.exists(name):
            print("%s Image present!" % name)
        else:
            segs1 = gettingFacets1(place)
            segs2 = gettingFacets2(place)
            segs = gettingFacets(place2)
            if (len(segs1) == 0):
                print("Problem in the available file %s" % place)
            else:

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
                line_segments3 = LineCollection(segs, linewidths=1.25, colors='black', linestyle='solid')
                ax.add_collection(line_segments1)
                ax.add_collection(line_segments2)
                ax.add_collection(line_segments3)
                ax.set_title('$t/\\tau_\gamma$ = %4.3f' % t, fontsize=TickLabel)
                #plt.scatter(segs[0], segs[1])
                #print("The line collection array: ",segs)

                ## Copied Lines
                ax.set_aspect('equal')
                ax.set_xlim(rmin, rmax)
                ax.set_ylim(zmin, zmax)

                ax.axis('off')
                # plt.show()
                plt.savefig(name, bbox_inches="tight", dpi=250)
                plt.close()
