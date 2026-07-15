ifneq ($(strip $(MISHKA_REAL8)),)
ifneq ($(MISHKA_REAL8),1)
$(error MISHKA_REAL8 must be 1 or unset)
endif
endif
ifneq ($(strip $(MISHKA_REAL16)),)
ifneq ($(MISHKA_REAL16),1)
$(error MISHKA_REAL16 must be 1 or unset)
endif
endif
ifeq ($(MISHKA_REAL8)$(MISHKA_REAL16),11)
$(error MISHKA_REAL8 and MISHKA_REAL16 are mutually exclusive)
endif

ifeq ($(MISHKA_REAL8),1)
MISHKA_PRECISION_FLAGS := -fdefault-real-8 -fdefault-double-8
else ifeq ($(MISHKA_REAL16),1)
MISHKA_PRECISION_FLAGS := -fdefault-real-16
else
MISHKA_PRECISION_FLAGS :=
endif
