import pytest


# ------------------------------------------------------
# Basic tests
# ------------------------------------------------------

# Function
def plus_one(x):
    return x + 1


def test_incorrect():
    assert plus_one(3) != 5


def test_floats():
    assert plus_one(3.5) == 4.5


def test_negative():
    assert plus_one(-3) == -2

# ------------------------------------------------------
# Tests using fixtures

# Information about using fixtures:
# https://docs.pytest.org/en/6.2.x/fixture.html#fixtures
# ------------------------------------------------------
class Fruit:
    def __init__(self, name):
        self.name = name
        self.cubed = False

    def __eq__(self, other):
        return self.name == other.name

    def cube(self):
        self.cubed = True

class FruitSalad:
    def __init__(self, *fruit_bowl):
        self.fruit = fruit_bowl
        self._cube_fruit()

    def _cube_fruit(self):
        for fruit in self.fruit:
            fruit.cube()

@pytest.fixture
def my_fruit():
    return Fruit("apple")


@pytest.fixture
def fruit_basket(my_fruit):
    return [Fruit("banana"), my_fruit]


def test_my_fruit_in_basket(my_fruit, fruit_basket):
    assert my_fruit in fruit_basket


# Arrange
@pytest.fixture
def fruit_bowl():
    return [Fruit("apple"), Fruit("banana")]


def test_fruit_salad(fruit_bowl):
    # Act
    fruit_salad = FruitSalad(*fruit_bowl)

    # Assert
    assert all(fruit.cubed for fruit in fruit_salad.fruit)
