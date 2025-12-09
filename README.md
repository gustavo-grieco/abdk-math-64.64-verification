# The Great Verification of ABDK Math 64.64

This repository contains an ongoing effort to verify the key mathematical properties implemented by [ABDK Math 64x64](https://github.com/abdk-consulting/abdk-libraries-solidity) using [Echidna](https://github.com/crytic/echidna) (powered by [hevm](https://github.com/ethereum/hevm/)). The invariants were directly extracted from the [crytic-properties repository](https://github.com/crytic/properties/tree/main/contracts/Math/ABDKMath64x64).

## Status

Currently, the following test were fully verified or were fully explored without finding any counter examples:

| Invariant | Result |
| ----- | :---: |
| `prove_abs_negative(int128)` | ✅ |
| `prove_abs_positive(int128)` | ✅ |
| `prove_abs_subadditivity(int128,int128)` | ✅ |
| `prove_add_associative(int128,int128,int128)` | ✅ |
| `prove_add_commutative(int128,int128)` | ✅ |
| `prove_add_identity(int128)` | ✅ |
| `prove_add_range(int128,int128)` | ✅ |
| `prove_add_values(int128,int128)` | ✅ |
| `prove_avg_one_value(int128)` | ✅ |
| `prove_avg_operand_order(int128,int128)` | ✅ |
| `prove_avg_values_in_range(int128,int128)` | ✅ |
| `prove_div_div_by_zero(int128)` | ✅ |
| `prove_div_division_identity(int128)` | ✅ |
| `prove_div_division_num_zero(int128)` | ✅ |
| `prove_div_maximum_numerator(int128)` | ✅ |
| `prove_div_range(int128,int128)` | ✅ |
| `prove_inv_division(int128)` | ✅ |
| `prove_inv_sign(int128)` | ✅ |
| `prove_inv_values(int128)` | ✅ |
| `prove_mul_commutative(int128,int128)` | ✅ |
| `prove_mul_identity(int128)` | ✅ |
| `prove_mul_range(int128,int128)` | ✅ |
| `prove_neg_double_negation(int128)` | ✅ |
| `prove_neg_identity(int128)` | ✅ |
| `prove_pow_maximum_base(uint256)` | ✅ |
| `prove_pow_one_exponent(int128)` | ✅ |
| `prove_pow_zero_exponent(int128)` | ✅ |
| `prove_sqrt_negative(int128)` | ✅ |
| `prove_sub_equivalence_to_addition(int128,int128)` | ✅ |
| `prove_sub_identity(int128)` | ✅ |
| `prove_sub_neutrality(int128,int128)` | ✅ |
| `prove_sub_non_commutative(int128,int128)` | ✅ |
| `prove_sub_range(int128,int128)` | ✅ |
| `prove_sub_values(int128,int128)` | ✅ |
| `prove_ln_negative(int128)` | ✅ |
| `prove_log2_negative(int128)` | ✅ |

**Verified:** 34/57 (59.65%)

When an invariant is explored using the symbolic engine in verification mode, there a few possible results:

* **Verified** ✅ The code was fully explored, without any issues on the translation or during solving. As expected, no counterexamples.
* **Passed**  👍 The code was fully explored without detecting any counterexamples, but the SMT solver cannot determine the answer to some of the queries (e.g. it timed out), so the assertion could still fail.
* **Failed** 💥 The exploration revealed a counterexample that was successfully replayed in concrete mode.
* **Error** ❌ A bug or a missing feature blocks the exploration or solving of some paths.
* **Timeout** ⏳ There are scalability issues preventing the creation of the model to explore all the program paths.

Some invariants were not fully verified yet:

| Invariant | Result |
| ----- | :---: |
| `prove_mul_associative(int128, int128, int128)` |  👍 |
| `prove_mul_values(int128, int128)` | 👍 |
| `prove_abs_multiplicativeness(int128, int128)` | 👍 |
| `prove_inv_division_noncommutativity(int128, int128)` | 👍 |
| `prove_div_negative_divisor(int128,int128)` | 👍 |
| `prove_gavg_one_value(int128)` | 👍 |
| `prove_div_values(int128,int128)` | 👍 |
| `prove_inv_double_inverse(int128)` | 👍 |

In these cases, there are timeouts when solving some SMT constraints. Using different [SMTs solvers could help to full verified these](https://github.com/ethereum/hevm/issues/709#issuecomment-2833348972).

The following invariants are in the process of verification or failed in the preliminary fuzzing campaign and they need to be re-implemented. For the symbolic execution engine to be able to verify some of them, it will require aggresive [state merging implemented in hevm](https://github.com/ethereum/hevm/issues/763) in finish in reasonable amount of time.

| Invariant | Result | Blockers
| ----- | :---: | -----
| `prove_mul_distributive(int128, int128, int128)` | 💥 |
| `prove_inv_multiplication(int128, int128)` | ❓ |
| `prove_inv_identity(int128)` | 💥 |
| `prove_gavg_values_in_range(int128, int128)` | ❓ |
| `prove_gavg_operand_order(int128, int128)` | ❓ |
| `prove_pow_zero_base(uint256)` | ❓ |
| `prove_pow_base_one(uint256)` | ❓ |
| `prove_pow_product_same_base(int128, uint256, uint256)` | 💥 |
| `prove_pow_power_of_an_exponentiation(int128, uint256, uint256)` | 💥 |
| `prove_pow_distributive(int128, int128, uint256)` | 💥 |
| `prove_pow_values(int128, uint256)` | ❓ |
| `prove_pow_sign(int128, uint256)` | ❓ |
| `prove_pow_high_exponent(int128, uint256)` | 💥 |
| `prove_sqrt_inverse_mul(int128)` | 💥 |
| `prove_sqrt_inverse_pow(int128)` | 💥 |
| `prove_sqrt_distributive(int128, int128)` | ❓ |
| `prove_log2_distributive_mul(int128, int128)` | ❓ |
| `prove_log2_power(int128, uint256)` | 💥 |
| `prove_ln_distributive_mul(int128, int128)` | 💥 |
| `prove_ln_power(int128, uint256)` | 💥 |
| `prove_exp2_equivalence_pow(uint256)` | ❓ |
| `prove_exp2_inverse(int128)` | 💥 |
| `prove_exp2_negative_exponent(int128)` | ❓ |
| `prove_exp_inverse(int128)` | 💥 |
| `prove_exp_negative_exponent(int128)` | ❓ |

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

If you want to run the verification of a single property, use `T` like this:

```
make verify T=prove_abs_negative
```

Alternatively, hevm can be used directly, even selecting an invariant:
```
make verify-hevm T=prove_abs_negative
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
