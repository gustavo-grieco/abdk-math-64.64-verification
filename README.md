# The Great Verification of ABDK Math 64.64

This repository contains the on-going effort of verifying the important mathematical properties implemented by the [ABDK Math 64x64](https://github.com/abdk-consulting/abdk-libraries-solidity) using [Echidna](https://github.com/crytic/echidna) (powered by [hevm](https://github.com/ethereum/hevm/)). The invariants were directly extracted from the [crytic-properties repository](https://github.com/crytic/properties/tree/main/contracts/Math/ABDKMath64x64). 

## Status

Currently, the following test were fully verified or were fully explored without finding any counter examples:

| Invariant | Result |
| ----- | :---: |
| sub\_test\_non\_commutative(int128,int128) | ✅ |
| neg\_test\_identity(int128) | ✅ |
| sub\_test\_equivalence\_to\_addition(int128,int128) | ✅ |
| abs\_test\_negative(int128) | ✅ |
| div\_test\_values(int128,int128) | 👍 |
| inv\_test\_division(int128) | ✅ |
| abs\_test\_positive(int128) | ✅ |
| sqrt\_test\_negative(int128) | ✅ |
| sub\_test\_identity(int128) | ✅ |
| div\_test\_range(int128,int128) | ✅ |
| abs\_test\_subadditivity(int128,int128) | ✅ |
| inv\_test\_values(int128) | ✅ |
| add\_test\_commutative(int128,int128) | ✅ |
| mul\_test\_identity(int128) | ✅ |
| avg\_test\_one\_value(int128) | ✅ |
| add\_test\_associative(int128,int128,int128) | ✅ |
| add\_test\_identity(int128) | ✅ |
| avg\_test\_values\_in\_range(int128,int128) | ✅ |
| div\_test\_division\_num\_zero(int128) | ✅ |
| avg\_test\_operand\_order(int128,int128) | ✅ |
| div\_test\_division\_identity(int128) | ✅ |
| sub\_test\_neutrality(int128,int128) | ✅ |
| neg\_test\_double\_negation(int128) | ✅ |
| inv\_test\_sign(int128) | ✅ |
| div\_test\_negative\_divisor(int128,int128) | 👍 |
| div\_test\_maximum\_numerator(int128) | ✅ |

When a test is explored using the symbolic engine in verification mode, there a few possible results:

* **Verified** ✅ The code was fully explored, without any issues on the translation or during solving. As expected, no counterexamples.
* **Passed**  👍 The code was fully explored without detecting any counterexamples, but the SMT solver cannot determine the answer to some of the queries (e.g. it timed out), so the assertion could still fail.
* **Failed** 💥 The exploration revealed a counterexample that was successfully replayed in concrete mode.
* **Error** ❌ A bug or a missing feature blocks the exploration or solving of some paths.
* **Timeout** ⏳ There are scalability issues preventing the creation of the model to explore all the program paths. 

In the case of `div\_test\_values(int128,int128)` and `div\_test\_negative\_divisor(int128,int128)`, there are timeout when solving some SMT constraints. Using different [SMTs solvers could work](https://github.com/ethereum/hevm/issues/709#issuecomment-2833348972). 

The following invariants are in the process of verification but most of them will require aggresive [state merging implemented in hevm](https://github.com/ethereum/hevm/issues/763) in order to be verified in a reasonable time. 

| Invariant | Result |
| ----- | :---: |
| mul\_test\_associative(int128, int128, int128) | ❓ |
| mul\_test\_distributive(int128, int128, int128) | ❓ |
| mul\_test\_values(int128, int128) | ❓ |
| abs\_test\_multiplicativeness(int128, int128) | ❓ |
| inv\_test\_double\_inverse(int128) | ❓ |
| inv\_test\_division\_noncommutativity(int128, int128) | ❓ |
| inv\_test\_multiplication(int128, int128) | ❓ |
| inv\_test\_identity(int128) | ❓ |
| gavg\_test\_values\_in\_range(int128, int128) | ❓ |
| gavg\_test\_operand\_order(int128, int128) | ❓ |
| pow\_test\_zero\_exponent(int128) | ❓ |
| pow\_test\_zero\_base(uint256) | ❓ |
| pow\_test\_one\_exponent(int128) | ❓ |
| pow\_test\_base\_one(uint256) | ❓ |
| pow\_test\_product\_same\_base(int128, uint256, uint256) | ❓ |
| pow\_test\_power\_of\_an\_exponentiation(int128, uint256, uint256) | ❓ |
| pow\_test\_distributive(int128, int128, uint256) | ❓ |
| pow\_test\_values(int128, uint256) | ❓ |
| pow\_test\_sign(int128, uint256) | ❓ |
| pow\_test\_maximum\_base(uint256) | ❓ |
| pow\_test\_high\_exponent(int128, uint256) | ❓ |
| sqrt\_test\_inverse\_mul(int128) | ❓ |
| sqrt\_test\_inverse\_pow(int128) | ❓ |
| sqrt\_test\_distributive(int128, int128) | ❓ |
| log2\_test\_distributive\_mul(int128, int128) | ❓ |
| log2\_test\_power(int128, uint256) | ❓ |
| log2\_test\_negative(int128) | ❓ |
| ln\_test\_distributive\_mul(int128, int128) | ❓ |
| ln\_test\_power(int128, uint256) | ❓ |
| ln\_test\_negative(int128) | ❓ |
| exp2\_test\_equivalence\_pow(uint256) | ❓ |
| exp2\_test\_inverse(int128) | ❓ |
| exp2\_test\_negative\_exponent(int128) | ❓ |
| exp\_test\_inverse(int128) | ❓ |
| exp\_test\_negative\_exponent(int128) | ❓ |

These tables are going to be updated over time as more invariants are verified.

## How To Run

To re-run the currently verified tests, execute:

```
echidna . --contract CryticABDKMath64x64Properties --format text --config test/echidna.yaml
```

[Bitwuzla 0.8.2](https://github.com/bitwuzla/bitwuzla/releases/tag/0.8.2) was used as the SMT solver. Please make sure you install Echidna after [this PR](https://github.com/crytic/echidna/pull/1431) was merged. 

## Changes 

We made a few small modifications to this codebase: 

* Adapted the header for using foundry libs and remappings.
* Commented properties without arguments. These are actually unit tests and will be converted to foundry tests.
* Some small changes in the formatting.
* Some auxiliary function such as `most_significant_bits` will be replaced by loop-less equivalent code.

## Oh, Just One More Thing

If there is an emergency and some invariant does not hold, please [open an issue](https://github.com/gustavo-grieco/abdk-math-64.64-verification/issues) in our issue tracker (even verified ones, there is always a chance of a bug). For contact the author, please use [this form](https://forms.gle/V3jt7C2JQgZhoXfe9).