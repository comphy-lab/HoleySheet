// Bubbles inside a draining sheet. || Uses CLSVOF || Reduced film thickness || Viscocapillary time scale based formulation
// Id 1 is liquid pool, and Id 2 is Newtonian gas.

#include "axi.h"
#include "navier-stokes/centered.h"
#define FILTERED // Smear density and viscosity jumps

#include "two-phase-clsvof.h"
#include "integral.h"
scalar sigmaf[];
#include "distance.h"
// #include "two-phase.h"
// #include "navier-stokes/conserving.h"
// #include "tension.h"

#define tsnap (1e-2) // 0.001 only for some cases.

// Error tolerancs
#define fErr (1e-3)   // error tolerance in f1 VOF
#define KErr (1e-6)   // error tolerance in VoF curvature calculated using heigh function method (see adapt event)
#define VelErr (1e-3) // error tolerances in velocity -- Use 1e-2 for low Oh and 1e-3 to 5e-3 for high Oh/moderate to high J

#define Ldomain 4

int MAXlevel;
// Oh -> Solvent Ohnesorge number
// Oha -> air Ohnesorge number
// Bo -> Bond number = rhoR^3w^2/gamma
double Oh, Oha, Bo, tmax;
char nameOut[80], dumpFile[80];

// Boundary conditions
u.n[right] = dirichlet(-2 * Oh * pow(Bo,0.5) * x);
u.t[right] = dirichlet(Oh * pow(Bo,0.5) * y);
p[right] = dirichlet(0.);
pf[right] = dirichlet(0.);

u.n[top] = dirichlet(Oh * pow(Bo,0.5) * y);
u.t[top] = dirichlet(-2 * Oh * pow(Bo,0.5) * x);
p[top] = dirichlet(0.);
pf[top] = dirichlet(0.);

int main(int argc, char const *argv[])
{
    dtmax = 1e-5; //  BEWARE of this for stability issues.
    L0 = Ldomain;

    // Values taken from the terminal
    MAXlevel = atoi(argv[1]);
    Oh = atof(argv[2]);
    Bo = atof(argv[3]);
    tmax = atof(argv[4]);

    // Ensure that all the variables were transferred properly from the terminal or job script.
    if (argc < 5)
    {
        fprintf(ferr, "Lack of command line arguments. Check! Need %d more arguments\n", 5 - argc);
        return 1;
    }
    fprintf(ferr, "Level %d, Oh %2.1e, Bo %4.3f\n", MAXlevel, Oh, Bo);
    init_grid(1 << 7);
    // Create intermediate for all snapshots.
    char comm[80];
    sprintf(comm, "mkdir -p intermediate");
    system(comm);
    // Name of the restart file, used in writingFiles event.
    sprintf(dumpFile, "dump");

    rho1 = 1./(Oh*Oh), rho2 = 1e-3/(Oh*Oh);
    mu1 = 1., mu2 = 2e-2;

    // f.sigma = 1.0;
    d.sigmaf = sigmaf;

    run();
}

event init(t = 0)
{
    if (!restore(file = dumpFile))
    {
        // fraction(f, difference(1.5625 - x * x, 1 - x * x - y * y));
        foreach ()
        {
            d[] = -(1 - x*x - y*y);
            d[] = fabs(x) > 1.07 ? -d[] : d[];
            sigmaf[] = 1.;
            u.x[] = -2 * Bo * x;
            u.y[] = Bo * y;
        }
        boundary({f, u});
    }
    // return 1;
}

event adapt(i++)
{
    // scalar KAPPA[];
    // curvature(f, KAPPA);
    adapt_wavelet((scalar *){f, u.x, u.y},
                  (double[]){fErr, VelErr, VelErr}, MAXlevel, MAXlevel - 3);
}

// Dumping snapshots
event writingFiles(t = 0; t += tsnap; t <= tmax)
{
    dump(file = dumpFile);
    sprintf(nameOut, "intermediate/snapshot-%5.4f", t);
    dump(file = nameOut);
}

// Ending Simulation
event end(t = end)
{
}

// Log writing
event logWriting(i++)
{
    double ke = 0.;
    foreach (reduction(+ : ke))
    {
        ke += (2 * pi * y) * (0.5 * rho(f[]) * (sq(u.x[]) + sq(u.y[]))) * sq(Delta);
    }
    static FILE *fp;
    if (pid() == 0)
    {
        if (i == 0)
        {
            fprintf(ferr, "i dt t ke\n");
            fp = fopen("log", "w");
            fprintf(fp, "Level %d, Oh %2.1e, Bo %4.3f\n", MAXlevel, Oh, Bo);
            fprintf(fp, "i dt t ke\n");
        }
        else
        {
            fp = fopen("log", "a");
            fprintf(fp, "%d %g %g %g\n", i, dt, t, ke);
        }
        fprintf(fp, "%d %g %g %g\n", i, dt, t, ke);
        fclose(fp);
        fprintf(ferr, "%d %g %g %g\n", i, dt, t, ke);
    }

    assert(ke > -1e-10);
    assert(ke < 1e3);

    if ((ke > 1e3 || ke < 1e-6) && i > 1e1 && pid() == 0)
    {
        const char *message = ke > 1e3 ? "The kinetic energy blew up. Stopping simulation\n"
                                       : "kinetic energy too small now! Stopping!\n";
        fprintf(ferr, "%s", message);
        fp = fopen("log", "a");
        fprintf(fp, "%s", message);
        fclose(fp);
        dump(file = dumpFile);
        return 1;
    }
}
