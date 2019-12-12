import math


class Asteroid:
    """
    Class of Asteroid objects, contains the coordinates of the asteroid, the
    speed and the asteroid's size.
    This class contains functions that return an information about the
    asteroid, and functions that change the asteroid's attributes if needed.
    """

    def __init__(self, x_coor, x_speed, y_coor, y_speed, size):
        """
        Initialize a new Asteroid object.
        :param x_coor: x axis coordinate
        :param x_speed: x axis speed
        :param y_coor: y axis coordinate
        :param y_speed: y axis speed
        :param size: the size of the asteroid
        """
        self.__x_coor = x_coor
        self.__x_speed = x_speed
        self.__y_coor = y_coor
        self.__y_speed = y_speed
        self.__size = size

    def get_coor(self):
        """
        :return: a tuple of the ship's coordinates.
        """
        return self.__x_coor, self.__y_coor

    def set_coor(self, new_coor):
        """
        Change the current coordinates to the new coordinates.
        :param new_coor: a tuple of coordinates the user want to change the
        asteroid coordinates to.
        :return: None
        """
        self.__x_coor, self.__y_coor = new_coor

    def get_speed(self):
        """
        :return: a tuple of the asteroid's speed in both axises
        """
        return self.__x_speed, self.__y_speed

    def get_size(self):
        """
        :return: the size of the asteroid.
        """
        return self.__size

    def get_radius(self):
        """
        :return: the radius of the asteroid.
        """
        radius = self.__size * 10 - 5
        return radius

    def has_intersection(self, obj):
        """
        Checks if their was an intersection between the asteroid and the
        object, by checking the distance between them.
        :param obj: another object (ship or torpedo).
        :return: True if their was an intersection between the asteroid and the
        object, and False if their wasn't.
        """
        distance = math.sqrt((obj.get_coor()[0] - self.__x_coor) ** 2 +
                             (obj.get_coor()[1] - self.__y_coor) ** 2)
        if distance <= self.get_radius() + obj.get_radius():
            return True
        return False
