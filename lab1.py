import matplotlib.pyplot as plt

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

# очікувана за теоретичним законом розподілу кількість влучень в і-ий інтервал
np = [n * (ends_of_intervals[i+1] - ends_of_intervals[i]) / (max(x) - min(x)) for i in range(len(ends_of_intervals) - 1)]

# перевірка відповідності досліджуваних випадкових чисел рівномірному закону розподілу
criterion = sum([(y[i] - np[i]) ** 2 / np[i] for i in range(len(y))])
print('Табличне значення критерію, взяте при рівні значимості α=0.05 та кількості степенів свободи 19, дорівнює 30.1.')
print('Розраховане значення критерію: ', round(criterion, 6))
if criterion <= 30.1:
    print('{0} < 30.1, отже з довірчою ймовірністю 0,95 можна стверджувати, що знайдений закон розподілу\nвідповідає '
          'спостережуваним значенням випадкової величини.'.format(round(criterion, 1)))
else:
    print('{0} > 30.1, отже з довірчою ймовірністю 0,95 можна стверджувати, що знайдений закон розподілу\nне '
          'відповідає спостережуваним значенням випадкової величини.'.format(round(criterion, 1)))

# побудова гістограми
fig, ax = plt.subplots()
ax.bar(ends_of_intervals[0:20], y, width=h-0.005)

fig.set_figwidth(12)
fig.set_figheight(6)

plt.show()
