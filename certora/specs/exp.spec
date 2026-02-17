methods {
    function exp_2(int128) external returns (int128) envfree;
    function exp(int128) external returns (int128) envfree;
    function pow(int128, uint256) external returns (int128) envfree;
    function log_2(int128) external returns (int128) envfree;
    function ln(int128) external returns (int128) envfree;
    function inv(int128) external returns (int128) envfree;
    function fromUInt(uint256) external returns (int128) envfree;
    function equal_within_precision(int128, int128, uint256) external returns (bool) envfree;
    function equal_within_tolerance(int128, int128, int128) external returns (bool) envfree;
}

// exp_2(x) == pow(2, x) for integer x
// TWO_FP = 2 << 64
rule exp2_equivalence_pow(uint256 x) {
    int128 TWO_FP = 36893488147419103232; // 2 << 64
    int128 x_fp = fromUInt@withrevert(x);
    require !lastReverted;
    int128 exp2_x = exp_2@withrevert(x_fp);
    require !lastReverted;
    int128 pow_2_x = pow@withrevert(TWO_FP, x);
    require !lastReverted;

    assert exp2_x == pow_2_x, "exp_2(x) == pow(2, x)";
}

// exp_2(log_2(x)) ~= x
rule exp2_inverse(int128 x) {
    int128 ONE_TENTH_FP = 1844674407370955162;
    int128 QUINTILLION_FP = 18446744073709551616000000000000000000;
    require x >= ONE_TENTH_FP && x <= QUINTILLION_FP;

    int128 log2_x = log_2(x);
    int128 exp2_log2_x = exp_2@withrevert(log2_x);
    require !lastReverted;

    assert equal_within_tolerance(x, exp2_log2_x, ONE_TENTH_FP),
        "exp_2(log_2(x)) ~= x";
}

// exp_2(-x) ~= inv(exp_2(x))
// MIN_64x64 = -0x80000000000000000000000000000000
rule exp2_negative_exponent(int128 x) {
    int128 MIN_64x64 = -170141183460469231731687303715884105728;
    require x < 0 && x != MIN_64x64;

    int128 exp2_x = exp_2@withrevert(x);
    require !lastReverted;
    int128 neg_x = require_int128(0 - x);
    int128 exp2_neg_x = exp_2@withrevert(neg_x);
    require !lastReverted;
    int128 inv_exp2_neg_x = inv@withrevert(exp2_neg_x);
    require !lastReverted;

    assert equal_within_precision(exp2_x, inv_exp2_neg_x, 4),
        "exp_2(-x) ~= inv(exp_2(x))";
}

// exp(-x) ~= inv(exp(x))
rule exp_negative_exponent(int128 x) {
    int128 MIN_64x64 = -170141183460469231731687303715884105728;
    require x < 0 && x != MIN_64x64;

    int128 exp_x = exp@withrevert(x);
    require !lastReverted;
    int128 neg_x = require_int128(0 - x);
    int128 exp_neg_x = exp@withrevert(neg_x);
    require !lastReverted;
    int128 inv_exp_neg_x = inv@withrevert(exp_neg_x);
    require !lastReverted;

    assert equal_within_precision(exp_x, inv_exp_neg_x, 4),
        "exp(-x) ~= inv(exp(x))";
}

// exp(ln(x)) ~= x
rule exp_inverse(int128 x) {
    int128 ONE_TENTH_FP = 1844674407370955162;
    int128 QUINTILLION_FP = 18446744073709551616000000000000000000;
    require x >= ONE_TENTH_FP && x <= QUINTILLION_FP;

    int128 ln_x = ln@withrevert(x);
    require !lastReverted;
    int128 exp_ln_x = exp@withrevert(ln_x);
    require !lastReverted;

    assert equal_within_tolerance(x, exp_ln_x, ONE_TENTH_FP),
        "exp(ln(x)) ~= x";
}
