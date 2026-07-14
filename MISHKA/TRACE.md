# MISHKA operator trace

This branch writes a machine-readable operator trace to `fort.29` after a
successful inverse-iteration solve. The trace is diagnostic only: it is written
after the eigenvalue and boundary-condition diagnostics, and reconstructs local
matrices in the existing `ZMA` scratch array.

Build from the repository root with:

```sh
make -C HELENA
make -C MISHKA
```

Run HELENA and MISHKA in separate directories. Give each executable its input
as `fort.10`, then copy HELENA's `fort.12` into the MISHKA directory. MISHKA
produces the usual files plus `fort.29`.

The trace contains comma-separated records:

- `DIMENSIONS`, `EQUILIBRIUM`, and `MODE` describe the run.
- `PROFILE` gives the radial coordinate, safety factor, pressure, and toroidal
  field function at every HELENA mapping surface.
- `Q1_SELECTION` identifies the profile surface nearest `q = 1` and the MISHKA
  cell containing it.
- `QUADRATURE` gives the equilibrium quantities used at each Gaussian point in
  the selected axis, `q = 1`, and edge cells.
- `COEFFICIENT` gives each complex Fourier-spline coefficient and its radial
  derivative at those points.
- `MATRIX` gives every entry of the local stiffness (`A`) and mass (`B`)
  matrices in the same two-dimensional `ZMA` view used by the solver.
- `VECTOR` gives every component of the converged radial eigenvector.

The MISHKA build intentionally uses default `REAL` and `COMPLEX` kinds. This
matches the single-precision BLAS routines and the bundled MISHKA library ABI.
HELENA remains double precision. Floating-point traps and backtraces are enabled
in both programs; failure to open or close `fort.29` stops the run.
