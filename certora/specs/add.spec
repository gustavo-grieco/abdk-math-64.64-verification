methods {
    function add(int128, int128) external returns (int128) envfree;
    function neg(int128) external returns (int128) envfree;
}

// x + y == y + x
rule add_commutative(int128 x, int128 y) {
    int128 x_y = add@withrevert(x, y);
    bool firstReverted = lastReverted;

    int128 y_x = add@withrevert(y, x);
    bool secondReverted = lastReverted;

    assert firstReverted == secondReverted, "both must revert or both must succeed";
    assert !firstReverted => x_y == y_x, "add(x,y) == add(y,x)";
}

// (x + y) + z == x + (y + z)
rule add_associative(int128 x, int128 y, int128 z) {
    int128 x_y = add@withrevert(x, y);
    require !lastReverted;
    int128 y_z = add@withrevert(y, z);
    require !lastReverted;
    int128 xy_z = add@withrevert(x_y, z);
    require !lastReverted;
    int128 x_yz = add@withrevert(x, y_z);
    require !lastReverted;

    assert xy_z == x_yz, "(x+y)+z == x+(y+z)";
}

// x + 0 == x and x + (-x) == 0
rule add_identity(int128 x) {
    int128 x_0 = add(x, 0);
    assert x_0 == x, "x + 0 == x";

    int128 neg_x = neg(x);
    int128 x_neg_x = add@withrevert(x, neg_x);
    require !lastReverted;
    assert x_neg_x == 0, "x + (-x) == 0";
}

// if y >= 0 then x+y >= x, else x+y < x
rule add_values(int128 x, int128 y) {
    int128 x_y = add@withrevert(x, y);
    require !lastReverted;

    assert y >= 0 => x_y >= x, "adding non-negative increases";
    assert y < 0 => x_y < x, "adding negative decreases";
}

// result is in valid range (trivially true but checks no overflow)
rule add_range(int128 x, int128 y) {
    int128 result = add@withrevert(x, y);
    int128 MAX_64x64 = 170141183460469231731687303715884105727;
    int128 MIN_64x64 = -170141183460469231731687303715884105728;
    assert !lastReverted => (result <= MAX_64x64 && result >= MIN_64x64),
        "result in range";
}
