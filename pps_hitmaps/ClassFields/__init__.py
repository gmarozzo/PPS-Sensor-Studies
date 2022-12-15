
class IntField:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value:int):
        if not isinstance(value, int):
            raise ValueError(f'expecting integer in {self.name}')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

class PositiveIntField:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value:int):
        if not isinstance(value, int):
            raise ValueError(f'expecting integer in {self.name}')
        if value <= 0:
            raise ValueError(f'expecting a positive integer in {self.name}')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

class NonNegativeIntField:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value:int):
        if not isinstance(value, int):
            raise ValueError(f'expecting integer in {self.name}')
        if value < 0:
            raise ValueError(f'expecting a positive integer in {self.name}')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

class FloatField:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value:float):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise ValueError(f'expecting float in {self.name}')
        instance.__dict__[self.name] = float(value)

    def __set_name__(self, owner, name):
        self.name = name

class ListField:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value:list):
        if not isinstance(value, list):
            raise ValueError(f'expecting list in {self.name}')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

class FloatListField:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value:list):
        if not isinstance(value, list):
            raise ValueError(f'expecting list in {self.name}')
        if not (all(isinstance(x, float) or isinstance(x, int) for x in value)):
            raise ValueError(f'expecting list of floats in {self.name}')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

class FloatPairListField:
    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value:list):
        if not isinstance(value, list):
            raise ValueError(f'expecting list in {self.name}')
        if not all(isinstance(x, tuple) for x in value):
            raise ValueError(f'expecting list of tuples in {self.name}')
        if not all(isinstance(x, float) or isinstance(x, int) for x in [item for y in value for item in y]):
            raise ValueError(f'expecting list of tuples of floats in {self.name}')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name

__all__ = ["IntField", "PositiveIntField", "NonNegativeIntField", "FloatField", "ListField", "FloatListField", "FloatPairListField"]