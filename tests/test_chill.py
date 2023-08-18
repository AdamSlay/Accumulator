from src.models.chill import utah_model


def test_utah_model_freezing():
    # += 0.0
    assert utah_model(33.0, 0.0) == 0.0
    assert utah_model(34.0, 10.0) == 10.0


def test_utah_model_cold():
    # += 0.5
    assert utah_model(35.0, 0.0) == 0.5
    assert utah_model(36.0, 10.0) == 10.5


def test_utah_model_chill():
    # += 1.0
    assert utah_model(37.0, 0.0) == 1.0
    assert utah_model(48.0, 10.0) == 11.0


def test_utah_model_cool():
    # += 0.5
    assert utah_model(49.0, 0.0) == 0.5
    assert utah_model(54.0, 10.0) == 10.5


def test_utah_model_neutral():
    # += 0.0
    assert utah_model(55.0, 0.0) == 0.0
    assert utah_model(60.0, 10.0) == 10.0


def test_utah_model_warm():
    # += -0.5
    assert utah_model(61.0, 0.0) == 0.0
    assert utah_model(65.0, 10.0) == 9.5


def test_utah_model_hot():
    # += -1.0
    assert utah_model(66.0, 0.0) == 0.0
    assert utah_model(67.0, 10.0) == 9.0


def test_utah_model_decimal():
    # += 0.5
    assert utah_model(35.3, 0.0) == 0.5
    assert utah_model(36.7, 10.0) == 11.0
