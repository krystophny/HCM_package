FC = gfortran
LIBS = -llapack -lblas
TITLE = helcode.exe
OPTS = -g -fbacktrace -ffpe-trap=invalid,zero,overflow -fdefault-real-8 -fallow-argument-mismatch
OBJS = hel12a.o ppplib.o

all: $(OBJS)
	$(FC) -o $(TITLE) $(OBJS) $(LIBS) $(OPTS)
	rm *.mod
hel12a.o: hel12a.f
	$(FC) -c -o hel12a.o hel12a.f $(OPTS)
ppplib.o: ppplib.f
	$(FC) -c -o ppplib.o ppplib.f $(OPTS)
clean:
	rm $(OBJS) $(TITLE)
cleanall:
	rm $(OBJS) $(TITLE) ./output/* ./plot/* ./mapping/*
