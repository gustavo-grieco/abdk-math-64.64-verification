methods {
    function pow(int128, uint256) external returns (int128) envfree;
    function abs(int128) external returns (int128) envfree;
}

// x ** 0 == 1
// ONE_FP = 1 << 64
rule pow_zero_exponent(int128 x) {
    int128 ONE_FP = 18446744073709551616;
    int128 x_pow_0 = pow(x, 0);
    assert x_pow_0 == ONE_FP, "x^0 == 1";
}

// 0 ** x == 0 (for x != 0)
rule pow_zero_base(uint256 x) {
    require x != 0;
    int128 zero_pow_x = pow(0, x);
    assert zero_pow_x == 0, "0^x == 0";
}

// x ** 1 == x
rule pow_one_exponent(int128 x) {
    int128 x_pow_1 = pow(x, 1);
    assert x_pow_1 == x, "x^1 == x";
}

// 1 ** x == 1
// ONE_FP = 1 << 64
rule pow_base_one(uint256 x) {
    int128 ONE_FP = 18446744073709551616;
    int128 one_pow_x = pow(ONE_FP, x);
    assert one_pow_x == ONE_FP, "1^x == 1";
}

// MAX ** a must revert for a > 1
// MAX_64x64 = 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
rule pow_maximum_base(uint256 a) {
    int128 MAX_64x64 = 170141183460469231731687303715884105727;
    require a > 1;
    pow@withrevert(MAX_64x64, a);
    assert lastReverted, "MAX^a must revert for a > 1";
}

// |x| >= 1 => |x^a| >= 1 and |x| <= 1 => |x^a| <= 1
// ONE_FP = 1 << 64
rule pow_values(int128 x, uint256 a) {
    int128 ONE_FP = 18446744073709551616;
    require x != 0;
    int128 x_a = pow@withrevert(x, a);
    require !lastReverted;

    assert abs(x) >= ONE_FP => abs(x_a) >= ONE_FP, "|x|>=1 => |x^a|>=1";
    assert abs(x) <= ONE_FP => abs(x_a) <= ONE_FP, "|x|<=1 => |x^a|<=1";
}

// even exponent => positive result; odd exponent => preserves sign
rule pow_sign(int128 x, uint256 a) {
    require x != 0 && a != 0;
    int128 x_a = pow@withrevert(x, a);
    require !lastReverted;
    require x_a != 0; // avoid rounding to zero

    assert a % 2 == 0 => x_a == abs(x_a), "even exp => positive";
    assert (a % 2 != 0 && x < 0) => x_a < 0, "odd exp, negative base => negative";
    assert (a % 2 != 0 && x > 0) => x_a > 0, "odd exp, positive base => positive";
}

// |x| < 1 and very high exponent => result is zero
// ONE_FP = 1 << 64
rule pow_high_exponent(int128 x, uint256 a) {
    int128 ONE_FP = 18446744073709551616;
    require abs(x) < ONE_FP;
    require a > 340282366920938463463374607431768211456; // 2^128
    int128 result = pow@withrevert(x, a);
    require !lastReverted;
    assert result == 0, "tiny base ^ huge exp == 0";
}
