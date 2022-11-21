from harnas.error import Error


def test_from_exception():
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    e = Exception(text)
    error = Error.from_exception(e)

    assert error.message == text


def test_str():
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
    error = Error(text)

    assert str(error) == text
