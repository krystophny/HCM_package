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
- `Q1_SELECTION` identifies the profile surface nearest `q = 1` and its
  selected MISHKA cell.
- `INTERVAL_SELECTION` identifies eight strictly ordered trace cells: the
  cells nearest normalized poloidal radii 0.10, 0.25, 0.40, 0.55, 0.70, 0.85,
  and 0.95, plus the cell nearest `q = 1` between the 0.40 and 0.55 cells.
- `QUADRATURE` gives the equilibrium quantities used at each Gaussian point in
  every selected cell. The interior targets avoid treating a half-mesh sample
  as either the magnetic axis or plasma edge.
- `COEFFICIENT` gives each complex Fourier-spline coefficient and its radial
  derivative at those points.
- `MATRIX` gives every entry of the local stiffness (`A`) and mass (`B`)
  matrices in the same two-dimensional `ZMA` view used by the solver.
- `VECTOR` gives every component of the converged radial eigenvector.
- `RADIAL_DOF`, `BASIS_SAMPLE`, `AXIS_CONSTRAINT`, and `EDGE_CONSTRAINT`
  expose the cubic/quadratic scatter and the boundary slots actually used by
  the legacy assembly.
- `CELL_QUADRATIC` and `CELL_BLOCK` give the Hermitian and legacy-bilinear
  contributions of every radial cell. `TOTAL_QUADRATIC`, `TOTAL_BLOCK`, and
  `GLOBAL_RESIDUAL` independently audit the printed eigenpair. These
  diagnostic reductions use complex double precision; the solver and its ABI
  remain single precision.

For meshes with at most 101 radial nodes, `FULL_MATRIX` records also contain
every local matrix. Set `GLISS_MISHKA_FULL_MATRIX=1` to request those records
on a larger mesh. Any other nonempty value is rejected. Full-matrix output is
intended for bounded, scripted debugging in external storage, not for normal
regression artifacts.

Set `GLISS_MISHKA_ITER_RESIDUAL=1` to write a `GLISS_ITER_RESIDUAL` line to
`fort.20` after every shift-invert iteration. Each line contains the proposed
eigenvalue, norms of `A x`, `B x`, and `A x - lambda B x`, the normwise relative
residual, the residual-gate status and tolerance, and the radial node with the
largest residual block. Any other nonempty value is rejected.

Set `GLISS_MISHKA_RESIDUAL_TOL` to a finite number in `(0, 1]` to make that
residual a convergence requirement. The usual eigenvalue-correction test must
then pass together with the requested residual tolerance. If the iteration
limit is reached first, MISHKA exits with a nonzero status instead of emitting
an uncertified result. Setting the tolerance also enables the per-iteration
lines, so a failed run retains the evidence needed to locate the problem.

The MISHKA build intentionally uses default `REAL` and `COMPLEX` kinds. This
matches the single-precision BLAS routines and the bundled MISHKA library ABI.
HELENA remains double precision. Floating-point traps and backtraces are enabled
in both programs; failure to open or close `fort.29` stops the run.
