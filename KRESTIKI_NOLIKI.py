from random import randint


class Cell:
    def __init__(self, value=0):
        self.value = value #текущее значение в ячейке: 0 - клетка свободна; 1 - стоит крестик; 2 - стоит нолик.
        #надо будет закрыть

    def __bool__(self):
        return self.value == 0

class TicTacToe:
    N = 3          # размер поля
    FREE_CELL = 0      # свободная клетка
    HUMAN_X = 1        # крестик (игрок - человек)
    COMPUTER_O = 2     # нолик (игрок - компьютер)

    def __init__(self):
        self._win = 0  #0 - не закончена, 1 - выиграл человек, 2 - выиграл компьютер, 3 - ничья
        self.init()

    def __bool__(self): #окончена ли игра
        return self._win == 0 and self._win not in (1, 2, 3)

    @property
    def is_human_win(self): #возвращает True, если победил человек, иначе - False
        return self._win == 1

    @property
    def is_computer_win(self): #возвращает True, если победил компьютер, иначе - False
        return self._win == 2

    @property
    def is_draw(self): #возвращает True, если ничья, иначе - False.
        return self._win == 3

    def __update_win_status(self):
        for row in self.pole:
            if all(x.value == self.HUMAN_X for x in row):
                self._win = 1
                return
            elif all(x.value == self.COMPUTER_O for x in row):
                self._win = 2
                return

        for i in range(self.N):
            if all(x.value == self.HUMAN_X for x in (row[i] for row in self.pole)):
                self._win = 1
                return
            elif all(x.value == self.COMPUTER_O for x in (row[i] for row in self.pole)):
                self._win = 2
                return

        if all(self.pole[i][i].value == self.HUMAN_X for i in range(self.N)) or \
                all(self.pole[i][-1-i].value == self.HUMAN_X for i in range(self.N)):
            self._win = 1
            return
        elif all(self.pole[i][i].value == self.COMPUTER_O for i in range(self.N)) or \
                all(self.pole[i][-1-i].value == self.COMPUTER_O for i in range(self.N)):
            self._win = 2
            return

        if all(x.value != self.FREE_CELL for row in self.pole for x in row):
            self._win = 3
            return

    def __check_index(self, index): #проверка индексов при: res = game[i, j], ниже два метода
        i, j = index 
        if type(i) != int or type(j) != int or not( 0 <= i < self.N) or not( 0 <= j < self.N):
            raise IndexError('некорректно указанные индексы')

    def __check_value(self, value): #проверка на правильность передачи хода(комп, человек или свободна)
        i, j = value
        if i in (self.FREE_CELL, self.HUMAN_X, self.COMPUTER_O) and j in (self.FREE_CELL, self.HUMAN_X, self.COMPUTER_O):
            return
        raise ValueError('Неверно переданы данные хода')


    def __getitem__(self, item):
        self.__check_index(item)
        i, j = item
        return self.pole[i][j].value

    def __setitem__(self, key, value):
        self.__check_index(key)
        self.__check_value(key)
        i, j = key
        obj = self.pole[i][j]
        if bool(obj):
            obj.value = value
        else:
            ValueError('Клетка занята')

        self.__update_win_status()

    def init(self): #инициализация игры (очистка игрового поля, возможно, еще какие-либо действия)
        self.pole = tuple(tuple(Cell() for _ in range(self.N)) for _ in range(self.N)) #самое поле из обьектов,
        #публичный для теста, потом закрыть



    def show(self): #отображение текущего состояния игрового поля (запрашивает координаты свободной клетки и ставит туда крестик)
        temp = ['?', 'X', 'O']
        k = 0
        print('  1 2 3')
        for row in self.pole:
            k += 1
            print(k, end=' ')
            for col in row:
                print(temp[col.value], end=' ')
            print()

    def human_go(self): #реализация хода игрока (запрашивает координаты свободной клетки и ставит туда крестик)
        if not self:
            return

        while True:
            i, j = map(lambda x: int(x)-1, input('Введите координаты клетки: ').split())
            if self[i, j] == self.FREE_CELL:
                self[i, j] = self.HUMAN_X 
                break
            else:
                 print('Клетка занята')

    def computer_go(self): #реализация хода компьютера (ставит случайным образом нолик в свободную клетку)
        if not self:
            return 

        while True:
            i, j = randint(0, self.N-1), randint(0, self.N-1)
            if self[i, j] == self.FREE_CELL:
                self[i, j] = self.COMPUTER_O
                break


game = TicTacToe()
game.init()
step_game = 0
game.show()
while game:

    if step_game % 2 == 0:
        game.human_go()
    else:
        game.computer_go()
        game.show()

    step_game += 1


game.show()

if game.is_human_win:
    print("Поздравляем! Вы победили!")
elif game.is_computer_win:
    print("Все получится, со временем")
else:
    print("Ничья.")


