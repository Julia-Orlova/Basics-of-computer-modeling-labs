import numpy as np

# дані спостережень
x_observed = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5]
y_observed = [14, 18.222, 18, 17.216, 16.444, 15.778, 15.219, 14.749, 14.352,
              14.014, 13.722, 13.469, 13.248, 13.052, 12.879, 12.724]


# функція пошуку коофіцієнтів b
def find_b(n):
    # функціональна залежність f(x)
    def f_of_x(x, a):
        return 1 / (x ** a)

    # матриця X з рядків 1, f1(xi), f2(xi)... fk(xi)
    X = [[1 for i in range(n + 1)] for j in range(len(x_observed))]
    for i in range(1, n + 1):
        for j in range(len(x_observed)):
            X[j][i] = f_of_x(x_observed[j], i)

    X = np.array(X)
    # вектор-стовпець y1, y2 ... yn
    Y = np.array([[y_observed[i]] for i in range(len(x_observed))])
    X_transposed = X.transpose()

    # b = (X_transposed * X) ** (-1) * X_transposed * y
    B = ((np.linalg.inv(X_transposed.dot(X))).dot(X_transposed)).dot(Y)

    return B


# функція залежності y від x, b
def f_of_x_and_b(x, b):
    f = 0
    for i in range(len(b)):
        f += b[i] / (x ** i)
    return f


# вибір найкращої моделі методом найменших квадратів
best_b = []
min = 100
for n in range(0, 20):
    criterion = sum([(f_of_x_and_b(x_observed[i], find_b(n)) - y_observed[i]) ** 2 for i in range(len(x_observed))])
    if criterion < min:
        min = criterion
        best_b = find_b(n)

# вивід результатів
print('y = b0 + b1 / x  + b2 / x ** 2 + ... + bn / x ** n')
print('Значення коефіцієнтів bі при найкращій моделі:')

for i in range((len(best_b))):
    if i % 4 == 0:
        try:
            print('b{0} = {1}; b{2} = {3}; b{4} = {5}; b{6} = {7};'.format(i, float(best_b[i]), i+1,
                    float(best_b[i+1]), i+2, float(best_b[i+2]), i+3, float(best_b[i+3])))
        except:
            try:
                print('b{0} = {1}; b{2} = {3}; b{4} = {5};'.format(i, float(best_b[i]), i + 1,
                                        float(best_b[i + 1]), i+2, float(best_b[i+2])))
            except:
                try:
                    print('b{0} = {1}; b{2} = {3};'.format(i, float(best_b[i]), i+1, float(best_b[i+1])))
                except:
                    print('b{0} = {1};'.format(i, float(best_b[i])))

print('Значення y при знайдених bі:')
print([round((float(f_of_x_and_b(x_observed[i], best_b))), 3) for i in range(len(x_observed))])
print('Спостережувані y:')
print(y_observed)
