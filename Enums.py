from enum import Enum


class Status(Enum):
    UNAUTHORIZED = 0
    AUTHORIZED = 1
    LOGGED_IN = 11
    LOGGED_OUT = 21

    def __and__(self, other):
        return self.value & other.value


class Occurs(Enum):
    ZERO = 1
    ONE = 10
    MORE = 100
    ZERO_ONE = 11
    ZERO_MORE = 101
    ONE_MORE = 110

    def __and__(self, other):
        return self.value & other.value

    @staticmethod
    def from_str(label):
        if label == "?":
            return Occurs.ZERO_ONE
        elif label == "*":
            return Occurs.ZERO_MORE
        elif label == "1":
            return Occurs.ONE
        elif label == "+":
            return Occurs.ONE_MORE
        else:
            raise NotImplementedError
