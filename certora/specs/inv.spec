methods {
    function inv(int128) external returns (int128) envfree;
    function div(int128, int128) external returns (int128) envfree;
    function mul(int128, int128) external returns (int128) envfree;
    function abs(int128) external returns (int128) envfree;
    function equal_within_precision(int128, int128, uint256) external returns (bool) envfree;
    function equal_within_tolerance(int128, int128, int128) external returns (bool) envfree;
    function significant_bits_after_mult(int128, int128) external returns (uint256) envfree;
    function log_2(int128) external returns (int128) envfree;
    function toUInt(int128) external returns (uint64) envfree;
    function msb64x64(int128) external returns (uint256) envfree;
}

// inv(inv(x)) ~= x (within precision loss of 2*log2(x)+2 bits)
rule inv_double_inverse(int128 x) {
    require x != 0;
    int128 inv_x = inv@withrevert(x);
    require !lastReverted;
    int128 double_inv = inv@withrevert(inv_x);
    require !lastReverted;

    uint256 loss = require_uint256(2 * msb64x64(x) + 2);
    assert equal_within_precision(x, double_inv, loss),
        "inv(inv(x)) ~= x";
}

// inv(x) == 1 / x
// ONE_FP = 1 << 64
rule inv_division(int128 x) {
    int128 ONE_FP = 18446744073709551616;
    require x != 0;
    int128 inv_x = inv(x);
    int128 div_1_x = div(ONE_FP, x);
    assert inv_x == div_1_x, "inv(x) == 1/x";
}

// x / y ~= 1 / (y / x)
rule inv_division_noncommutativity(int128 x, int128 y) {
    int128 ONE_TENTH_FP = 1844674407370955162; // 0.1 in 64.64
    require x != 0 && y != 0;
    int128 x_y = div@withrevert(x, y);
    require !lastReverted;
    int128 y_x = div@withrevert(y, x);
    require !lastReverted;
    int128 inv_y_x = inv@withrevert(y_x);
    require !lastReverted;

    // 290 * ONE_TENTH_FP = 29 * ONE_FP
    int128 tolerance = 534955378138176997248; // 290 * ONE_TENTH_FP
    assert equal_within_tolerance(x_y, inv_y_x, tolerance),
        "x/y ~= inv(y/x)";
}

// inv(x) * inv(y) ~= inv(x * y)
rule inv_multiplication(int128 x, int128 y) {
    require x != 0 && y != 0;
    int128 inv_x = inv(x);
    int128 inv_y = inv(y);
    int128 inv_x_times_inv_y = mul@withrevert(inv_x, inv_y);
    require !lastReverted;

    int128 x_y = mul@withrevert(x, y);
    require !lastReverted;
    int128 inv_x_y = inv@withrevert(x_y);
    require !lastReverted;

    require significant_bits_after_mult(x, y) > 10;
    require significant_bits_after_mult(inv_x, inv_y) > 10;

    // precision loss: 2 * |log2(x) - log2(y)| + 1
    int128 log2_x = log_2(abs(x));
    int128 log2_y = log_2(abs(y));
    int128 log_diff = require_int128(log2_x - log2_y);
    int128 abs_log_diff = log_diff < 0 ? require_int128(0 - log_diff) : log_diff;
    uint256 loss = require_uint256(2 * toUInt(abs_log_diff) + 1);

    assert equal_within_precision(inv_x_y, inv_x_times_inv_y, loss),
        "inv(x*y) ~= inv(x)*inv(y)";
}

// inv(x) * x ~= 1
rule inv_identity(int128 x) {
    int128 ONE_FP = 18446744073709551616;
    int128 ONE_TENTH_FP = 1844674407370955162;
    int128 BILLION_FP = 18446744073709551616000000000;
    int128 abs_x = x < 0 ? require_int128(0 - x) : x;
    require abs_x >= ONE_TENTH_FP && abs_x <= BILLION_FP;

    int128 inv_x = inv(x);
    int128 identity = mul@withrevert(inv_x, x);
    require !lastReverted;

    assert equal_within_tolerance(identity, ONE_FP, ONE_TENTH_FP),
        "inv(x) * x ~= 1";
}

// |inv(x)| <= 1 when |x| >= 1, |inv(x)| > 1 when |x| < 1
// ONE_FP = 1 << 64
rule inv_values(int128 x) {
    int128 ONE_FP = 18446744073709551616;
    require x != 0;
    int128 abs_inv_x = abs(inv(x));
    int128 abs_x = abs(x);

    assert abs_x >= ONE_FP => abs_inv_x <= ONE_FP, "|x|>=1 => |inv(x)|<=1";
    assert abs_x < ONE_FP => abs_inv_x > ONE_FP, "|x|<1 => |inv(x)|>1";
}

// sign(inv(x)) == sign(x)
rule inv_sign(int128 x) {
    require x != 0;
    int128 inv_x = inv(x);

    assert x > 0 => inv_x > 0, "positive preserved";
    assert x < 0 => inv_x < 0, "negative preserved";
}
