class Square:
    def __init__(self,width):
        self.__width = width
        self.__area = None


    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self,width):
        if width <= 0:
            raise  Exception('输入数据不合法')
        self.__width = width
        self.__area =None

    @property
    def area(self):
        if self.__area is None:
            self.__area = self.__width * self.__width
            return self.__area


def main():
    square = Square(5)
    print(square.area)
    square.width = 10
    print(square.area)
    square.width = -3

if __name__ == '__main__':
    main()