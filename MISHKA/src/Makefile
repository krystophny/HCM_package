TITLE = mishka.exe
POSITION = ../
OBJS = mishka1.o
MISLIB = $(POSITION)mishkalib.a
LIBS = -lblas $(MISLIB)
OPTS = -g -fbacktrace -ffpe-trap=invalid,zero,overflow -fallow-argument-mismatch
FC = gfortran
include ../precision.mk
OPTS += $(MISHKA_PRECISION_FLAGS)

ifeq ($(MISHKA_REAL8),1)
OBJS += precision_blas.o
else ifeq ($(MISHKA_REAL16),1)
OBJS += precision_blas_real16.o
endif

all : $(OBJS)
	$(FC) -o $(POSITION)$(TITLE) $(OBJS) $(LIBS) $(OPTS);


mishka1.o : pre
	./pre.exe <mishka1_info.source.f> mishka1.f;
	$(FC) $(OPTS) -c -o mishka1.o mishka1.f;

precision_blas.o : precision_blas.f
	$(FC) $(OPTS) -c -o precision_blas.o precision_blas.f;

precision_blas_real16.o : precision_blas_real16.f
	$(FC) $(OPTS) -c -o precision_blas_real16.o precision_blas_real16.f;

pre :
	$(FC) -o pre.exe pre.f

clean :
	rm -f *.o $(POSITION)$(TITLE) pre.exe;
