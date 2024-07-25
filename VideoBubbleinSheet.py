# To get facets for bubbles in sheets

import numpy as np
import os
import subprocess as sp
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import multiprocessing as mp
from functools import partial
from pathlib import Path
import argparse

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['text.usetex'] = True
# matplotlib.rcParams['text.latex.preamble'] = [r'']

def gettingFacets(filename, asy):
    exe = ["./getFacet", filename]
    p = sp.Popen(exe, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout, stderr = p.communicate()
    stderr_output = stderr.decode("utf-8")
    points = stderr_output.split("\n")
    segments = []

    if len(points) > 100:
        for i in range(len(points) - 1):
            current_point = points[i].split()
            if current_point:
                next_point = points[i + 1].split()
                if next_point:
                    r1, z1 = float(current_point[1]), float(current_point[0])
                    r2, z2 = float(next_point[1]), float(next_point[0])
                    if asy:
                        segment_variants = [
                                ((r1, z1), (r2, z2)),
                                ((-r1, z1), (-r2, z2))
                            ]    
                    else:    
                        segment_variants = [
                            ((r1, z1), (r2, z2)),
                            ((-r1, z1), (-r2, z2)),
                            ((r1, -z1), (r2, -z2)),
                            ((-r1, -z1), (-r2, -z2))
                        ]
                    
                    segments.extend(segment_variants)
    return segments

# def gettingfield(filename, zmin, zmax, rmax, nr, Ohs, Ohp, Oha):
#     exe = ["./getData", filename, str(zmin), str(0), str(zmax), str(rmax), str(nr), str(Ohs), str(Ohp), str(Oha)]
#     p = sp.Popen(exe, stdout=sp.PIPE, stderr=sp.PIPE)
#     stdout, stderr = p.communicate()
#     temp1 = stderr.decode("utf-8")
#     temp2 = temp1.split("\n")
#     # print(temp2) #debugging
#     Rtemp, Ztemp, D2temp, veltemp, Utemp, Vtemp, taupTemp = [],[],[],[],[],[],[]

#     for n1 in range(len(temp2)):
#         temp3 = temp2[n1].split(" ")
#         if temp3 == ['']:
#             pass
#         else:
#             Ztemp.append(float(temp3[0]))
#             Rtemp.append(float(temp3[1]))
#             D2temp.append(float(temp3[2]))
#             veltemp.append(float(temp3[3]))
#             Utemp.append(float(temp3[4]))
#             Vtemp.append(float(temp3[5]))
#             taupTemp.append(float(temp3[6]))

#     R = np.asarray(Rtemp)
#     Z = np.asarray(Ztemp)
#     D2 = np.asarray(D2temp)
#     vel = np.asarray(veltemp)
#     U = np.asarray(Utemp)
#     V = np.asarray(Vtemp)
#     taup = np.asarray(taupTemp)
#     nz = int(len(Z)/nr)

#     # print("nr is %d %d" % (nr, len(R))) # debugging
#     print("nz is %d" % nz)

#     R.resize((nz, nr))
#     Z.resize((nz, nr))
#     D2.resize((nz, nr))
#     vel.resize((nz, nr))
#     U.resize((nz, nr))
#     V.resize((nz, nr))
#     taup.resize((nz, nr))

#     return R, Z, D2, vel, U, V, taup, nz
# ----------------------------------------------------------------------------------------------------------------------


def process_timestep(ti, folder, nGFS, Ldomain, GridsPerR, rmin, rmax, zmin, zmax, lw, asy):
    """Process a single timestep."""
    t = 0.1*ti
    snapshot_file = Path(f"intermediate/snapshot-{t:.4f}")
    output_file = folder / f"{int(t * 1000):08d}.png"

    if not snapshot_file.exists():
        print(f"{snapshot_file} not found!")
        return
    
    if output_file.exists():
        print(f"{output_file} already present!")
        return
    
    segs = gettingFacets(snapshot_file, asy)
    
    if not segs:
        print(f"Problem in the available file {snapshot_file}")
        return

    # R, Z, taus, vel, U, V, taup, nz = gettingfield(place, zmin, zmax, rmax, nr, Ohs, Ohp, Oha)
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
    line_segments = LineCollection(segs, linewidths=3.25, colors='green', linestyle='solid')
    ax.add_collection(line_segments)
    ax.set_title('$t/\\tau_\gamma$ = %4.3f' % t, fontsize=TickLabel)
    #plt.scatter(segs[0], segs[1])
    #print("The line collection array: ",segs)

    ## Copied Lines
    ax.set_aspect('equal')
    ax.set_xlim(rmin, rmax)
    ax.set_ylim(zmin, zmax)

    ax.axis('off')
    # plt.show()
    plt.savefig(output_file, bbox_inches="tight", dpi=250)
    plt.close()
    print(f"{ti+1} is done")

def main():
    parser = argparse.ArgumentParser(description="Process facets for bubbles in sheets.")
    parser.add_argument('--asy', action='store_true', 
                        help="If set, use asymmetric variants. Default is false.")
    args = parser.parse_args()
    
    nGFS = 100
    Ldomain = 4
    GridsPerR = 64
    nr = int(GridsPerR*Ldomain)

    rmin, rmax, zmin, zmax = -Ldomain, Ldomain, -Ldomain/2, Ldomain/2
    lw = 2

    folder = Path('Video')  # output folder

    if not folder.is_dir():
        os.makedirs(folder)
    
    # Prepare the partial function with fixed arguments
    process_func = partial(process_timestep, folder=folder, nGFS=nGFS, Ldomain=Ldomain, GridsPerR=GridsPerR, rmin=rmin, rmax=rmax, zmin=zmin, zmax=zmax, lw=lw, asy=args.asy)

    # Use all available CPU cores
    num_processes = 8 #mp.cpu_count()
    
    # Create a pool of worker processes
    with mp.Pool(processes=num_processes) as pool:
        # Map the process_func to all timesteps
        pool.map(process_func, range(nGFS))

if __name__ == "__main__":
    main()