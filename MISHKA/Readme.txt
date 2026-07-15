*MISHIKA-1 file list

src : source file of MISHKA
lib : all other dependent libraries except libblas

namelist, output, mapping, plot : store input and output files


*Compile MISHIKA:

$ make

If successful, an executable 'mishika.exe' will be automatically generated

For reproducible operator traces in double precision, use

$ make clean
$ make MISHKA_REAL8=1

This opt-in build promotes MISHKA's default REAL and COMPLEX data and all of
its bundled LINPACK routines.  A small adapter maps the historical SCOPY,
SSCAL, CCOPY, CSCAL, CAXPY, CDOTC, CDOTU, SCASUM, and ICAMAX calls to the
corresponding double-precision BLAS routines.  The default build and its
single-precision ABI are unchanged when MISHKA_REAL8 is unset.

For a slower quadruple-precision diagnostic trace, use

$ make clean
$ make MISHKA_REAL16=1

This build uses explicit REAL(16)/COMPLEX(32) loops for the same historical
BLAS entry points.  MISHKA_REAL8 and MISHKA_REAL16 are mutually exclusive;
each option must be 1 or unset.  The trace records the actual storage widths.
Trace accumulation uses at least double precision and never downcasts a
quadruple build.  The eigenvector written for diagnostics is cleaned through a
temporary copy, so suppressing tiny printed values cannot alter the solved
vector or its subsequent residual trace.  Run `make check-real16-blas` for a
deterministic unit check of every compatibility entry point.

NOTE: gfortran and blas library is required. (Included in PRL_PTM virtual machines)
If you don't have them, you can install gfortran and blas library by

$ sudo apt-get install gfortran
$ sudo apt-get install libblas-dev


*Run MISHIKA:

1. copy mapping file from HELENA mapping directory into 'mapping' under this directory
2. make the namelist and store it into 'namelist' under this directory
3. run MISHIKA

$ ./runmis mappingfile namelistfile

for example,

$ ./runmis he18696_290_10a mi18696_290_10a_1

NOTE: This version of MISHIKA do not have any modification.

