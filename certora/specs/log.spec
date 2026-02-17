methods {
    function log_2(int128) external returns (int128) envfree;
    function ln(int128) external returns (int128) envfree;
    function mul(int128, int128) external returns (int128) envfree;
    function add(int128, int128) external returns (int128) envfree;
    function abs(int128) external returns (int128) envfree;
    function pow(int128, uint256) external returns (int128) envfree;
    function fromUInt(uint256) external returns (int128) envfree;
    function toUInt(int128) external returns (uint64) envfree;
    function equal_within_precision(int128, int128, uint256) external returns (bool) envfree;
    function equal_within_tolerance(int128, int128, int128) external returns (bool) envfree;
    function significant_bits_after_mult(int128, int128) external returns (uint256) envfree;
}

// log2(x * y) ~= log2(x) + log2(y)
rule log2_distributive_mul(int128 x, int128 y) {
    int128 log2_x = log_2@withrevert(x);
    require !lastReverted;
    int128 log2_y = log_2@withrevert(y);
    require !lastReverted;
    int128 log2_x_plus_log2_y = add(log2_x, log2_y);

    int128 xy = mul@withrevert(x, y);
    require !lastReverted;
    int128 log2_xy = log_2@withrevert(xy);
    require !lastReverted;

    require significant_bits_after_mult(x, y) > 10;
    uint256 loss = require_uint256(toUInt(abs(add(log_2(x), log_2(y)))));

    assert equal_within_precision(log2_x_plus_log2_y, log2_xy, loss),
        "log2(x*y) ~= log2(x)+log2(y)";
}

// log2 of negative must revert
rule log2_negative(int128 x) {
    require x < 0;
    log_2@withrevert(x);
    assert lastReverted, "log2 of negative must revert";
}

// ln of negative must revert
rule ln_negative(int128 x) {
    require x < 0;
    ln@withrevert(x);
    assert lastReverted, "ln of negative must revert";
}

// ln(x^y) ~= y * ln(x)
rule ln_power(int128 x, uint256 y) {
    int128 ONE_TENTH_FP = 1844674407370955162;
    int128 QUINTILLION_FP = 18446744073709551616000000000000000000;
    require x >= ONE_TENTH_FP && x <= QUINTILLION_FP;
    require y >= 1 && y <= 10;

    int128 ln_x = ln@withrevert(x);
    require !lastReverted;
    int128 abs_ln_x = ln_x < 0 ? require_int128(0 - ln_x) : ln_x;
    require abs_ln_x >= ONE_TENTH_FP;

    int128 x_y = pow@withrevert(x, y);
    require !lastReverted;
    require x_y >= ONE_TENTH_FP && x_y <= QUINTILLION_FP;

    int128 ln_x_y = ln@withrevert(x_y);
    require !lastReverted;
    int128 y_fp = fromUInt(y);
    int128 y_times_ln_x = mul@withrevert(y_fp, ln_x);
    require !lastReverted;

    assert equal_within_tolerance(ln_x_y, y_times_ln_x, ONE_TENTH_FP),
        "ln(x^y) ~= y*ln(x)";
}
