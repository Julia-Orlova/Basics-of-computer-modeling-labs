import matplotlib.pyplot as plt
from math import exp, erf

# вхідні дані
a = 5 ** 13
c = 2 ** 31
print('Вхідні значення: a = {0}, c = {1}'.format(a, c))
n = 10000
z_0 = 1

# генерація випадкових чисел
x = []
z_i = z_0
for i in range(n):
    z_iplus1 = (z_i * a) % c
    x_i = z_iplus1 / c
    x.append(x_i)
    z_i = z_iplus1

# довжина інтервалу h
h = (max(x) - min(x)) / 20

ends_of_intervals = [min(x), min(x) + h, min(x) + 2*h, min(x) + 3*h, min(x) + 4*h, min(x) + 5*h, min(x) + 6*h,
        min(x) + 7*h, min(x) + 8*h, min(x) + 9*h, min(x) + 10*h, min(x) + 11*h, min(x) + 12*h, min(x) + 13*h,
        min(x) + 14*h, min(x) + 15*h, min(x) + 16*h, min(x) + 17*h, min(x) + 18*h, min(x) + 19*h, min(x) + 20*h]

# кількість влучень згенерованих чисел в інтервали
y = [0 for i in range(len(ends_of_intervals) - 1)]

for i in range(len(x)):
    for j in range(len(y)):
        if ends_of_intervals[j] <= x[i] <= ends_of_intervals[j+1]:
            y[j] += 1

# середне арифметичне та дисперсія
average = sum(x) / n
dispersion = sum([(x[i] - average) ** 2 for i in range(n)]) / (n - 1)
print('Середнє арифметичне значення = {0}\nДисперсія = {1}'.format(round(average, 3), round(dispersion, 3)))

# перевірка відповідності досліджуваних випадкових чисел рівномірному закону розподілу
# очікувана за теоретичним законом розподілу кількість влучень в і-ий інтервал
np_even = [n * (ends_of_intervals[i+1] - ends_of_intervals[i]) / (max(x) - min(x)) for i in range(len(ends_of_intervals) - 1)]
criterion_even = sum([(y[i] - np_even[i]) ** 2 / np_even[i] for i in range(len(y))])

# перевірка відповідності досліджуваних випадкових чисел експотенціальному закону розподілу
lambd = 1 / average
np_exponential = [n * (exp(- lambd * ends_of_intervals[i]) - exp(- lambd * ends_of_intervals[i+1]))
                  for i in range(len(ends_of_intervals) - 1)]
criterion_exponential = sum([(y[i] - np_exponential[i]) ** 2 / np_exponential[i] for i in range(len(y))])

# перевірка відповідності досліджуваних випадкових чисел нормальному закону розподілу
np_normal = [n * (erf((ends_of_intervals[i+1] - average) / (dispersion * 2) ** (1/2))
                  - erf((ends_of_intervals[i] - average) / (dispersion * 2) ** (1/2))) / 2
                  for i in range(len(ends_of_intervals) - 1)]
criterion_normal = sum([(y[i] - np_normal[i]) ** 2 / np_normal[i] for i in range(len(y))])

print('Табличне значення критерію, взяте при рівні значимості α=0.05 та кількості степенів свободи 19, дорівнює 30.1.')
print('Розраховане значення критеріїв: рівномірний - {0}, експотенціальний - {1}, нормальний - {2}'
      .format(round(criterion_even, 3), round(criterion_exponential, 3), round(criterion_normal, 3)))

if criterion_even <= 30.1:
    print('{0} < 30.1, отже з довірчою ймовірністю 0,95 можна стверджувати,\nщо випадкова величина розподілена '
          'за рівномірним законом розподілу.'.format(round(criterion_even, 1)))
elif criterion_exponential <= 30.1:
    print('{0} > 30.1, отже з довірчою ймовірністю 0,95 можна стверджувати,\nщо випадкова величина розподілена '
          'за експотенціальним законом розподілу.'.format(round(criterion_exponential, 1)))
elif criterion_normal <= 30.1:
    print('{0} > 30.1, отже з довірчою ймовірністю 0,95 можна стверджувати,\nщо випадкова величина розподілена '
          'за нормальним законом розподілу.'.format(round(criterion_normal, 1)))
else:
    print('З довірчою ймовірністю 0,95 можна стверджувати, що випадкова величина\nне розподілена за рівномірним,'
          ' нормальним та експотенціальним законами розподілу.')
          
# побудова гістограми
fig, ax = plt.subplots()
ax.bar(ends_of_intervals[0:20], y, width=h-0.005)

fig.set_figwidth(12)
fig.set_figheight(6)

plt.show()
