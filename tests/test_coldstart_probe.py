import weltenfw


def test_version_is_str():
    assert isinstance(weltenfw.__version__, str)


def test_module_has_all():
    assert hasattr(weltenfw, "__all__")
    assert isinstance(weltenfw.__all__, (list, tuple))
