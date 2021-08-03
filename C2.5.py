# C2.5. Итоговое практическое задание
class Dot:
    # Прием параметров х и у для координат точек
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Данный метод сравнивает объекты класса "Dot" и выдает True при равенстве
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # Метод для вывода точки в консоль
    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

# Создание собственных исключений
# создание класса для доски (Родительский класс - исключение)
class BoardException(Exception):
    pass
# Создание исключения для выстрела за доску
# Это дочерний класс от класса исключение для доски
# Его метод выводит пользователю сообщение о выходе за доску
class OutBoardException(BoardException):
    def __str__(self):
        return "Координаты вашего выстрела за пределами поля"

# Так же дочерний класс для сообщения о повторном выстреле в точку
class RepeatBoardException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

# Класс для внутренней логики при размещении кораблей на доске
class WrongPositionOnBoardException(BoardException):
    pass

class Ship:
    # Инициализация корабля
    # Создание основных атрибутов корабля:
    # bow - задается нос корабля
    # о - положение корабля (Вертикальное/Горизонтальное)
    # l - длина корабля, а длина это еще и жизни
    def __init__(self, bow, o, l):
        self.bow = bow
        self.o = o
        self.l = l
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x
            cur_y = self.bow.y

            # Горизонтальное положение корабля
            if self.o == 0:
                cur_x += i
            # Вертикальное положение корабля
            elif self.o == 1:
                cur_y += i
            # добавление точек в список
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    # Показывает попадание в корабль
    def shooten(self, shot):
        return shot in self.dots

# Создание класса игрового поля (Доска)
class Board:
    # определяется видимость поля и его размер
    def __init__(self, hid = False, size = 6):
        # видимость поля
        self.hid = hid
        # размер поля
        self.size = size

        # создание самой игровой сетки
        self.field = [[" "] * size for i in range(size)]

        # кол-во пораженных кораблей
        self.count = 0

        # список кораблей на доске
        self.ships = []

        # хранит точки, которые использованы (выстрелом или кораблем с контуром)
        self.busy = []

    # метод вывода корабля на доску
    def __str__(self):
        # в эту переменную записывается вся доска
        res = ""
        res += "    1   2   3   4   5   6  "
        # формирование внешнего вида строк доски
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        # Если доска скрыта, то меняется символ корабля на символ пустой клетки
        if self.hid:
            res = res.replace("■", " ")
        return res

    # проверка принадлежности точки к доске
    def out(self, d):
        # Если точка не в интервале от 0 до размера доски (по х и по у)
        # то вернется ложь
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    # Создание контура корабля
    # verb - определяет необходимость вывода контура
    def contour(self, ship, verb = False):
        # Создание списка точек, которые занимают все клетки
        # в радиусе 1 от каждой точки корабля.
        # (0, 0) - это точка корабля.
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                # если точка в пределах поля и не в списке занятых
                if not(self.out(cur)) and cur not in self.busy:
                    # и если контур видемый
                    if verb:
                        # то в клетки записывается символ "*"
                        self.field[cur.x][cur.y] = "*"
                    # добавление точки в список занятых,
                    # видимость контура не влияет на это условие
                    self.busy.append(cur)

    # Метод добавления корабля на доску
    def add_ship(self, ship):
        # Для точек корабля
        for d in ship.dots:
            # Если точка за пределами доски или занята
            if self.out(d) or d in self.busy:
                # то вылавливается исключение
                raise WrongPositionOnBoardException()
        # Для точек корабля (После проверки на исключение)
        for d in ship.dots:
            # присваивается символ ■
            self.field[d.x][d.y] = "■"
            # и точка добавляется в список занятых
            self.busy.append(d)

        # корабль добавляется в список кораблей на доске
        self.ships.append(ship)
        # и для корабля создается контур
        self.contour(ship)

    # Выстрел
    def shot(self, d):
        # Если введенная точка за полем - активируется исключение
        if self.out(d):
            raise OutBoardException()

        # Если введенная точка входит в список занятых, так же исключение
        if d in self.busy:
            raise RepeatBoardException()
        # Если не возникло исключений то точка добавляется в список занятых
        self.busy.append(d)

        for ship in self.ships:
            # Если точка входит в точки корабля, то это попадание
            if ship.shooten(d):
                # Уменьшается жизнь
                ship.lives -= 1
                # В место попадания ставится "Х"
                self.field[d.x][d.y] = "X"
                # Если жизни кончались
                if ship.lives == 0:
                    # Увеличивается счетчик уничтоженных кораблей
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True
        self.field[d.x][d.y] = "*"
        print("Мимо!")
        return False

    def begin(self):
         self.busy = []


b = Board()
b.add_ship(Ship(Dot(1, 2), 0, 3))
print(b.busy)


