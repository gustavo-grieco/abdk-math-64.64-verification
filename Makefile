.PHONY: verify

verify:
	@mkdir -p logs
	echidna . --contract CryticABDKMath64x64Properties --config test/verify.yaml | tee logs/verify.log

fuzz:
	@mkdir -p logs
	echidna . --contract CryticABDKMath64x64Properties --config test/fuzz.yaml --timeout 3600 --workers 8 | tee logs/fuzz.log
