from  enum import Enum
import math
from  math import sqrt

class CFieldType(Enum):
    '''
    Enumerator of different field types
    '''
    EMPTY = 0
    WALL = 1
    OPEN = 2
    CLOSED = 3
    GARBAGE = 4
    AGENT = 5
    COLLECTOR = 6


# calss of singe maze cell
class CField():
    '''
    This class holds the implementation of fields on the map
    '''

    def __hash__(self):
        return hash((self.pos_y, self.pos_x))

    def __lt__(self, other):
        return self.pos_x < other.pos_y

    def __eq__(self, other):

        if self.__class__.__name__ == other.__class__.__name__:
            if self.pos_x == other.pos_x and self.pos_y == other.pos_y:
                return True
        return False

    def __init__(self, fieldType):
        '''
        Constructor of the class, creates a new field
        :param fieldType: type of the field
        :type fieldType: CFieldType
        '''
        self.my_type = fieldType
        self.neighbours = []
        self.pos_x = 0
        self.pos_y = 0
        self.distance = 0

    def set_pos_x(self, posX: int) -> None:
        '''
        Setter of a X coordinates of field
        :param posX: X coord of a field
        :type posX: int
        :return: None
        '''
        self.pos_x = posX

    def set_pos_y(self, posY: int) -> None:
        '''
        Setter of a Y coordinates of field
        :param posY: Y coord of a field
        :type posY: int
        :return: None
        '''
        self.pos_y = posY

    def get_pos_x(self) -> int:
        '''
        Getter of a X coordinates of field
        :return: X coord of a field
        :rtype: int
        '''
        return self.pos_x

    def get_pos_y(self) -> int:
        '''
       Getter of a Y coordinates of field
       :return: Y coord of a field
       :rtype: int
       '''
        return self.pos_y

    def set_type(self, type: CFieldType):
        '''
        Setter of a type of field
        :param type: New type of the field
        :type type: CFieldType
        :return: None
        '''
        self.my_type = type

    def get_type(self) -> CFieldType:
        '''
        Getter of a X coordinates of field
        :return: Type of the field
        :rtype: CFieldType
        '''
        return self.my_type

    def save_neighbour(self, neighbour) -> None:
        '''
        Saves the information about neighbouring fields
        :param neighbour: The neighbouring field
        :type: CField
        :return: None
        '''
        self.neighbours.append(neighbour)

    def __str__(self) -> str:
        return '[' + str(self.pos_y) + ',' + str(self.pos_x) + ']'


def count_euclidean_distance_of_fields(field_a: CField, field_b: CField) -> float:
    '''
    Counts the distance of two given fields
    :return: Euclidean distance of two fields
    :rtype: float
    '''
    return sqrt(math.pow(field_a.pos_x - field_b.pos_x, 2) + math.pow(field_a.pos_y - field_b.pos_y, 2))
