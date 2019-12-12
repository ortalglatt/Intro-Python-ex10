import math


class Ship:
    """
    Class of Ship objects, contains the coordinates of the ship, the speed and
    the direction.
    This class contains functions that return an information about the ship,
    and functions that change the ship's attributes if needed.
    """

    TURN_SHIP = 7
    SHIP_RADIUS = 1

    def __init__(self, x_coor, x_speed, y_coor, y_speed, direction):
        """
        Initialize a new Ship object.
        :param x_coor: x axis coordinate
        :param x_speed: x axis speed
        :param y_coor: y axis coordinate
        :param y_speed: y axis speed
        :param direction: the direction in degrees
        """
        self.__x_coor = x_coor
        self.__x_speed = x_speed
        self.__y_coor = y_coor
        self.__y_speed = y_speed
        self.__direction = direction
        self.__radius = self.SHIP_RADIUS

    def get_coor(self):
        """
        :return: a tuple of the coordinates of the ship
        """
        return self.__x_coor, self.__y_coor

    def set_coor(self, new_coor):
        """
        Change the current coordinates to the new coordinates.
        :param new_coor: a tuple of coordinates the user want to change the
        ship coordinates to.
        :return: None
        """
        self.__x_coor, self.__y_coor = new_coor

    def get_speed(self):
        """
        :return: a tuple of the speed in axis x and axis y of the ship
        """
        return self.__x_speed, self.__y_speed

    def get_direction(self):
        """
        :return: the direction of the ship
        """
        return self.__direction

    def get_radius(self):
        """
        :return: the radius of the ship
        """
        return self.__radius

    def turn_ship_left(self):
        """
        Changes the direction of the ship to the left side.
        :return: None
        """
        self.__direction += self.TURN_SHIP

    def turn_ship_right(self):
        """
        Changes the direction of the ship to the left side.
        :return: None
        """
        self.__direction -= self.TURN_SHIP

    def speed_up(self):
        """
        Accelerates the ship's speed in both axises.
        :return: None
        """
        new_speed_x = self.get_speed()[0] + \
                      math.cos(math.radians(self.__direction))
        new_speed_y = self.get_speed()[1] + \
                      math.sin(math.radians(self.__direction))
        self.__x_speed, self.__y_speed = new_speed_x, new_speed_y
