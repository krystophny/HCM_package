include precision.mk

.PHONY: all clean cleanoutput check-real16-blas

all: mishkalib.a
	cd src && $(MAKE) all; 
	echo make successful!;

mishkalib.a :
	cd lib && $(MAKE) all; 

clean:
	cd lib && $(MAKE) clean; 
	cd src && $(MAKE) clean;

cleanoutput:
	rm output/* plot/* tmp_mis/*;
	rmdir tmp_mis;

check-real16-blas:
	$(MAKE) -C tests check-real16-blas
