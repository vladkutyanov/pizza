from pizza_final import *
import pytest


def test_margherita_size():
    with pytest.raises(ValueError):
        assert Margherita(123)


def test_pepperoni_size():
    with pytest.raises(ValueError):
        assert Pepperoni('size')


def test_hawaiian_size():
    with pytest.raises(ValueError):
        assert Hawaiian('size')


def test_pizzas_equality_pep_marg():
    with pytest.raises(TypeError):
        assert Pepperoni() == Margherita()


def test_pizzas_equality_pep_pep():
    assert Pepperoni(pizza_size='L') != \
           Pepperoni(pizza_size='XL')


def test_recipe():
    assert Pepperoni().dict() == \
           {'Pepperoni': ['tomato sauce', 'mozzarella', 'pepperoni']}


def test_bake():
    with pytest.raises(TypeError):
        assert bake(Margherita()) \
               == bake(Pepperoni())


def test_bake_without_pizza():
    with pytest.raises(AttributeError):
        assert bake(123) == Pepperoni()


def test_order_routines():
    assert order_routines(Margherita(), True, False) is None
