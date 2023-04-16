from enum import Enum


class Status(Enum):
    """
    Represents the authentication status codes that a user can have. Each status code is assigned a unique integer value.
    """

    UNAUTHORIZED = 0
    AUTHORIZED = 1
    LOGGED_IN = 11
    LOGGED_OUT = 21

    def __and__(self, other):
        return self.value & other.value


class Occurs(Enum):
    """
    Represents the possible occurrences of an element in a document. Each occurrence is assigned a unique integer value.
    """
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
        """
        Converts a string to an Occurs enum.

        @param label: (str) the occurs symbol from the template to convert
        @return: (Occurs) the corresponding Occurs enum
        """

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
