from args import Args


def test_create_with_no_schema_or_argument():
    args = Args('', [])
    assert args.cardinality() == 0


def test_simple_boolean_preset():
    args = Args('x', ['-x'])
    assert args.cardinality() == 1
    assert args.getBoolean('x')


def test_boolean_bad_key():
    args = Args('x', ['-x'])
    assert args.cardinality() == 1
    try:
        args.getBoolean('y')
        assert False
    except KeyError as e:
        print(e)
        assert True


def tests_paces_in_format():
    args = Args('x, y', ['-xy'])
    assert args.cardinality() == 2
    assert args.has('x')
    assert args.has('y')


def test_simple_string_preset():
    args = Args('x*', ['-x', 'param'])
    assert args.cardinality() == 1
    assert args.has('x')
    assert args.getString('x') == 'param'
