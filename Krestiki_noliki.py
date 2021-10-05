
# Приветствие
def info():
    print("     ИГРА")
    print("Крестики нолики")
    print("Во время игры необходимо вводить координаты от 0 до 2 ")
    print("первая координата это столбец, ")
    print("вторая координата это строка  ")

map_game =[["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]   #Поле для игры

def show_map():                                 #Поле для игры
    print("  0 1 2")
    for i in range(len(map_game)):
        print(str(i), *map_game[i])


def hod():                              #Ввод координат с проверкой на числа и отсутствие других символов
    while True:
        cords = input(" Введите координаты :").split()
        if len(cords) != 2:
            print("Введите 2 координаты!")
            continue

        x, y = cords

        if not(x.isdigit()) or not(y.isdigit()):
            print("Введите числа!")
            continue

        x, y = int(x), int(y)


        if 0 <= x <= 2 and 0 <= y <= 2:
            if map_game[x][y] == "-":
                return x, y
            else:
                print(" клетка занята, введите другие координаты!")
        else:
            print("Введите координаты от 0 до 2")

def check_pobed():              #Проверка выйгрышных вариантов
    var_win = [((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
               ((0, 2), (1, 1), (2, 0)), ((0, 0), (1, 1), (2, 2)), ((0, 0), (1, 0), (2, 0)),
               ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2))]

    for i in var_win:
        a = i[0]
        b = i[1]
        c = i[2]

        if map_game[a[0]][a[1]] == map_game[b[0]][b[1]] == map_game[c[0]][c[1]] != "-":
            print(f"Выиграл {map_game[a[0]][a[1]]}!")
            return True
    return False



def game():         # цикл игры
    num = 0
    while True:
        num += 1

        show_map()

        if num % 2 == 1:
            print("Ходит крестик")
        else:
            print("Ходит нолик")

        x, y = hod()

        if num % 2 == 1:
            map_game[x][y] = "X"
        else:
            map_game[x][y] = "0"
        if check_pobed():
            break

        if num == 9:

            print("Ничья")
            break



def main():
    info()
    game()

main()
