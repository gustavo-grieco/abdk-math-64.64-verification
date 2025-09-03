.PHONY: verify

# Allows to pass a target to verify, e.g. make verify T=check_mul
TARGET ?=
ifneq ($(TARGET),)
    T_ARG = --sym-exec-target $(TARGET)
endif

verify:
	@mkdir -p logs
	echidna . --contract CryticABDKMath64x64Properties --config test/verify.yaml $(T_ARG) | tee logs/verify.log

fuzz:
	@mkdir -p logs
	echidna . --contract CryticABDKMath64x64Properties --config test/fuzz.yaml --timeout 3600 --workers 8 | tee logs/fuzz.log
