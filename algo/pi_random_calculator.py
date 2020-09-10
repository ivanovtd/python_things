import random

def estimate_pi(n: int):
    """Идея следующая: 
        Постройте ось координат x,y в котором нарисуйте четверть круга радиусом 1 и квадрат со строной 1
        Отношение количества точек в круге к количеству точек в квадрате будет равно отношению количества точек в послном круге с радиусом 1 к количеству точек в квадрате со стороной 2. Высчитав площадь квадрата равную (2*r)**2 и площадб круга, равную pi * r**2 мы получим следующее уравнение: (pi * r**2) / ((2*r) **2) = num_points_in_circle / num_points total => получаем что pi = 4 * num_points_in_circle / num_points_total
        """

    num_points_in_circle = 0
    num_points_total = 0
    for _ in range(n):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        distance = x**2 + y**2
        if distance <= 1:
            num_points_in_circle += 1
        num_points_total += 1
    return 4 * num_points_in_circle / num_points_total

if __name__ == '__main__':
    print(estimate_pi(10000000))
