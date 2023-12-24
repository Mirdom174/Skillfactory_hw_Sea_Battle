import random
import time


class BoardOutException(Exception):
    pass


class Dot:
    def __init__(self, x, y):
        self.x=x
        self.y=y
    def __eq__(self, other):
        if self.x==other.x and self.y==other.y:
            return True


class Ship:
    def __init__(self, dlina, start_dot, napravlenie, zhizni):
        self.dlina=dlina
        self.start_dot=start_dot
        self.napravlenie=napravlenie
        self.zhizni=zhizni
    def dots(self):
        list_of_dots=[self.start_dot]
        if self.dlina>1:
            x, y = self.start_dot
            if self.napravlenie==0:  #горизонтальное направление слева-направо
                for some_dot in range(self.dlina-1):
                    y+=1
                    list_of_dots.append([x,y])
            else: #вертикальное направление сверху-вниз
                for some_dot in range(self.dlina-1):
                    x+=1
                    list_of_dots.append([x,y])
        return list_of_dots


class Board:
    def clear(self):
        self.field = [[' ', 1, 2, 3, 4, 5, 6],
                      [1, '-', '-', '-', '-', '-', '-'],
                      [2, '-', '-', '-', '-', '-', '-'],
                      [3, '-', '-', '-', '-', '-', '-'],
                      [4, '-', '-', '-', '-', '-', '-'],
                      [5, '-', '-', '-', '-', '-', '-'],
                      [6, '-', '-', '-', '-', '-', '-']]
        self.list_of_ships = []
    def __init__(self, hid):
        self.hid = hid
        self.field = [[' ', 1, 2, 3, 4, 5, 6],
                       [1, '-', '-', '-', '-', '-', '-'],
                       [2, '-', '-', '-', '-', '-', '-'],
                       [3, '-', '-', '-', '-', '-', '-'],
                       [4, '-', '-', '-', '-', '-', '-'],
                       [5, '-', '-', '-', '-', '-', '-'],
                       [6, '-', '-', '-', '-', '-', '-']]
        self.list_of_ships = []

    def add_ship(self, some_ship):
        self.list_of_ships.append(some_ship)
        for i, j in some_ship.dots():
                self.field[i][j]='■'

    def contour (self, some_ship):
        list_of_contour=[]
        if some_ship.napravlenie==1: #Вертикальный
            first_iteration=True
            for i, j in some_ship.dots():
                list_of_contour.append([i,j + 1])
                list_of_contour.append([i, j - 1])
                if first_iteration:
                    list_of_contour.append([i - 1, j])
                    list_of_contour.append([i - 1, j - 1])
                    list_of_contour.append([i - 1, j + 1])
                    first_iteration=False
            list_of_contour.append([i + 1, j + 1])
            list_of_contour.append([i + 1, j])
            list_of_contour.append([i + 1, j - 1])
        else:  #Горизонтальный
            first_iteration = True
            for i, j in some_ship.dots():
                list_of_contour.append([i + 1,j])
                list_of_contour.append([i - 1, j])
                if first_iteration:
                    list_of_contour.append([i + 1, j-1])
                    list_of_contour.append([i - 1, j-1])
                    list_of_contour.append([i, j - 1])
                    first_iteration = False
            list_of_contour.append([i + 1, j + 1])
            list_of_contour.append([i - 1, j + 1])
            list_of_contour.append([i, j + 1])
        list_of_contour_uncorrect = []
        for element in list_of_contour:
            for i in element:
                 if i>6 or i<1:
                    list_of_contour_uncorrect.append(element)
        correct_list=[x for x in list_of_contour if x not in list_of_contour_uncorrect]


        return correct_list
    def Shot(self, some_dot):
        if self.field[some_dot.x][some_dot.y]=='■':
            for some_ship in self.list_of_ships:
                if [some_dot.x, some_dot.y] in some_ship.dots():
                    some_ship.zhizni-=1
                    if some_ship.zhizni==0:
                        for x,y in self.contour(some_ship):
                            self.field[x][y] = 'T'
            self.field[some_dot.x][some_dot.y] ='X'
            return True
        if self.field[some_dot.x][some_dot.y]=='-':
            self.field[some_dot.x][some_dot.y] ='T'
            return False
        if (self.field[some_dot.x][some_dot.y]=='T' or
                self.field[some_dot.x][some_dot.y]=='X'):
            raise BoardOutException
    def out(self, some_dot):
        if 7 < some_dot.x < 1 or 7 < some_dot.y < 1:
            return False
        else:
            return True
    def print_field(self):
        if self.hid==0:
            print('Моя доска:')
        else:
            print('Вражеская доска:')
        for row in self.field:
            for element in row:
                if self.hid==0:
                    print(f"{element}", end="  ")
                else:
                    if element == 'T' or element == 'X' :
                        print(f"{element}", end="  ")
                    else:
                        if type(element)==int:
                            print(f"{element}", end="  ")
                        else:
                            print('-', end="  ")
            print()



def random_dot():
    x = int(random.randrange(1,7))
    y = int(random.randrange(1,7))
    dot_shot = Dot(x, y)
    return dot_shot

class Player:
    def __init__(self, my_Board, enemy_Board):
        self.my_Board = my_Board
        self.enemy_Board = enemy_Board
    def ask(self):
        print('something')

    def move(self):
        dot_shot=self.ask()
        if self.enemy_Board.Shot(dot_shot):
            return True


class User(Player):
    def ask(self):
        asker = True
        while asker:
            x = input('Введите строку для выстрела!')
            if check_input(x):
                x=int(x)
                y = input('Введите столбец для выстрела!')
                if check_input(y):
                    y=int(y)
                    dot_shot = Dot(x, y)
                    asker = False
                    return dot_shot
                else:
                    continue
            else:
                continue


class AI(Player):
    def ask(self):
        x = int(random.randrange(1, 7))
        y = int(random.randrange(1, 7))
        dot_shot = Dot(x, y)
        return dot_shot

list_unposible_dots = []
for i in range(7):
    list_unposible_dots.append([i, 0])
    list_unposible_dots.append([i, 7])
    list_unposible_dots.append([0, i])
    list_unposible_dots.append([7, i])
def rand_ship(dlina):
    AIship1 = Ship(dlina, [random_dot().x, random_dot().y], random.randrange(0, 2), dlina)
    for dot in AIship1.dots():
        if dot in list_unposible_dots:
            raise BoardOutException()
    Board2.add_ship(AIship1)
    for dot in Board2.contour(AIship1):
        list_unposible_dots.append(dot)
    for dot in AIship1.dots():
        list_unposible_dots.append(dot)

def check_input(x, a=1, b=6):
    if x.isdigit():
        if a<=int(x)<=b:
            return True
        else:
            print(f'число вне диапозона [{a}:{b}] попробуйте ещё.')
    else:
        print(f'вводите число [{a}:{b}] попробуйте ещё.')




class Game:
    def random_board(self):
        global Board2
        a=0
        not_end=True
        while not_end:
            count=0
            list_unposible_dots.clear()
            for i in range(7):
                list_unposible_dots.append([i, 0])
                list_unposible_dots.append([i, 7])
                list_unposible_dots.append([0, i])
                list_unposible_dots.append([7, i])

            for i in range(100):
                try:
                    rand_ship(3)
                    count += 1
                    break
                except:
                    continue
            for i in range(100):
                try:
                    rand_ship(2)
                    count += 1
                    break
                except:
                    continue
            for i in range(100):
                try:
                    rand_ship(2)
                    count += 1
                    break
                except:
                    continue
            for i in range(1000):
                try:
                    rand_ship(1)
                    count += 1
                    break
                except:
                    continue
            for i in range(1000):
                try:
                    rand_ship(1)
                    count += 1
                    break
                except:
                    continue
            for i in range(1000):
                try:
                    rand_ship(1)
                    count += 1
                    break
                except:
                    continue
            for i in range(1000):
                try:
                    rand_ship(1)
                    count+=1
                    break
                except:
                    continue
            if count==7:
                not_end=False
            else:
                Board2.clear()

            a+=1
            if a>100:
                print('выход из 100 попыток создать доску!, перезапустите игру')
                break
    def greet(self):
        print('Приветствую игрок! Для начала нужно расставить свои корабли,\n'
              'корабли не могут быть ближе одной клетки друг к другу.\n'
              'Вводи сначала строку, затем столбец точки, где будет расположен нос корабля.\n'
              'Затем выбери расположение:'
              'горизонтально - 0 (слева направо), вертикально - 1 (сверху вниз).\n'
              'Корабли не могут выходить за пределы поля, имей ввиду при растановке и стрельбе.\n'
              'Необходимо выставить один трехпалубный, два двухпалубных и четыре однопалубных корабля.\n'
              'Выстрелы даются до первого промаха, после чего ход уходит сопернику.\n'
              'Попадание отобразится как Х, промах как Т.\n'
              'Когда корабль противника уничтожен вокруг него автоматически проставятся Т\n'
              '(поля в которых по правилам игры не может быть корабля.)\n'
              'Удачи!\n')
    def loop(self):
        not_end = True
        win = False
        while not_end:
            Board1.print_field()
            Board2.print_field()
            correct_move=True
            while correct_move:
                try:
                    while user.move():
                        sum_zhizni=0
                        for some_ship in Board2.list_of_ships:
                            sum_zhizni+=some_ship.zhizni
                        if sum_zhizni == 0:
                            print('Попадание! Это был последний корабль противника!')
                            Board1.print_field()
                            Board2.print_field()
                            win=True
                            not_end=False
                            correct_move = False
                            break
                        print('Попадание! Ходите ещё раз!')
                        Board1.print_field()
                        Board2.print_field()
                    else:
                        print('Вы промахнулись! Ход противника:')
                    correct_move = False
                except:
                    print('Невозможно выстрелить сюда!')
                    continue
            if not_end:
                correct_move = True
                while correct_move:
                    try:
                        while AI.move():
                            sum_zhizni = 0
                            for some_ship in Board1.list_of_ships:
                                sum_zhizni += some_ship.zhizni
                            if sum_zhizni == 0:
                                print('Попадание! Это был ваш последний корабль!')
                                Board1.print_field()
                                Board2.print_field()
                                not_end = False
                                correct_move = False
                                break
                            print('Попадание! Противник ходит ещё раз!')
                        else:
                            print('Противник промахнулся. Ваш ход!')
                        correct_move = False
                    except:
                        continue
        if win:
            print('\nВы победили! Поздравляю!')
        else:
            print('Вы проиграли! Попробуйте ещё!')
        time.sleep(10)

    def start(self):
        self.random_board()
        self.greet()
        self.user_board()
        self.loop()
    def user_board(self):
        global Board1
        list_of_user_ships_to_add=[3,2,2,1,1,1,1]
        while True:
            try:
                list_unposible_dots.clear()
                for a in range(7):
                    list_unposible_dots.append([a, 0])
                    list_unposible_dots.append([a, 7])
                    list_unposible_dots.append([0, a])
                    list_unposible_dots.append([7, a])
                for i in list_of_user_ships_to_add:
                    Board1.print_field()
                    print(f'Установите {i}-палубный корабль. Введите координаты и направление носа корабля')
                    x = input('Введите строку расположения носа корабля!')
                    if check_input(x):
                        x = int(x)
                        y = input('Введите столбец расположения носа корабля!')
                        if check_input(y):
                            y = int(y)
                        else:
                            raise BoardOutException
                    else:
                        raise BoardOutException
                    if i==1:
                        z=0
                    else:
                        z = input('Введите направление носа корабля! 0-горизонтально, 1-вертикально.')
                        if check_input(z,0,1):
                            z=int(z)
                        else:
                            raise BoardOutException
                    Ship1=Ship(i,[x,y],z,i)
                    for dot in Ship1.dots():
                        if dot in list_unposible_dots:
                            raise BoardOutException()
                    Board1.add_ship(Ship1)
                    for dot in Board1.contour(Ship1):
                        list_unposible_dots.append(dot)
                    for dot in Ship1.dots():
                        list_unposible_dots.append(dot)
                break
            except:
                Board1.clear()
                print('Корабль расположен не по правилам, попробуйте ещё раз')
                continue


Board1=Board(0)
Board2=Board(1)
Game1=Game()
user=User(Board1, Board2)
AI=AI(Board2, Board1)
Game1.start()







