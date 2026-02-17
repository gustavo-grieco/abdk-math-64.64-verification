methods {
    function div(int128, int128) external returns (int128) envfree;
    function abs(int128) external returns (int128) envfree;
    function neg(int128) external returns (int128) envfree;
}

// x / 1 == x and x / x == 1 (when x != 0)
// ONE_FP = 1 << 64
rule div_division_identity(int128 x) {
    int128 ONE_FP = 18446744073709551616;
    int128 div_1 = div(x, ONE_FP);
    assert div_1 == x, "x / 1 == x";

    int128 div_x = div@withrevert(x, x);
    // x/x should succeed unless x == 0
    assert !lastReverted => div_x == ONE_FP, "x / x == 1";
    assert lastReverted => x == 0, "only reverts when x == 0";
}

// x / -y == -(x / y)
rule div_negative_divisor(int128 x, int128 y) {
    require y < 0;
    int128 x_y = div@withrevert(x, y);
    require !lastReverted;
    int128 neg_y = neg(y);
    int128 x_neg_y = div@withrevert(x, neg_y);
    require !lastReverted;

    assert x_y == neg(x_neg_y), "x / -y == -(x / y)";
}

// 0 / x == 0 (when x != 0)
rule div_division_num_zero(int128 x) {
    require x != 0;
    int128 div_0 = div(0, x);
    assert div_0 == 0, "0 / x == 0";
}

// |x/y| <= |x| when |y| >= 1, |x/y| >= |x| when |y| < 1
// ONE_FP = 1 << 64
rule div_values(int128 x, int128 y) {
    int128 ONE_FP = 18446744073709551616;
    require y != 0;
    int128 x_y = div@withrevert(x, y);
    require !lastReverted;
    int128 abs_x_y = abs(x_y);
    int128 abs_x = abs(x);
    int128 abs_y = abs(y);

    assert abs_y >= ONE_FP => abs_x_y <= abs_x, "|y|>=1 => |x/y|<=|x|";
    assert abs_y < ONE_FP => abs_x_y >= abs_x, "|y|<1 => |x/y|>=|x|";
}

// division by zero must revert
rule div_div_by_zero(int128 x) {
    div@withrevert(x, 0);
    assert lastReverted, "div by zero must revert";
}

// |x / MAX| <= 1
// MAX_64x64 = 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
rule div_maximum_denominator(int128 x) {
    int128 ONE_FP = 18446744073709551616;
    int128 MAX_64x64 = 170141183460469231731687303715884105727;
    int128 result = div(x, MAX_64x64);
    assert abs(result) <= ONE_FP, "|x / MAX| <= 1";
}

// MAX / x succeeds only when |x| >= 1
rule div_maximum_numerator(int128 x) {
    int128 ONE_FP = 18446744073709551616;
    int128 MAX_64x64 = 170141183460469231731687303715884105727;
    int128 result = div@withrevert(MAX_64x64, x);
    assert !lastReverted => abs(x) >= ONE_FP, "succeeds only when |x| >= 1";
}

// result is in valid range
rule div_range(int128 x, int128 y) {
    int128 result = div@withrevert(x, y);
    int128 MAX_64x64 = 170141183460469231731687303715884105727;
    int128 MIN_64x64 = -170141183460469231731687303715884105728;
    assert !lastReverted => (result <= MAX_64x64 && result >= MIN_64x64),
        "result in range";
}
