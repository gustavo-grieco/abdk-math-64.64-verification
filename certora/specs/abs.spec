methods {
    function abs(int128) external returns (int128) envfree;
    function neg(int128) external returns (int128) envfree;
    function add(int128, int128) external returns (int128) envfree;
    function mul(int128, int128) external returns (int128) envfree;
    function equal_within_precision(int128, int128, uint256) external returns (bool) envfree;
}

// |x| >= 0
rule abs_positive(int128 x) {
    int128 abs_x = abs@withrevert(x);
    require !lastReverted;
    assert abs_x >= 0, "|x| >= 0";
}

// |x| == |-x|
rule abs_negative(int128 x) {
    int128 abs_x = abs@withrevert(x);
    require !lastReverted;
    int128 neg_x = neg(x);
    int128 abs_neg_x = abs@withrevert(neg_x);
    require !lastReverted;
    assert abs_x == abs_neg_x, "|x| == |-x|";
}

// |x * y| == |x| * |y| (within precision)
rule abs_multiplicativeness(int128 x, int128 y) {
    int128 abs_x = x < 0 ? require_int128(0 - x) : x;
    int128 abs_y = y < 0 ? require_int128(0 - y) : y;
    int128 xy = mul@withrevert(x, y);
    require !lastReverted;
    int128 abs_xy = xy < 0 ? require_int128(0 - xy) : xy;
    int128 abs_x_abs_y = mul@withrevert(abs_x, abs_y);
    require !lastReverted;

    assert equal_within_precision(abs_xy, abs_x_abs_y, 1),
        "|x*y| == |x|*|y| within 1 bit";
}

// |x + y| <= |x| + |y|
rule abs_subadditivity(int128 x, int128 y) {
    int128 abs_x = abs@withrevert(x);
    require !lastReverted;
    int128 abs_y = abs@withrevert(y);
    require !lastReverted;
    int128 x_plus_y = add@withrevert(x, y);
    require !lastReverted;
    int128 abs_x_plus_y = abs@withrevert(x_plus_y);
    require !lastReverted;
    int128 abs_x_plus_abs_y = add@withrevert(abs_x, abs_y);
    require !lastReverted;

    assert abs_x_plus_y <= abs_x_plus_abs_y, "|x+y| <= |x|+|y|";
}
