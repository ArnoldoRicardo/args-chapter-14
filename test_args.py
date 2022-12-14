from args import Args


def test_create_with_no_schema_or_argument():
    args = Args('', [])
    assert args.cardinality() == 0


def test_simple_boolean_preset():
    args = Args('x', ['-x'])
    assert args.cardinality() == 1
    assert args.getBoolean('x')


def tests_paces_in_format():
    args = Args('x, y', ['-xy'])
    assert args.cardinality() == 2
    assert args.has('x')
    assert args.has('y')
