class Torpedo:
    """
    Class of Torpedo objects, contains the coordinates of the torpedo, the
    speed and the direction.
    This class contains functions that return an information about the torpedo,
    and functions that change the torpedo's attributes if needed.
    """

    TORPEDO_RADIUS = 4

    def __init__(self, x_coor, x_speed, y_coor, y_speed, direction):
        """
        Initialize a new Torpedo object.
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
        self.__radius = self.TORPEDO_RADIUS

    def get_coor(self):
        """
        :return: a tuple of the ship's coordinates
        """
        return self.__x_coor, self.__y_coor

    def set_coor(self, new_coor):
        """
        Change the current coordinates to the new coordinates.
        :param new_coor: a tuple of coordinates the user want to change the
        torpedo coordinates to.
        :return: None
        """
        self.__x_coor, self.__y_coor = new_coor

    def set_speed(self, new_speed):
        """
        Change the current speed to the new speed.
        :param new_speed: a tuple of the speed in axis x and axis y that the
        user wants to change the torpedo's speed to.
        :return: None
        """
        self.__x_speed, self.__y_speed = new_speed

    def set_direction(self, new_dir):
        """
        Changes the current direction of the torpedo to the new direction.
        :param new_dir: the direction the user wants to change the torpedo's
        direction to.
        :return: None
        """
        self.__direction = new_dir

    def get_speed(self):
        """
        :return: a tuple of the torpedo's speed in both axises
        """
        return self.__x_speed, self.__y_speed

    def get_direction(self):
        """
        :return: the direction of the torpedo
        """
        return self.__direction

    def get_radius(self):
        """
        :return: the radius of the torpedo
        """
        return self.__radius

