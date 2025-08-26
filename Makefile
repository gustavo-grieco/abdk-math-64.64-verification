.PHONY: verify

verify:
	@mkdir -p logs
	echidna . --contract CryticABDKMath64x64Properties --config test/echidna.yaml | tee logs/echidna.log