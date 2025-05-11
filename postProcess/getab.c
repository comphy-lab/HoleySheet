// get major axis a, and minor axis b of the bubble

#include "axi.h"
#include "navier-stokes/centered.h"
#include "fractions.h"

char filename[80], nameTrack[80];
scalar * list = NULL;
scalar f2[];

int main(int a, char const *arguments[])
{
  sprintf (filename, "%s", arguments[1]);

  restore (file = filename);
  boundary((scalar *){f2, u.x, u.y});

  double xmax = -HUGE;
  double ymax = -HUGE;
  double x_ymax = 0, y_xmax = 0;
  
  foreach(){
    if (x > xmax && f2[] > 1-1e-3)
      {
        xmax = x;
        y_xmax = y;
      }
    if (y > ymax && f2[] > 1-1e-3)
      {
        ymax = y;
        x_ymax = x;
      }
  }

  FILE * fp = ferr;
  fprintf(ferr, "%f %7.6e %7.6e %7.6e %7.6e\n", t,  xmax, y_xmax, x_ymax, ymax);
  fflush (fp);
  fclose (fp);
}