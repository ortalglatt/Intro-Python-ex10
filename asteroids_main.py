from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import sys
import random
import math

DEFAULT_ASTEROIDS_NUM = 5
DEF_AST_SIZE = 3


class GameRunner:
    """
    Class of GameRunner objects, contains all the attributes a game need for
    it's run.
    This class contains all the functions that needed to run a whole game, and
    the function that runs the game.
    """

    AST_MAX_SPEED = 4
    AST_MIN_SPEED = 1
    MAX_TORPEDOS = 10
    MAX_SPECIAL_TORPEDOS = 5
    MAX_LIFE_TIME = 200
    SPECIAL_MAX_LIFE_TIME = 150
    SPECIAL_TORPEDOS_AMOUNT = 8
    SHIP_LIFE = 3
    SCORE = {3: 20, 2: 50, 1: 100}
    COL_MSG = ("Collision!", "You hit an asteroid! You've got one less lives. "
                             "Be careful!")
    WIN_MSG = ("Winner!", "Good job! you won the game :)")
    EXIT_MSG = ("Exit", "See you next time!")
    GAME_OVER_MSG = ("Game Over", "You ran out of lives :(")

    def __init__(self, asteroids_amount=DEFAULT_ASTEROIDS_NUM):
        """
        Initialize a new GameRunner object.
        :param asteroids_amount: the amount of asteroids in the beginning of
        the game (default number).
        """
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        self.__ship = self.__add_ship()
        self.__asteroids = []
        self.__add_asteroids(asteroids_amount)
        self.__torpedos = {}
        self.__special_torpedos = {}
        self.__lives = self.SHIP_LIFE
        self.__score = 0

    def __add_ship(self):
        """
        Adds a new ship object with random coordinates, speed 0 in both axises
        and direction 0, and put the ship on the screen.
        :return: the object of the ship
        """
        x = random.randint(self.__screen_min_x, self.__screen_max_x)
        y = random.randint(self.__screen_min_y, self.__screen_max_y)
        ship = Ship(x, 0, y, 0, 0)
        self.__screen.draw_ship(x, y, 0)
        return ship

    def __add_asteroids(self, asteroids_amount):
        """
        Adds an amount of asteroids objects with random coordinates, random
        speed and default size, make sure that their is enough distance between
        the asteroids and the ship, and put the asteroids on the screen.
        :param asteroids_amount: the amount of the asteroids you want to add to
        the game.
        :return: None
        """
        for ast in range(asteroids_amount):
            x = random.randint(self.__screen_min_x, self.__screen_max_x)
            y = random.randint(self.__screen_min_y, self.__screen_max_y)
            x_speed = random.randint(self.AST_MIN_SPEED, self.AST_MAX_SPEED)
            y_speed = random.randint(self.AST_MIN_SPEED, self.AST_MAX_SPEED)
            asteroid_to_add = Asteroid(x, x_speed, y, y_speed, DEF_AST_SIZE)
            # The while loop makes sure that the asteroid is not on the ship.
            while asteroid_to_add.has_intersection(self.__ship):
                x = random.randint(self.__screen_min_x, self.__screen_max_x)
                y = random.randint(self.__screen_min_y, self.__screen_max_y)
                asteroid_to_add = Asteroid(x, x_speed, y, y_speed,
                                           DEF_AST_SIZE)
            self.__add_ast_on_screen(asteroid_to_add)

    def __add_ast_on_screen(self, ast):
        """
        Adds the given asteroid to the screen.
        :param ast: an asteroid object
        :return: None
        """
        self.__screen.register_asteroid(ast, ast.get_size())
        self.__asteroids.append(ast)
        self.__screen.draw_asteroid(ast, ast.get_coor()[0], ast.get_coor()[1])

    def __add_torpedo(self):
        """
        Adds torpedo to the screen, with the ship's direction and a speed that
        calculates by the ship's speed and direction. The function will also
        add the torpedo to the torpedos dictionary with a life-time counter
        that starts with zero.
        :return: None
        """
        ship_dir = math.radians(self.__ship.get_direction())
        x_speed = self.__ship.get_speed()[0] + 2 * math.cos(ship_dir)
        y_speed = self.__ship.get_speed()[1] + 2 * math.sin(ship_dir)
        x_coor, y_coor = self.__ship.get_coor()
        tor_to_add = Torpedo(x_coor, x_speed, y_coor, y_speed,
                             self.__ship.get_direction())
        self.__torpedos[tor_to_add] = 0
        self.__screen.register_torpedo(tor_to_add)
        self.__screen.draw_torpedo(tor_to_add, x_coor, y_coor,
                                   self.__ship.get_direction())

    def __add_special_torpedo(self):
        """
        Adds special torpedo - a default amount of regular torpedos, that will
        be around the ship, will move with it, and will turn around themselves.
        The function will add every torpedo to the screen, and to the special
        torpedos dictionary with it's life-time counter and it's original
        direction.
        :return: None
        """
        for i in range(self.SPECIAL_TORPEDOS_AMOUNT):
            direction = self.__ship.get_direction() + \
                        (i * (360 / self.SPECIAL_TORPEDOS_AMOUNT))
            dir_in_rad = math.radians(direction)
            x_speed = self.__ship.get_speed()[0] + 2 * math.cos(dir_in_rad)
            y_speed = self.__ship.get_speed()[1] + 2 * math.sin(dir_in_rad)
            x_coor, y_coor = self.__ship.get_coor()
            special_tor = Torpedo(x_coor, x_speed, y_coor, y_speed, direction)
            self.__special_torpedos[special_tor] = [0, dir_in_rad]
            self.__screen.register_torpedo(special_tor)
            self.__screen.draw_torpedo(special_tor, x_coor, y_coor, direction)

    def __move_object(self, obj):
        """
        Moves the object, by changing it's coordinates in both axises.
        :param obj: an object of one of the classes (ship, torpedo, asteroid).
        :return: None
        """
        delta_x = self.__screen_max_x - self.__screen_min_x
        delta_y = self.__screen_max_y - self.__screen_min_y
        new_coor_x = (obj.get_speed()[0] + obj.get_coor()[0] -
                      self.__screen_min_x) % delta_x + self.__screen_min_x
        new_coor_y = (obj.get_speed()[1] + obj.get_coor()[1] -
                      self.__screen_min_y) % delta_y + self.__screen_min_y
        obj.set_coor((new_coor_x, new_coor_y))

    def __update_ship(self):
        """
        Update the ship by putting it on the screen with the current
        attributes.
        :return: None
        """
        self.__screen.draw_ship(self.__ship.get_coor()[0],
                                self.__ship.get_coor()[1],
                                self.__ship.get_direction())

    def __ship_hit_asteroid(self):
        """
        Checks if the ship crushed into one of the asteroids on the screen.
        If it did, the function will remove one life of the ship's lives and
        remove the steroid.
        :return: None
        """
        ast_to_remove = None
        for ast in self.__asteroids:
            if ast.has_intersection(self.__ship):
                ast_to_remove = ast
                if self.__lives > 1:
                    self.__screen.show_message(self.COL_MSG[0],
                                               self.COL_MSG[1])
                    break
        if ast_to_remove:
            self.__lives -= 1
            self.__screen.remove_life()
            self.__remove_asteroid(ast_to_remove)

    def __ship_teleport(self):
        """
        Teleports the ship to another coordinates on the screen, and make sure
        it won't be on an asteroid.
        :return: None
        """
        x_coor = random.randint(self.__screen_min_x, self.__screen_max_x)
        y_coor = random.randint(self.__screen_min_y, self.__screen_max_y)
        self.__ship.set_coor((x_coor, y_coor))
        for ast in self.__asteroids:
            # The while loop makes sure that the ship won't be on an asteroid.
            while ast.has_intersection(self.__ship):
                x_coor = random.randint(self.__screen_min_x,
                                        self.__screen_max_x)
                y_coor = random.randint(self.__screen_min_y,
                                        self.__screen_max_y)
                self.__ship.set_coor((x_coor, y_coor))

    def __move_asteroids(self):
        """
        Moves all the asteroids on the screen.
        :return: None
        """
        for ast in self.__asteroids:
            self.__move_object(ast)
            self.__screen.draw_asteroid(ast, ast.get_coor()[0],
                                        ast.get_coor()[1])

    def __change_asteroid(self, tor, ast):
        """
        Adds two new asteroids instead the one that the torpedo hit.
        The new asteroids will be with smaller size, new speed that calculates
        by the torpedo's speed and the original asteroid's speed.
        :param tor: the torpedo that hit the asteroid
        :param ast: the asteroid that the torpedo hit, and need to be replaced.
        :return: None
        """
        new_size = ast.get_size() - 1
        x, y = ast.get_coor()
        ast_speed = ast.get_speed()
        speed_av = math.sqrt(ast_speed[0] ** 2 + ast_speed[1] ** 2)
        x_speed_1 = (tor.get_speed()[0] + ast_speed[0]) / speed_av
        y_speed_1 = (tor.get_speed()[1] + ast_speed[1]) / speed_av
        x_speed_2 = (tor.get_speed()[0] - ast_speed[0]) / speed_av
        y_speed_2 = (tor.get_speed()[1] - ast_speed[1]) / speed_av
        asteroid_1 = Asteroid(x, x_speed_1, y, y_speed_1, new_size)
        asteroid_2 = Asteroid(x, x_speed_2, y, y_speed_2, new_size)
        self.__add_ast_on_screen(asteroid_1)
        self.__add_ast_on_screen(asteroid_2)

    def __remove_asteroid(self, ast):
        """
        Remove the given asteroid from the screen, and updates the asteroids
        list.
        :param ast: the asteroid the user want to remove
        :return: None
        """
        self.__screen.unregister_asteroid(ast)
        new_asteroids_lst = []
        for ast_obj in self.__asteroids:
            if ast is not ast_obj:
                new_asteroids_lst.append(ast_obj)
        self.__asteroids = new_asteroids_lst

    def __move_torpedos(self):
        """
        Moves all the torpedos on the screen. This function will delete every
        torpedo that it's life-time arrived to the maximum, and will add 1 to
        any other torpedo's counter.
        :return: None
        """
        for tor in self.__torpedos:
            self.__move_object(tor)
            self.__screen.draw_torpedo(tor, tor.get_coor()[0],
                                       tor.get_coor()[1], tor.get_direction())
            # Checks if the torpedo's life-time arrived to the maximum.
            if self.__torpedos[tor] == self.MAX_LIFE_TIME:
                self.__remove_torpedo(tor)
            else:
                self.__torpedos[tor] += 1

    def __move_special_torpedos(self):
        """
        Moves all the special torpedos to there original direction and also
        with the ship (so they will always will be around the ship).
        The function will also remove the torpedo if it arrived to the maximum
        life-time, and will add 1 to every other torpedo's life-time counter.
        :return: None
        """
        for tor in self.__special_torpedos:
            cur_dir = self.__special_torpedos[tor][1]
            x_speed = self.__ship.get_speed()[0] + 2 * math.cos(cur_dir)
            y_speed = self.__ship.get_speed()[1] + 2 * math.sin(cur_dir)
            tor.set_speed((x_speed, y_speed))
            self.__move_object(tor)
            new_dir = tor.get_direction() + 5
            tor.set_direction(new_dir)
            self.__screen.draw_torpedo(tor, tor.get_coor()[0],
                                       tor.get_coor()[1], tor.get_direction())
            # Checks if the torpedo's life-time arrived to the maximum.
            if self.__special_torpedos[tor][0] == self.SPECIAL_MAX_LIFE_TIME:
                self.__remove_torpedo(tor)
            else:
                self.__special_torpedos[tor][0] += 1

    def __remove_torpedo(self, tor):
        """
        Remove the torpedo from the screen and from the dictionary it appears
        in (regular torpedos or special torpedos).
        :param tor: the torpedo the user wants to remove.
        :return: None
        """
        new_torpedos_dic = {}
        # Checks if it is a regular torpedo.
        if tor in self.__torpedos:
            for tor_obj in self.__torpedos:
                if tor is not tor_obj:
                    new_torpedos_dic[tor_obj] = self.__torpedos[tor_obj]
            self.__torpedos = new_torpedos_dic
        # checks if it is a special torpedo.
        elif tor in self.__special_torpedos:
            for tor_obj in self.__special_torpedos:
                if tor is not tor_obj:
                    new_torpedos_dic[tor_obj] = self.__special_torpedos[
                        tor_obj]
            self.__special_torpedos = new_torpedos_dic
        self.__screen.unregister_torpedo(tor)

    def __check_torpedo_hit_asteroid(self, torpedos_dic):
        """
        checks if one of the torpedos in the given dictionary hit one of the
        asteroid on the screen. If thir is a torpedo that hit an asteroid, the
        function will remove the asteroid and the torpedo from the screen, will
        add new asteroids as needed and will update the score.
        :param torpedos_dic: the torpedo's dictionary (regular torpedos or
        special torpedos) the user want to check if one of them hit an
        asteroid.
        :return:
        """
        tor_to_remove, ast_to_remove = None, None
        for tor in torpedos_dic:
            for ast in self.__asteroids:
                if ast.has_intersection(tor):
                    tor_to_remove, ast_to_remove = tor, ast
                    # if the asteroid has the smallest size, we don't need to
                    # add new asteroids instead.
                    if ast.get_size() > 1:
                        self.__change_asteroid(tor_to_remove, ast_to_remove)
                        break
        if tor_to_remove:
            self.__score += self.SCORE[ast_to_remove.get_size()]
            self.__screen.set_score(self.__score)
            self.__remove_asteroid(ast_to_remove)
            self.__remove_torpedo(tor_to_remove)

    def __torpedo_hit_asteroid(self):
        """
        Checks if one of all the torpedos - regular and special - hit an
        asteroid.
        :return: None
        """
        self.__check_torpedo_hit_asteroid(self.__torpedos)
        self.__check_torpedo_hit_asteroid(self.__special_torpedos)

    def __clicks_control(self):
        """
        Checks which the user pressed and respond for that key.
        Up - accelerate the ship's speed.
        Right - turn the ship right.
        Left - turn the ship left.
        "t" - teleport the ship.
        Space - make a regular torpedo.
        "s" - make a spacial torpedo.
        :return: None
        """
        if self.__screen.is_up_pressed():
            self.__ship.speed_up()
            self.__update_ship()
        if self.__screen.is_right_pressed():
            self.__ship.turn_ship_right()
            self.__update_ship()
        if self.__screen.is_left_pressed():
            self.__ship.turn_ship_left()
            self.__update_ship()
        if self.__screen.is_teleport_pressed():
            self.__ship_teleport()
            self.__update_ship()
        if self.__screen.is_space_pressed() and len(self.__torpedos) < \
                self.MAX_TORPEDOS:
            self.__add_torpedo()
        if self.__screen.is_special_pressed() and len(self.__special_torpedos)\
                < self.MAX_SPECIAL_TORPEDOS * self.SPECIAL_TORPEDOS_AMOUNT:
            self.__add_special_torpedo()

    def __end_game(self):
        """
        Checks if the game supposed to end, by checking if their are no more
        lives, if the player hit all the asteroids and if the player want to
        exit. The function will end the game if needed.
        :return: None
        """
        # Checks if the player hit all the asteroids and won the game.
        if len(self.__asteroids) == 0:
            self.__screen.show_message(self.WIN_MSG[0], self.WIN_MSG[1])
            self.__screen.end_game()
            sys.exit()
        # Checks if the player want to stop the game.
        elif self.__screen.should_end():
            self.__screen.show_message(self.EXIT_MSG[0], self.EXIT_MSG[1])
            self.__screen.end_game()
            sys.exit()
        # Checks if their are no more lives.
        elif self.__lives == 0:
            self.__screen.show_message(self.GAME_OVER_MSG[0],
                                       self.GAME_OVER_MSG[1])
            self.__screen.end_game()
            sys.exit()

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        Runs the loops by moving the ship, the asteroids and the torpedos,
        checking what key the player pressed, checking if the ship crushed an
        asteroid and if one of the torpedos hit one of the asteroid, and
        checking if the game supposed to end.
        :return: None
        """
        self.__move_object(self.__ship)
        self.__update_ship()
        self.__move_asteroids()
        self.__move_torpedos()
        self.__move_special_torpedos()
        self.__clicks_control()
        self.__ship_hit_asteroid()
        self.__torpedo_hit_asteroid()
        self.__end_game()


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
