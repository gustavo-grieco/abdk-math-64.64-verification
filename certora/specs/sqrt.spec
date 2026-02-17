methods {
    function sqrt(int128) external returns (int128) envfree;
    function mul(int128, int128) external returns (int128) envfree;
    function pow(int128, uint256) external returns (int128) envfree;
    function equal_within_tolerance(int128, int128, int128) external returns (bool) envfree;
}

// sqrt(x) * sqrt(x) ~= x
rule sqrt_inverse_mul(int128 x) {
    int128 ONE_TENTH_FP = 1844674407370955162;
    int128 QUINTILLION_FP = 18446744073709551616000000000000000000; // 10^18 in 64.64
    require x >= ONE_TENTH_FP && x <= QUINTILLION_FP;

    int128 sqrt_x = sqrt(x);
    int128 squared = mul@withrevert(sqrt_x, sqrt_x);
    require !lastReverted;

    assert equal_within_tolerance(squared, x, ONE_TENTH_FP),
        "sqrt(x)^2 ~= x";
}

// sqrt(x) ** 2 ~= x
rule sqrt_inverse_pow(int128 x) {
    int128 ONE_TENTH_FP = 1844674407370955162;
    int128 QUINTILLION_FP = 18446744073709551616000000000000000000;
    require x >= ONE_TENTH_FP && x <= QUINTILLION_FP;

    int128 sqrt_x = sqrt(x);
    int128 squared = pow@withrevert(sqrt_x, 2);
    require !lastReverted;

    assert equal_within_tolerance(squared, x, ONE_TENTH_FP),
        "sqrt(x)^2 ~= x (via pow)";
}

// sqrt(x) * sqrt(y) ~= sqrt(x * y)
rule sqrt_distributive(int128 x, int128 y) {
    int128 ONE_TENTH_FP = 1844674407370955162;
    int128 QUINTILLION_FP = 18446744073709551616000000000000000000;
    require x >= ONE_TENTH_FP && x <= QUINTILLION_FP;
    require y >= ONE_TENTH_FP && y <= QUINTILLION_FP;

    int128 sqrt_x = sqrt(x);
    int128 sqrt_y = sqrt(y);
    int128 sqrt_x_sqrt_y = mul@withrevert(sqrt_x, sqrt_y);
    require !lastReverted;
    int128 xy = mul@withrevert(x, y);
    require !lastReverted;
    int128 sqrt_xy = sqrt(xy);

    assert equal_within_tolerance(sqrt_x_sqrt_y, sqrt_xy, ONE_TENTH_FP),
        "sqrt(x)*sqrt(y) ~= sqrt(x*y)";
}

// sqrt(negative) must revert
rule sqrt_negative(int128 x) {
    require x < 0;
    sqrt@withrevert(x);
    assert lastReverted, "sqrt of negative must revert";
}
