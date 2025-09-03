# The Great Verification of ABDK Math 64.64

This repository contains an ongoing effort to verify the key mathematical properties implemented by [ABDK Math 64x64](https://github.com/abdk-consulting/abdk-libraries-solidity) using [Echidna](https://github.com/crytic/echidna) (powered by [hevm](https://github.com/ethereum/hevm/)). The invariants were directly extracted from the [crytic-properties repository](https://github.com/crytic/properties/tree/main/contracts/Math/ABDKMath64x64).

## Status

Currently, the following test were fully verified or were fully explored without finding any counter examples:

| Invariant | Result |
| ----- | :---: |
| `sub_test_non_commutative(int128,int128)` | ✅ |
| `neg_test_identity(int128)` | ✅ |
| `sub_test_equivalence_to_addition(int128,int128)` | ✅ |
| `abs_test_negative(int128)` | ✅ |
| `div_test_values(int128,int128)` | 👍 |
| `inv_test_division(int128)` | ✅ |
| `abs_test_positive(int128)` | ✅ |
| `sqrt_test_negative(int128)` | ✅ |
| `sub_test_identity(int128)` | ✅ |
| `div_test_range(int128,int128)` | ✅ |
| `abs_test_subadditivity(int128,int128)` | ✅ |
| `inv_test_values(int128)` | ✅ |
| `add_test_commutative(int128,int128)` | ✅ |
| `mul_test_identity(int128)` | ✅ |
| `avg_test_one_value(int128)` | ✅ |
| `add_test_associative(int128,int128,int128)` | ✅ |
| `add_test_identity(int128)` | ✅ |
| `avg_test_values_in_range(int128,int128)` | ✅ |
| `div_test_division_num_zero(int128)` | ✅ |
| `avg_test_operand_order(int128,int128)` | ✅ |
| `div_test_division_identity(int128)` | ✅ |
| `sub_test_neutrality(int128,int128)` | ✅ |
| `neg_test_double_negation(int128)` | ✅ |
| `inv_test_sign(int128)` | ✅ |
| `div_test_negative_divisor(int128,int128)` | 👍 |
| `div_test_maximum_numerator(int128)` | ✅ |
| `gavg_test_one_value(int128)` | 🎉 |
| `mul_test_range(int128,int128)` | ✅ |
| `add_test_values(int128,int128)` | ✅ |
| `sub_test_range(int128,int128)` | ✅ |
| `mul_test_commutative(int128,int128)` | ✅ |
| `div_test_maximum_denominator(int128)` | ✅ |
| `div_test_div_by_zero(int128)` | ✅ |
| `add_test_range(int128,int128)` | ✅ |
| `sub_test_values(int128,int128)` | ✅ |

When an invariant is explored using the symbolic engine in verification mode, there a few possible results:

* **Verified** ✅ The code was fully explored, without any issues on the translation or during solving. As expected, no counterexamples.
* **Passed**  👍 The code was fully explored without detecting any counterexamples, but the SMT solver cannot determine the answer to some of the queries (e.g. it timed out), so the assertion could still fail.
* **Failed** 💥 The exploration revealed a counterexample that was successfully replayed in concrete mode.
* **Error** ❌ A bug or a missing feature blocks the exploration or solving of some paths.
* **Timeout** ⏳ There are scalability issues preventing the creation of the model to explore all the program paths. 

In the case of `div_test_values(int128,int128)` and `div_test_negative_divisor(int128,int128)`, there are timeouts when solving some SMT constraints. Using different [SMTs solvers could help to full verified these](https://github.com/ethereum/hevm/issues/709#issuecomment-2833348972).

The following invariants are in the process of verification or failed in the preliminary fuzzing campaign and they need to be re-implemented. For the symbolic execution engine to be able to verify some of them, it will require aggresive [state merging implemented in hevm](https://github.com/ethereum/hevm/issues/763) in finish in reasonable amount of time. 

| Invariant | Result |
| ----- | :---: |
| `mul_test_associative(int128, int128, int128)` | ❓ |
| `mul_test_distributive(int128, int128, int128)` | ❓ |
| `mul_test_values(int128, int128)` | ❓ |
| `abs_test_multiplicativeness(int128, int128)` | ❓ |
| `inv_test_double_inverse(int128)` | ❓ |
| `inv_test_division_noncommutativity(int128, int128)` | ❓ |
| `inv_test_multiplication(int128, int128)` | ❓ |
| `inv_test_identity(int128)` | ❓ |
| `gavg_test_values_in_range(int128, int128)` | ❓ |
| `gavg_test_operand_order(int128, int128)` | ❓ |
| `pow_test_zero_exponent(int128)`  | ❓ |
| `pow_test_zero_base(uint256)` | ❓ |
| `pow_test_one_exponent(int128)` | ❓ |
| `pow_test_base_one(uint256)` | ❓ |
| `pow_test_product_same_base(int128, uint256, uint256)` | 💥 |
| `pow_test_power_of_an_exponentiation(int128, uint256, uint256)` | 💥 |
| `pow_test_distributive(int128, int128, uint256)` | 💥 |
| `pow_test_values(int128, uint256)` | ❓ |
| `pow_test_sign(int128, uint256)` | ❓ |
| `pow_test_maximum_base(uint256)` | ❓ |
| `pow_test_high_exponent(int128, uint256)` | 💥 |
| `sqrt_test_inverse_mul(int128)` | 💥 |
| `sqrt_test_inverse_pow(int128)` | 💥 |
| `sqrt_test_distributive(int128, int128)` | ❓ |
| `log2_test_distributive_mul(int128, int128)` | ❓ |
| `log2_test_power(int128, uint256)` | 💥 |
| `log2_test_negative(int128)` | ❓ |
| `ln_test_distributive_mul(int128, int128)` | 💥 |
| `ln_test_power(int128, uint256)` | 💥 |
| `ln_test_negative(int128)` | ❓ |
| `exp2_test_equivalence_pow(uint256)` | ❓ |
| `exp2_test_inverse(int128)` | 💥 |
| `exp2_test_negative_exponent(int128)` | ❓ |
| `exp_test_inverse(int128)` | 💥 |
| `exp_test_negative_exponent(int128)` | ❓ |

These tables are going to be updated over time as more invariants are verified.

## How To Run

If you want to run a preliminary fuzzing campaign, use:

```
make fuzz
```

To re-run the currently verified tests, execute:

```
make verify
```

If you want to run the verification of a single property, use `TARGET` like this:

```
make verify TARGET=abs_test_negative
```

To make sure the verification works as expected, please install Echidna from its latest `master` revision and [Bitwuzla 0.8.2](https://github.com/bitwuzla/bitwuzla/releases/tag/0.8.2).

## Changes 

We made a few small modifications to this codebase: 

* Adapted the header for using Foundry libraries and remappings.
* Commented out properties without arguments. These are actually unit tests and will be converted into Foundry tests.
* Applied minor formatting changes.
* Replaced some auxiliary functions such as `most_significant_bits` with loop-less equivalents.

## Oh, Just One More Thing

If an emergency arises and an invariant does not hold, please [open an issue](https://github.com/gustavo-grieco/abdk-math-64.64-verification/issues) in our tracker (even verified invariants can still reveal bugs). To contact the author directly, please use [this form](https://forms.gle/V3jt7C2JQgZhoXfe9).