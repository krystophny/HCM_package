include precision.mk

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
