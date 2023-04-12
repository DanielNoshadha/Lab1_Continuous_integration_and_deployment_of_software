import pytest
from PackMan import draw_stuff, move_packman, direction, turns_allowed


def test_draw_stuff():
    with pytest.raises(TypeError):
        draw_stuff(10, 20)


def test_move_packman():
    with pytest.raises(TypeError):
        direction = 0
        turns_allowed[0]
        move_packman(450, 663)
