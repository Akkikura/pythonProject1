import sqlalchemy as sq
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __init__(self, id_publ, name):
        self.id_publ = id_publ
        self.name = name

    def __repr__(self):
        return f'({self.id_publ}) {self.name}'


class Book(Base):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'))

    def __init__(self, id_book, title, id_publ):
        self.id = id_book
        self.title = title
        self.id_publisher = id_publ

    def __repr__(self):
        return f'{self.title}'


class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __init__(self, id_shop, shop_name):
        self.id = id_shop
        self.name = shop_name

    def __repr__(self):
        return f'{self.name}'


class Stock(Base):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'))
    count = sq.Column(sq.Integer)

    def __init__(self, id_stock, id_book, id_shop, count):
        self.id = id_stock
        self.id_book = id_book
        self.id_shop = id_shop
        self.count = count


class Sale(Base):
    __tablename__ = 'sale'
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer)
    date_sale = sq.Column(sq.Date)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'))
    count = sq.Column(sq.Integer)

    def __init__(self, id, price, date_sale, id_stock, count):
        self.id = id
        self.price = price
        self.date_sale = date_sale
        self.id_stock = id_stock
        self.count = count

    def __repr__(self):
        return f'{self.price} | {self.date_sale}'


DSN = 'postgresql://postgres:8812@localhost:5432/main_db'

engine = create_engine(DSN)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
publ_1 = Publisher(1, 'Пушкин')
publ_2 = Publisher(2, 'Чехов')
publ_3 = Publisher(3, 'Толстой')

session.add(publ_1)
session.add(publ_2)
session.add(publ_3)
session.commit()

book_1 = Book(1, 'Капитанская дочь', 1)
book_2 = Book(2, 'Руслан и Людмида', 1)
book_3 = Book(3, 'Война и Мир', 3)
book_4 = Book(4, 'Вишневый сад', 2)
session.add(book_1)
session.add(book_2)
session.add(book_3)
session.add(book_4)
session.commit()

shop_1 = Shop(1, 'Буквоед')
shop_2 = Shop(2, 'Книги и Книжечки')

session.add(shop_1)
session.add(shop_2)

session.commit()

stock_1 = Stock(1, 1, 1, 1)
stock_2 = Stock(2, 2, 1, 1)
stock_3 = Stock(3, 3, 2, 1)
stock_4 = Stock(4, 4, 2, 1)

session.add(stock_1)
session.add(stock_2)
session.add(stock_3)
session.add(stock_4)

session.commit()

sale_1 = Sale(1, 300, '11.09.2021', 1, 1)
sale_2 = Sale(2, 200, '11.09.2021', 2, 1)
sale_3 = Sale(3, 100, '11.09.2021', 3, 1)
sale_4 = Sale(4, 150, '11.09.2021', 4, 1)

session.add(sale_1)
session.add(sale_2)
session.add(sale_3)
session.add(sale_4)

session.commit()

zapros = input()
try:
    zapros = int(zapros)
    result = session.query(Book, Shop, Sale).filter(Publisher.id == zapros).filter(
        Publisher.id == Book.id_publisher).filter(Book.id_publisher == Stock.id_book).filter(
        Stock.id_shop == Shop.id).filter(Stock.id == Sale.id_stock).all()

except:
    result = session.query(Book, Shop, Sale).filter(Publisher.name == zapros).filter(
        Publisher.id == Book.id_publisher).filter(Book.id_publisher == Stock.id_book).filter(
        Stock.id_shop == Shop.id).filter(Stock.id == Sale.id_stock).all()
for r in result:
    print(f'{r[0]} | {r[1]} | {r[2]}')

session.close
