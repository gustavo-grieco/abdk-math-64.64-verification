methods {
    function avg(int128, int128) external returns (int128) envfree;
    function gavg(int128, int128) external returns (int128) envfree;
    function abs(int128) external returns (int128) envfree;
}

// avg(x,y) is between min(x,y) and max(x,y)
rule avg_values_in_range(int128 x, int128 y) {
    int128 avg_xy = avg(x, y);

    assert x >= y => (avg_xy >= y && avg_xy <= x), "avg in range when x>=y";
    assert x < y => (avg_xy >= x && avg_xy <= y), "avg in range when x<y";
}

// avg(x, x) == x
rule avg_one_value(int128 x) {
    int128 avg_x = avg(x, x);
    assert avg_x == x, "avg(x,x) == x";
}

// avg(x, y) == avg(y, x)
rule avg_operand_order(int128 x, int128 y) {
    int128 avg_xy = avg(x, y);
    int128 avg_yx = avg(y, x);
    assert avg_xy == avg_yx, "avg(x,y) == avg(y,x)";
}

// gavg(x, x) == |x|
rule gavg_one_value(int128 x) {
    int128 gavg_x = gavg@withrevert(x, x);
    require !lastReverted;
    assert gavg_x == abs(x), "gavg(x,x) == |x|";
}

// gavg(x, y) == gavg(y, x)
rule gavg_operand_order(int128 x, int128 y) {
    int128 gavg_xy = gavg@withrevert(x, y);
    require !lastReverted;
    int128 gavg_yx = gavg@withrevert(y, x);
    require !lastReverted;
    assert gavg_xy == gavg_yx, "gavg(x,y) == gavg(y,x)";
}

// gavg(x,y) is between min(|x|,|y|) and max(|x|,|y|) (or zero if either is zero)
rule gavg_values_in_range(int128 x, int128 y) {
    int128 gavg_xy = gavg@withrevert(x, y);
    require !lastReverted;
    int128 abs_x = abs(x);
    int128 abs_y = abs(y);

    assert (x == 0 || y == 0) => gavg_xy == 0, "zero if either is zero";
    assert (x != 0 && y != 0 && abs_x >= abs_y) => (gavg_xy >= abs_y && gavg_xy <= abs_x),
        "gavg in range when |x|>=|y|";
    assert (x != 0 && y != 0 && abs_x < abs_y) => (gavg_xy >= abs_x && gavg_xy <= abs_y),
        "gavg in range when |x|<|y|";
}
