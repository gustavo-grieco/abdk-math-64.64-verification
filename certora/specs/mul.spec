methods {
    function mul(int128, int128) external returns (int128) envfree;
    function add(int128, int128) external returns (int128) envfree;
    function equal_within_tolerance(int128, int128, int128) external returns (bool) envfree;
    function equal_within_precision(int128, int128, uint256) external returns (bool) envfree;
    function significant_bits_after_mult(int128, int128) external returns (uint256) envfree;
}

// x * y == y * x
rule mul_commutative(int128 x, int128 y) {
    int128 x_y = mul@withrevert(x, y);
    bool firstReverted = lastReverted;

    int128 y_x = mul@withrevert(y, x);
    bool secondReverted = lastReverted;

    assert firstReverted == secondReverted, "both must revert or both must succeed";
    assert !firstReverted => x_y == y_x, "mul(x,y) == mul(y,x)";
}

// x * 1 == x and x * 0 == 0
// ONE_FP = 1 << 64 = 18446744073709551616
rule mul_identity(int128 x) {
    int128 ONE_FP = 18446744073709551616; // 1 << 64
    int128 x_1 = mul(x, ONE_FP);
    int128 x_0 = mul(x, 0);

    assert x_0 == 0, "x * 0 == 0";
    assert x_1 == x, "x * 1 == x";
}

// result is in valid range
rule mul_range(int128 x, int128 y) {
    int128 result = mul@withrevert(x, y);
    int128 MAX_64x64 = 170141183460469231731687303715884105727;
    int128 MIN_64x64 = -170141183460469231731687303715884105728;
    assert !lastReverted => (result <= MAX_64x64 && result >= MIN_64x64),
        "result in range";
}

// (x * y) * z ~= x * (y * z)
// ONE_TENTH_FP = 0.1 in 64.64
rule mul_associative(int128 x, int128 y, int128 z) {
    int128 ONE_TENTH_FP = 1844674407370955162;
    require (x < 0 ? require_int128(0 - x) : x) >= ONE_TENTH_FP;
    require (y < 0 ? require_int128(0 - y) : y) >= ONE_TENTH_FP;
    require (z < 0 ? require_int128(0 - z) : z) >= ONE_TENTH_FP;

    int128 x_y = mul@withrevert(x, y);
    require !lastReverted;
    int128 y_z = mul@withrevert(y, z);
    require !lastReverted;
    int128 xy_z = mul@withrevert(x_y, z);
    require !lastReverted;
    int128 x_yz = mul@withrevert(x, y_z);
    require !lastReverted;

    assert equal_within_tolerance(xy_z, x_yz, ONE_TENTH_FP),
        "(x*y)*z ~= x*(y*z)";
}

// x * (y + z) ~= x * y + x * z
rule mul_distributive(int128 x, int128 y, int128 z) {
    int128 ONE_TENTH_FP = 1844674407370955162;
    int128 QUINTILLION_FP = 18446744073709551616000000000000000000;
    int128 abs_x = x < 0 ? require_int128(0 - x) : x;
    int128 abs_y = y < 0 ? require_int128(0 - y) : y;
    int128 abs_z = z < 0 ? require_int128(0 - z) : z;

    require abs_x >= ONE_TENTH_FP && abs_x <= QUINTILLION_FP;
    require abs_y >= ONE_TENTH_FP && abs_y <= QUINTILLION_FP;
    require abs_z >= ONE_TENTH_FP && abs_z <= QUINTILLION_FP;

    int128 y_plus_z = add@withrevert(y, z);
    require !lastReverted;

    // Avoid catastrophic cancellation when y ~ -z
    int128 abs_y_plus_z = y_plus_z < 0 ? require_int128(0 - y_plus_z) : y_plus_z;
    require abs_y_plus_z >= ONE_TENTH_FP;

    int128 x_times_y_plus_z = mul@withrevert(x, y_plus_z);
    require !lastReverted;
    int128 x_times_y = mul@withrevert(x, y);
    require !lastReverted;
    int128 x_times_z = mul@withrevert(x, z);
    require !lastReverted;
    int128 x_y_plus_x_z = add@withrevert(x_times_y, x_times_z);
    require !lastReverted;

    assert equal_within_tolerance(x_y_plus_x_z, x_times_y_plus_z, ONE_TENTH_FP),
        "x*(y+z) ~= x*y + x*z";
}

// if x >= 0: y >= 1 => x*y >= x, y < 1 => x*y <= x
// if x < 0: y >= 1 => x*y <= x, y < 1 => x*y >= x
// ONE_FP = 1 << 64
rule mul_values(int128 x, int128 y) {
    int128 ONE_FP = 18446744073709551616;
    int128 x_y = mul@withrevert(x, y);
    require !lastReverted;

    assert (x >= 0 && y >= ONE_FP) => x_y >= x, "positive x, y>=1";
    assert (x >= 0 && y < ONE_FP) => x_y <= x, "positive x, y<1";
    assert (x < 0 && y >= ONE_FP) => x_y <= x, "negative x, y>=1";
    assert (x < 0 && y < ONE_FP) => x_y >= x, "negative x, y<1";
}
