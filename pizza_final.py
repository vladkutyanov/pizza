import click
from random import randint
from abc import ABC, abstractmethod


class Pizza(ABC):
    """
    Абстрактный класс пиццы, от него наследуются различные виды пицц.
    """
    @classmethod
    @abstractmethod
    def dict(cls):
        pass

    @classmethod
    @abstractmethod
    def __eq__(cls, other):
        pass


class Margherita(Pizza):
    """
    Класс для пиццы Маргарита. Наследуется от абстрактного класса Pizza.
    На вход подаем размер - L, XL. По умоланию размер L.
    """
    def __init__(self, pizza_size='L'):
        """
        Инициализируем пиццу
        """
        self.name = 'Margherita'
        self.recipe = ['tomato sauce', 'mozzarella', 'tomatoes']
        if pizza_size not in ['L', 'XL']:
            raise ValueError('Size should be either L or XL')
        else:
            self.pizza_size = pizza_size
        self.emoji = '\U0001F9C0'

    def dict(self):
        """
        Возвращает словарь {название пиццы: рецепт}
        """
        return {self.name: self.recipe}

    def __eq__(self, other):
        """
        Сравниваем пиццы, если на вход подается не Маргарита - выбрасываем ошибку.
        Если не совпали размер и/или рецепт Маргарит, то пиццы не равны.
        """
        if not isinstance(other, Margherita):
            raise TypeError('The second pizza is not a Margherita')
        if self.pizza_size != other.pizza_size or self.recipe != other.recipe:
            return False
        return True


class Pepperoni(Pizza):
    """
    Класс для пиццы Пепперони. Наследуется от абстрактного класса Pizza.
    На вход подаем размер - L, XL. По умоланию размер L.
    """
    def __init__(self, pizza_size='L'):
        """
        Инициализируем пиццу
        """
        self.name = 'Pepperoni'
        self.recipe = ['tomato sauce', 'mozzarella', 'pepperoni']
        if pizza_size not in ['L', 'XL']:
            raise ValueError('Size should be either L or XL')
        else:
            self.pizza_size = pizza_size
        self.emoji = '\U0001F355'

    def dict(self):
        """
        Возвращает словарь {название пиццы: рецепт}
        """
        return {self.name: self.recipe}

    def __eq__(self, other):
        """
        Сравниваем пиццы, если на вход подается не Пепперони - выбрасываем ошибку.
        Если не совпали размер и/или рецепт Пепперони, то пиццы не равны.
        """
        if not isinstance(other, Pepperoni):
            raise TypeError('The second pizza is not a Pepperoni')
        if self.pizza_size != other.pizza_size or self.recipe != other.recipe:
            return False
        return True


class Hawaiian(Pizza):
    """
    Класс для гавайской пицы. Наследуется от абстрактного класса Pizza.
    На вход подаем размер - L, XL. По умоланию размер L.
    """
    def __init__(self, pizza_size='L'):
        self.name = 'Hawaiian'
        self.recipe = ['tomato sauce', 'chicken', 'pineapples']
        if pizza_size not in ['L', 'XL']:
            raise ValueError('Size should be either L or XL')
        else:
            self.pizza_size = pizza_size
        self.emoji = '\U0001F34D'

    def dict(self):
        """Возвращает словарь {название пиццы: рецепт}"""
        return {self.name: self.recipe}

    def __eq__(self, other):
        """
        Сравниваем пиццы, если на вход подается не Гавайская - выбрасываем ошибку.
        Если не совпали размер и/или рецепт Гавайских пицц, то пиццы не равны.
        """
        if not isinstance(other, Hawaiian):
            raise TypeError('The second pizza is not a Hawaiian')
        if self.pizza_size != other.pizza_size or self.recipe != other.recipe:
            return False
        return True


def log(log_message: str):
    """
    Декоратор выводит текст приготовления/доставки/самовывоза и времени, за которое было выполнено действие.
    Время задается через randint, зависит от размера пиццы: для XL приготовление требует больше времени.
    """
    def decorator(function):
        def wrapper(*args, **kwargs):
            if not isinstance(log_message, str):
                raise TypeError('The decorator accepts only strings')
            for pizza in args:
                if not hasattr(pizza, 'pizza_size'):
                    raise AttributeError('Check that your pizza has a size')
                if pizza.pizza_size == 'L':
                    time = randint(2, 10)
                    print(log_message.format(time))
                else:
                    time_bakery = randint(11, 20)
                    time_del = randint(2, 10)
                    if function.__name__ == 'bake':
                        print(log_message.format(time_bakery))
                    else:
                        print(log_message.format(time_del))
            return function(*args, **kwargs)
        return wrapper
    return decorator


@log('\U0001F9D1 Приготовили за {} с!')
def bake(pizza):
    """Готовит пиццу"""
    return pizza


@log('\U0001F6F5 Доставили за {} с!')
def deliver(pizza):
    """Доставляет пиццу"""
    return pizza


@log('\U0001F3E0 Забрали за {} с!')
def pick_up(pizza):
    """Забирает пиццу"""
    return pizza


@click.group()
def cli():
    pass


@cli.command()
def menu():
    """
    Выводит меню для доступных пицц.
    """
    pizzas = [Margherita(), Pepperoni(), Hawaiian()]
    for pizza in pizzas:
        print('- {} {}: {}'.format(pizza.name, pizza.emoji, ', '.join(pizza.recipe)))


def order_routines(pizza, delivery: bool, pickup: bool):
    """
    Вспомогательная функция, которая готовит, доставляет и забирает пиццу.
    """
    bake(pizza)
    if delivery:
        deliver(pizza)
    if pickup:
        pick_up(pizza)


@cli.command()
@click.option('--size', default='L', type=str)
@click.option('--delivery', default=False, is_flag=True)
@click.option('--pickup', default=False, is_flag=True)
@click.argument('pizza', nargs=1)
def order(pizza: str, delivery: bool, pickup: bool, size: str):
    """Готовит и доставляет пиццу.
    Вызывается с названием пиццы: Margherita, Pepperoni, Hawaiian
    Есть опция доставки --delivery
    Есть опция самодоставки --pickup
    Есть опция выбора размера: --size L/ --size XL, по умолчанию L"""
    if pickup and delivery:
        raise IOError('Выберите либо доставку, либо самодоставку')
    if size not in ['L', 'XL']:
        raise IOError('Извините, мы делаем и доставляем пиццы следующих размеров: L и XL')
    if pizza.capitalize() == 'Pepperoni':
        order_routines(Pepperoni(pizza_size=size), delivery, pickup)
    elif pizza.capitalize() == 'Margherita':
        order_routines(Margherita(pizza_size=size), delivery, pickup)
    elif pizza.capitalize() == 'Hawaiian':
        order_routines(Hawaiian(pizza_size=size), delivery, pickup)
    else:
        raise IOError('Извините, на данный момент мы готовим и доставляем только следующие пиццы: \n'
                      '- Маргариту (Margherita) \n'
                      '- Пепперони (Pepperoni) \n'
                      '- Гавайскую (Hawaiian)')


if __name__ == '__main__':
    cli()
