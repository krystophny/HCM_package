TITLE = mishkalib.a
POSITION = ../
OBJS = cbal.o cdiv.o comqr.o corth.o cpoco.o cpofa.o cposl.o csroot.o pythag.o sgtsl.o ppplib.o
FC = gfortran
FFLAGS=-fallow-argument-mismatch
include ../precision.mk
FFLAGS += $(MISHKA_PRECISION_FLAGS)

all : $(OBJS)
	ar r $(POSITION)$(TITLE) $(OBJS);

cbal.o :
cdiv.o :
comqr.o :
corth.o :
cpoco.o :
cpofa.o :
cposl.o :
csroot.o :
pythag.o :
sgtsl.o :
ppplib.o :


clean :
	rm -f *.o $(POSITION)$(TITLE);
