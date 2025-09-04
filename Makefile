.PHONY: verify

T ?=

ECHIDNA_ARG := $(if $(strip $(T)),--sym-exec-target $(T))
HEVM_ARG    := $(if $(strip $(T)),--match $(T))

verify:
	@mkdir -p logs
	echidna . --contract CryticABDKMath64x64Properties --config test/verify.yaml $(T_ARG) | tee logs/verify-echidna.log

verify-hevm:
	@mkdir -p logs
	@forge clean #2> /dev/null
	@forge build --ast #2> /dev/null
	hevm test --debug $(HEVM_ARG) | tee logs/verify-hevm.log

fuzz:
	@mkdir -p logs
	echidna . --contract CryticABDKMath64x64Properties --config test/fuzz.yaml --timeout 3600 --workers 8 | tee logs/fuzz.log
