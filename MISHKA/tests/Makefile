FC = gfortran
FFLAGS := -g -fbacktrace -fcheck=all -ffpe-trap=invalid,zero,overflow
TEST_EXE := .precision_blas_real16_test.exe

.PHONY: check-real16-blas

check-real16-blas:
	@set -eu; \
	trap 'rm -f $(TEST_EXE)' EXIT; \
	$(FC) $(FFLAGS) -fdefault-real-16 \
		-o $(TEST_EXE) ../src/precision_blas_real16.f \
		precision_blas_real16_test.f90; \
	./$(TEST_EXE)
