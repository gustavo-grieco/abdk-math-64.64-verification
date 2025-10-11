.PHONY: verify

T ?=

ECHIDNA_ARG := $(if $(strip $(T)),--sym-exec-target $(T))
HEVM_ARG    := $(if $(strip $(T)),--match $(T))

verify: verify-echidna

verify-echidna:
	@mkdir -p logs
	echidna . --contract CryticABDKMath64x64Properties --config test/verify.yaml $(ECHIDNA_ARG) | tee logs/verify-echidna.log

verify-hevm:
	@mkdir -p logs
	@forge clean 2> /dev/null
	@forge build --ast 2> /dev/null
	hevm test --max-buf-size 12 --debug --loop-detection-heuristic Naive --max-iterations 65 --max-depth 70 --solver bitwuzla $(HEVM_ARG) | tee logs/verify-hevm.log

fuzz:
	@mkdir -p logs
	echidna . --contract CryticABDKMath64x64Properties --config test/fuzz.yaml --workers 8 #| tee logs/fuzz.log
