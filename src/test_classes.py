from functions import square, cube

class TestClass:
    # Share this common number between test instances
    num = 5

    def test_square_class(self):
        result = square(self.num)
        assert result == self.num ** 2
    
    def test_cube_class(self):
        result = cube(self.num)
        assert result == self.num ** 3
