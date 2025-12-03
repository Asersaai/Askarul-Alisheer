# Способ 1: обычный импорт модуля
import math_utils
import string_utils as su   # импорт с псевдонимом

# Способ 2: выборочный импорт
from math_utils import add, multiply
from string_utils import count_letters


print("Add:", add(5, 3))
print("Multiply:", multiply(4, 7))

print("Subtract:", math_utils.subtract(10, 4))
print("Capitalize:", su.capitalize_words("hello world"))
print("Letters:", count_letters("Hello 123!!!"))


from shapes import Circle, Rectangle

c = Circle(5)
r = Rectangle(4, 6)

print("Circle area:", c.area())
print("Rectangle area:", r.area())
