import pytest
from PackMan import draw_stuff


def test_draw_stuff():
    with pytest.raises(TypeError):
        draw_stuff(10, 20)
