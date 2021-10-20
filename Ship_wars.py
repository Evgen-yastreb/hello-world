
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

