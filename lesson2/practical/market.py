"""Создать класс магазина. Конструктор должен инициализировать
значения: «Название магазина» и «Количество проданных
товаров». Реализовать методы объекта, которые будут увеличивать
кол-во проданных товаров, и реализовать вывод значения
переменной класса, которая будет хранить общее количество
товаров проданных всеми магазинами."""

class Market:

    __selled_all_goods = 0

    def __init__(self, name, selled_goods):

        self.name = name
        self.__selled_goods = selled_goods
        Market.__add_goods_number(selled_goods)

    def __add_goods_number(selled_goods):

        Market.__selled_all_goods += selled_goods


    def sell_goods(self, selled_goods):

        self.__selled_goods += selled_goods
        Market.__add_goods_number(selled_goods)

    def get_all_markets_selled_goods():

        return Market.__selled_all_goods

    def get_market_selled_goods(self):
        return self.__selled_goods



def main():
    market1 = Market('Auchan',123123)
    print(Market.get_all_markets_selled_goods()) #123123
    print(market1.get_market_selled_goods()) #123123

    market2 = Market('Billa',321321)
    print(Market.get_all_markets_selled_goods()) #444444

    try:
        print(market2.get_all_markets_selled_goods())# doesen't work, cause it's Class method
    except TypeError as err:
        print(err)

    print(market2.get_market_selled_goods()) #321321

    market1.sell_goods(556)
    print(market1.get_market_selled_goods()) #123679
    print(Market.get_all_markets_selled_goods()) #445000

if __name__ == '__main__':
    main()