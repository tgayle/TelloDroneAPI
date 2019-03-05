import pytest

from tellodroneapi.Drone import Drone


def test_base_drone_raises_error_on_init():
    with pytest.raises(TypeError):
        Drone()