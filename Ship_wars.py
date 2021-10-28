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
        self.field = [["O"]*size for i in range(size)]
        self.busy = []
        self.ships = []

    def add_ship(self, ship):
       for i in ship.dots:
           if self.out(i) or i in self.busy:
               raise WrongRangeShipException()
    for i in ship.dots:
        self.field[i.x][i.y] = "■"
        self.busy.append(i)
        self.ships.append(ship)
        self.contur(ship)

    def contur(self, ship, verb = False ):
        near = [(-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)]
        for i in ship.dots:
            for ix, iy in near:
                cur = dot(i.x + ix, d.y + dy )
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
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[a.x][a.y] = "."
        print("Мимо!")
        return False

    def begin(self):
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
        a = Dot(randit(0, 5), randint(0, 5))
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



class game:
    pass


print(asdasda)
