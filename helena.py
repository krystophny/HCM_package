from pickle import TRUE
import os
import numpy as np
import matplotlib.pyplot as plt
import f90nml

class Helena:
    keywords0D = ['MAGNETIC AXIS :', 'POLOIDAL BETA :', 'TOROIDAL BETA :', 'BETA STAR     :', 'NORM. BETA    :',
                'TOTAL CURRENT :', 'TOTAL AREA    :', 'TOTAL VOLUME  :', 'INT. INDUCTANCE :', 'POL. FLUX     :',
                 'A,B,C         :']

    varwords0D = ['magnetic_axis', 'poloidal_beta', 'toroidal_beta', 'beta_star', 'norm_beta',
                'total_current', 'total_area', 'total_volume', 'inductance', 'poloidal_flux', 'abc']

    keywords1D = [' QS', ' P0', ' RBPHI']

    varwords1D = ['q', 'pressure', 'F']

    def __init__(self, helena_path):
      """Set the HELENA running path
      """
      self._helena_path = helena_path
      # check the existence
      if not os.path.exists(helena_path):
        raise FileNotFoundError('The specified HELENA path cannot be found')

      self._namelist_dir = os.path.join(helena_path, 'namelist')
      self._output_dir = os.path.join(helena_path, 'output')
      self._mappint_dir = os.path.join(helena_path, 'mapping')
      self._runhel_dir = os.path.join(helena_path, 'runhel')

    def read_namelist(self, namelist_name):
      """Read a namelist of HELENA"""
      namelist_fullpath = os.path.join(self._namelist_dir, namelist_name)
      # Read in the file
      with open(namelist_fullpath, 'r') as file:
        filedata = file.read()

      # Replace the target string
      filedata = filedata.replace('&END', '/')

      self._namelist_name = namelist_name
      self._namelist_fullpath = namelist_fullpath

      # Write the file out again
      with open(namelist_fullpath, 'w') as file:
        file.write(filedata)

      self.namelist = f90nml.read(namelist_fullpath)

    def print_namelist(self):
        print(self.namelist)

    def run(self, namelist_name = None):
      import subprocess
      if namelist_name is None:
        if self.namelist is None:
          raise FileNotFoundError("Please specify namelist file")
        else:
          print("Will run namelist " + self._namelist_name)
      else:
        self.read_namelist(namelist_name)

      self._runname = self._namelist_name + 'py'
      namelistrun_fullpath = os.path.join(self._namelist_dir, self._runname)
      self.namelist.write(namelistrun_fullpath, force=True)
      os.chdir(self._helena_path)
      subprocess.run(["./runhel", self._runname], capture_output=True)
      self.read_output(self._runname)


    def read_output(self, filename):
        """Read a Helena output
        """

        filename_fullpath = os.path.join(self._output_dir, filename)

        if not os.path.exists(filename_fullpath):
            raise FileNotFoundError()

        with open(filename_fullpath, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break

                for i in range(len(self.keywords0D)):
                    if self.keywords0D[i] in line:
                        item = list(map(float, line.split(':')[1].split()))
                        if len(item) == 1:
                            setattr(self, self.varwords0D[i], item[0])
                        else:
                            setattr(self, self.varwords0D[i], np.array(item))

                for i in range(len(self.keywords1D)):
                    if self.keywords1D[i] in line:
                        profile_data = []
                        while True:
                            line = f.readline()
                            linedata = list(map(float, line.split()))
                            if len(linedata) == 0:
                                break
                            else:
                                profile_data = profile_data + linedata
                        setattr(self, self.varwords1D[i], np.array(profile_data))
        self.s = np.linspace(0, 1, self.q.size, True)

        gridname = filename + '.grid'
        gridname_fullpath = os.path.join(self._output_dir, gridname)


        if os.path.exists(gridname_fullpath):

            with open(gridname_fullpath, 'r') as fgrid:
                firstline = fgrid.readline()
                ias, ns, nt = map(int, firstline.split())

                rgrid = np.zeros([ns, nt], dtype=np.float64)
                zgrid = np.zeros([ns, nt], dtype=np.float64)

                for i in range(ns):
                    for j in range(nt):
                        line = fgrid.readline()
                        xtext, ytext = line.split()
                        rgrid[i,j] = float(xtext)
                        zgrid[i,j] = float(ytext)

            self.ns = ns
            self.nt = nt
            self.ias = ias
            self.rgrid = rgrid
            self.zgrid = zgrid


        axisprof_name = filename + '.axisprof'
        axisprof_fullpath = os.path.join(self._output_dir, axisprof_name)

        if os.path.exists(axisprof_fullpath):

            with open(axisprof_fullpath, 'r') as faxiprof:
                firstline = faxiprof.readline()
                alldatalist = []
                for line in faxiprof:
                    datalist = list(map(float, line.split()))
                    if len(datalist) == 5:
                        alldatalist.append(datalist)

                alldatalist = np.array(alldatalist)

            self.xaxisprof = alldatalist[:,0]
            self.psiaxisprof = alldatalist[:,1]
            self.paxisprof = alldatalist[:,2]
            self.qaxisprof = alldatalist[:,3]
            self.curaxisprof = alldatalist[:,4]


    def __str__(self) -> str:
        strout = 'HELENA equilibrium\n'
        for i in range(len(self.keywords0D)):
            strout = strout + self.keywords0D[i] + str(getattr(self, self.varwords0D[i])) + '\n'

        return strout

    def plot_grid(self, ns_skip = 0):
        if self.ias == 0:
            for i in range(0, self.ns, ns_skip+1):
                plt.plot(self.rgrid[i, :], self.zgrid[i, :], 'b', linewidth=0.5)
                plt.plot(np.flip(self.rgrid[i, :]), np.flip(-self.zgrid[i, :]), 'b', linewidth=0.5)

        plt.axis('equal')
        plt.xlabel('x')
        plt.ylabel('y')

    def plot_pressure(self, xaxis_psi=False):
        """
        Plot the pressure profile
        @params
        xaxis_psi - use psi as the x axis, default False
        """

        if xaxis_psi:
            plt.plot(self.s**2, self.pressure)
            plt.xlabel(r"$\Psi$")
            plt.ylabel('p')
        else:
            plt.plot(self.s, self.pressure)
            plt.xlabel("s")
            plt.ylabel('p')

    def plot_q(self, xaxis_psi=False):
        """
        Plot the q profile
        @params
        xaxis_psi - use psi as the x axis, default False
        """

        if xaxis_psi:
            plt.plot(self.s**2, self.q)
            plt.xlabel(r"$\Psi$")
            plt.ylabel('q')
        else:
            plt.plot(self.s, self.q)
            plt.xlabel("s")
            plt.ylabel('q')

    def plot_F(self, xaxis_psi=False):
        """
        Plot the F profile
        @params
        xaxis_psi - use psi as the x axis, default False
        """

        if xaxis_psi:
            plt.plot(self.s**2, self.F)
            plt.xlabel(r"$\Psi$")
            plt.ylabel('F')
        else:
            plt.plot(self.s, self.F)
            plt.xlabel("s")
            plt.ylabel('F')

    def plot_axisprof(self):
        """
        Plot the profiles on the midplane
        """
        plt.subplot(221)
        plt.plot(self.xaxisprof, self.psiaxisprof)
        plt.xlabel('x')
        plt.ylabel(r"$\Psi$")
        plt.subplot(222)
        plt.plot(self.xaxisprof, self.qaxisprof)
        plt.xlabel('x')
        plt.ylabel('q')
        plt.subplot(223)
        plt.plot(self.xaxisprof, self.paxisprof)
        plt.xlabel('x')
        plt.ylabel('p')
        plt.subplot(224)
        plt.plot(self.xaxisprof, self.curaxisprof)
        plt.xlabel('x')
        plt.ylabel(r"$<J_\varphi>$")
