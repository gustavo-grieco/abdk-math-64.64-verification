methods {
    function neg(int128) external returns (int128) envfree;
    function add(int128, int128) external returns (int128) envfree;
}

// -(-x) == x
rule neg_double_negation(int128 x) {
    int128 double_neg = neg(neg(x));
    assert double_neg == x, "-(-x) == x";
}

// x + (-x) == 0
rule neg_identity(int128 x) {
    int128 neg_x = neg(x);
    int128 x_plus_neg_x = add@withrevert(x, neg_x);
    require !lastReverted;
    assert x_plus_neg_x == 0, "x + (-x) == 0";
}
