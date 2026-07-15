ifneq ($(strip $(MISHKA_REAL8)),)
ifneq ($(MISHKA_REAL8),1)
$(error MISHKA_REAL8 must be 1 or unset)
endif
endif

ifeq ($(MISHKA_REAL8),1)
MISHKA_PRECISION_FLAGS := -fdefault-real-8 -fdefault-double-8
else
MISHKA_PRECISION_FLAGS :=
endif
