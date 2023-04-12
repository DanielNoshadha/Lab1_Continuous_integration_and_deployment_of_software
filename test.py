from PackMan import move_packman

def test_move_packman():
    packman_x = 100
    packman_y = 100


    # Test moving Pacman to the right
    new_x, new_y = move_packman(packman_x, packman_y)
    assert new_x == 102
    assert new_y == 100
