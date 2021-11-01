from random import randint


class BoardException(Exception):
    pass

class OutOfBoardException(BoardException):
    def __str__(self):
        return 'Вы стреляете мимо поля'

class WrongShotException(BoardException):
    def __str__(self):
        return 'Вы сюда уже стреляли!'

class WrongRangeShipException(BoardException):
    pass


def show():
    return  print('Добро пожаловать в игру "Морской Бой"\n'
                  '     Правила игры стандартные        \n'
                  'Управление с помощью координат X и Y \n'
                  '     X - номер строки                \n'
                  '     Y - номер столбца               ')



class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"{self.x}, {self.y} "


class Ship:
    def __init__(self, nose, hp, pol):
        self.nose = nose
        self.hp = hp
        self.pol = pol
        self.lives = hp

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.hp):
            cur_x = self.nose.x
            cur_y = self.nose.y

            if self.pol == 0:
                cur_x += i

            elif self.pol == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shoot(self, shot):
        return shot in self.dots


class Board:

    def __init__(self, hid = False, size = 6):
        self.hid = hid
        self.size = size
        self.field = [["O"]*size for _ in range(size)]
        self.busy = []
        self.ships = []
        self.schet = 0
    def add_ship(self, ship):
       for a in ship.dots:
           if self.out(a) or a in self.busy:
               raise WrongRangeShipException()

       for a in ship.dots:

            self.field[a.x][a.y] = "■"
            self.busy.append(a)
            self.ships.append(ship)
            self.contur(ship)

    def contur(self, ship, verb = False ):
        near = [(-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)]
        for a in ship.dots:
            for ax, ay in near:
                cur = Dot(a.x + ax, a.y + ay )
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)
    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, a):
        return not((0 <= a.x < self.size) and (0 <= a.y < self.size))

    def shot(self, a):
        if self.out(a):
            raise OutOfBoardException()
        if a in self.busy:
            raise WrongShotException()

        self.busy.append(a)

        for ship in self.ships:
            if a in ship.dots:
                ship.lives -= 1
                self.field[a.x][a.y] = "X"
                if ship.lives == 0:
                    self.schet += 1
                    self.contur(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[a.x][a.y] = "."
        print("Мимо!")
        return False

    def begin(self):  #после расстановки кораблей обнуляется список для контроля выстрелов
        self.busy = []


class Player:                           #надо потестить.. чет
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        a = Dot(randint(0, 5), randint(0, 5))
        print(f'Ходит компьютер :{a.x + 1}  {a.y + 1}')
        return a


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)



class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        comp = self.random_board()
        comp.hid = True

        self.ai = AI(comp, pl)
        self.us = User(pl, comp)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_ships()
        return board

    def random_ships(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 500:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except WrongRangeShipException:
                    pass
        board.begin()

        return board

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.schet == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.schet == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        show()
        self.loop()





start_game = Game()
start_game.start()






