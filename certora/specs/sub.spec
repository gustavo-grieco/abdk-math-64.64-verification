methods {
    function add(int128, int128) external returns (int128) envfree;
    function sub(int128, int128) external returns (int128) envfree;
    function neg(int128) external returns (int128) envfree;
}

// x - y == x + (-y)
rule sub_equivalence_to_addition(int128 x, int128 y) {
    int128 minus_y = neg(y);
    int128 addition = add@withrevert(x, minus_y);
    require !lastReverted;
    int128 subtraction = sub@withrevert(x, y);
    require !lastReverted;

    assert addition == subtraction, "x - y == x + (-y)";
}

// x - y == -(y - x)
rule sub_non_commutative(int128 x, int128 y) {
    int128 x_y = sub@withrevert(x, y);
    require !lastReverted;
    int128 y_x = sub@withrevert(y, x);
    require !lastReverted;

    assert x_y == neg(y_x), "x - y == -(y - x)";
}

// x - 0 == x and x - x == 0
rule sub_identity(int128 x) {
    int128 x_0 = sub(x, 0);
    assert x_0 == x, "x - 0 == x";

    int128 x_x = sub@withrevert(x, x);
    require !lastReverted;
    assert x_x == 0, "x - x == 0";
}

// (x - y) + y == (x + y) - y == x
rule sub_neutrality(int128 x, int128 y) {
    int128 x_minus_y = sub@withrevert(x, y);
    require !lastReverted;
    int128 x_plus_y = add@withrevert(x, y);
    require !lastReverted;

    int128 x_minus_y_plus_y = add@withrevert(x_minus_y, y);
    require !lastReverted;
    int128 x_plus_y_minus_y = sub@withrevert(x_plus_y, y);
    require !lastReverted;

    assert x_minus_y_plus_y == x_plus_y_minus_y, "both paths equal";
    assert x_minus_y_plus_y == x, "result is x";
}

// if y >= 0 then x-y <= x, else x-y > x
rule sub_values(int128 x, int128 y) {
    int128 x_y = sub@withrevert(x, y);
    require !lastReverted;

    assert y >= 0 => x_y <= x, "subtracting non-negative decreases";
    assert y < 0 => x_y > x, "subtracting negative increases";
}

// result is in valid range
rule sub_range(int128 x, int128 y) {
    int128 result = sub@withrevert(x, y);
    int128 MAX_64x64 = 170141183460469231731687303715884105727;
    int128 MIN_64x64 = -170141183460469231731687303715884105728;
    assert !lastReverted => (result <= MAX_64x64 && result >= MIN_64x64),
        "result in range";
}
