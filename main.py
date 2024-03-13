# Этот алгоритм написан для того, чтобы оптимизировать проходимость перекрестка при помощи смены времени зеленого сигнала.


import random

# id светофоров и пешеходных переходов/дорог совпадают для удобства
# Словарь с состояниями пешеходных светофоров
pedestrian_traffic_lights = {11: {"красный": 0, "зеленый": 0},
                             12: {"красный": 0, "зеленый": 0},
                             13: {"красный": 0, "зеленый": 0},
                             14: {"красный": 0, "зеленый": 0},
                             15: {"красный": 0, "зеленый": 0},
                             16: {"красный": 0, "зеленый": 0},
                             17: {"красный": 0, "зеленый": 0},
                             18: {"красный": 0, "зеленый": 0}}
# Словарь с состояниями автомобильных светофоров
car_traffic_lights = {3: {"красный": 0, "желтый": 0, "зеленый": 0},
                      4: {"красный": 0, "желтый": 0, "зеленый": 0},
                      5: {"красный": 0, "желтый": 0, "зеленый": 0},
                      6: {"красный": 0, "желтый": 0, "зеленый": 0}}
# Словарь с количеством пешеходов на переходах (по id контролирующего светофора)
number_of_pedestrians_at_crossing = {11: 2, 12: 3, 13: 2, 14: 0, 15: 0, 16: 0, 17: 0, 18: 2}
# Словарь с количеством автомобилей на дорогах (по id контролирующего светофора)
number_of_cars_on_the_roads = {3: 1, 4: 2, 5: 2, 6: 2}
# Скорость пешехода, измеряемая в секундах
pedestrian_speed = 15
# Скорость автомобиля, измеряемая в секундах
car_speed = 15
general_queue_of_walkers = {}  # очередь для светофоров
single_timer = 0  # таймер для одного светофора
COUNT = 1  # количество итераций
min_time_for_signal = 15
max_time_for_signal = 90
collection_of_traffic_data = {}  # сбор данных о проходимости перекрестка
flag = False  # флаг, включающийся перед оптимизацией
traffic_light_time = {}  # время свечения светофора
optimization_rule = {1: {"малое", "малое", 1},
                     2: {"малое", "среднее", 2},
                     3: {"малое", "большое", 2},
                     4: {"среднее", "малое", 3},
                     5: {"среднее", "среднее", 1},
                     6: {"среднее", "большое", 2},
                     7: {"большое", "малое", 3},
                     8: {"большое", "среднее", 3},
                     9: {"большое", "большое",
                         1}}  # правила оптимизации светофоров по количеству пешеходов и автомобилей


# 1 - не изменять, 2 - увеличить, 3 - уменьшить


# Изначальная смена цветов светофоров для начала алгоритма
def initial_colors_of_traffic_lights():
    car_traffic_lights[3]["красный"] = 1
    car_traffic_lights[4]["зеленый"] = 1
    car_traffic_lights[5]["красный"] = 1
    car_traffic_lights[6]["зеленый"] = 1

    pedestrian_traffic_lights[11]["зеленый"] = 1
    pedestrian_traffic_lights[12]["красный"] = 1
    pedestrian_traffic_lights[13]["красный"] = 1
    pedestrian_traffic_lights[14]["зеленый"] = 1
    pedestrian_traffic_lights[15]["зеленый"] = 1
    pedestrian_traffic_lights[16]["красный"] = 1
    pedestrian_traffic_lights[17]["красный"] = 1
    pedestrian_traffic_lights[18]["зеленый"] = 1


# Рандомная смена цвета светофора
def the_traffic_lights_is_on(colors_traffic_lights, type):
    if type == "pedestrians":
        colors = ["красный", "зеленый"]

        for traffic_lights in colors_traffic_lights:
            if random.choice(colors) == "красный":
                colors_traffic_lights[traffic_lights]["красный"] = 1
                colors_traffic_lights[traffic_lights]["зеленый"] = 0
            else:
                colors_traffic_lights[traffic_lights]["красный"] = 0
                colors_traffic_lights[traffic_lights]["зеленый"] = 1
    else:
        colors = ["красный", "желтый", "зеленый"]

        for traffic_lights in colors_traffic_lights:
            if random.choice(colors) == "красный":
                colors_traffic_lights[traffic_lights]["красный"] = 1
                colors_traffic_lights[traffic_lights]["желтый"] = 0
                colors_traffic_lights[traffic_lights]["зеленый"] = 0
            elif random.choice(colors) == "желтый":
                colors_traffic_lights[traffic_lights]["красный"] = 0
                colors_traffic_lights[traffic_lights]["желтый"] = 1
                colors_traffic_lights[traffic_lights]["зеленый"] = 0
            else:
                colors_traffic_lights[traffic_lights]["красный"] = 0
                colors_traffic_lights[traffic_lights]["желтый"] = 0
                colors_traffic_lights[traffic_lights]["зеленый"] = 1


# Смена света светофоров, взаимосвязанных друг с другом, когда известен цвет
def traffic_light_change(id_tl, color):  # color - цвет, на который нужно поменять свет светофора
    if id_tl == 4 or id_tl == 6:
        if color == "красный":
            color = "зеленый"
        elif color == "зеленый":
            color = "красный"
        else:
            color = "желтый"
    if color == "красный":
        car_traffic_lights[3]["зеленый"] = 0
        car_traffic_lights[3]["желтый"] = 0
        car_traffic_lights[5]["зеленый"] = 0
        car_traffic_lights[5]["желтый"] = 0
    elif color == "зеленый":
        car_traffic_lights[3]["красный"] = 0
        car_traffic_lights[3]["желтый"] = 0
        car_traffic_lights[5]["красный"] = 0
        car_traffic_lights[5]["желтый"] = 0
    else:
        car_traffic_lights[3]["зеленый"] = 0
        car_traffic_lights[3]["красный"] = 0
        car_traffic_lights[5]["зеленый"] = 0
        car_traffic_lights[5]["красный"] = 0
    car_traffic_lights[3][color] = 1
    car_traffic_lights[5][color] = 1
    # else:
    if id_tl == 3 or id_tl == 5:
        if color == "красный":
            color = "зеленый"
        elif color == "зеленый":
            color = "красный"
        else:
            color = "желтый"
    if color == "красный":
        car_traffic_lights[4]["зеленый"] = 0
        car_traffic_lights[4]["желтый"] = 0
        car_traffic_lights[6]["зеленый"] = 0
        car_traffic_lights[6]["желтый"] = 0
    elif color == "зеленый":
        car_traffic_lights[4]["красный"] = 0
        car_traffic_lights[4]["желтый"] = 0
        car_traffic_lights[6]["красный"] = 0
        car_traffic_lights[6]["желтый"] = 0
    else:
        car_traffic_lights[4]["зеленый"] = 0
        car_traffic_lights[4]["красный"] = 0
        car_traffic_lights[6]["зеленый"] = 0
        car_traffic_lights[6]["красный"] = 0
    car_traffic_lights[4][color] = 1
    car_traffic_lights[6][color] = 1


def traffic_light_timer():
    # рандомно выбирается временной отрезок (сколько времени будет гореть светофор)
    for key in car_traffic_lights.keys():
        traffic_light_time[key] = random.randint(min_time_for_signal, max_time_for_signal)


def optimization(tl):
    if car_traffic_lights[tl]["зеленый"] == 1:
        if number_of_cars_on_the_roads[tl] <= 4 and traffic_light_time[tl] <= 30:
            print("# то применяется правило 1")
            traffic_light_time[tl] = 60
        elif number_of_cars_on_the_roads[tl] <= 7 and traffic_light_time[tl] <= 30:
            print("# то применяется правило 2")
            traffic_light_time[tl] = 90
        elif number_of_cars_on_the_roads[tl] <= 10 and traffic_light_time[tl] <= 30:
            print("# то применяется правило 3")
            traffic_light_time[tl] = 120
        elif number_of_cars_on_the_roads[tl] <= 4 and traffic_light_time[tl] <= 60:
            print("# то применяется правило 4")
            traffic_light_time[tl] = 60
        elif number_of_cars_on_the_roads[tl] <= 7 and traffic_light_time[tl] <= 60:
            print("# то применяется правило 5")
            traffic_light_time[tl] = 90
        elif number_of_cars_on_the_roads[tl] <= 10 and traffic_light_time[tl] <= 60:
            print("# то применяется правило 6")
            traffic_light_time[tl] = 120
        elif number_of_cars_on_the_roads[tl] <= 4 and traffic_light_time[tl] <= 90:
            print("# то применяется правило 7")
            traffic_light_time[tl] = 30
        elif number_of_cars_on_the_roads[tl] <= 7 and traffic_light_time[tl] <= 90:
            print("# то применяется правило 8")
            traffic_light_time[tl] = 90
        elif number_of_cars_on_the_roads[tl] <= 10 and traffic_light_time[tl] <= 90:
            print("# то применяется правило 9")
            traffic_light_time[tl] = 120


def algorithm():
    count = 0

    while count < COUNT:
        for car in number_of_cars_on_the_roads:
            random_count_car = random.randint(5, 10)
            number_of_cars_on_the_roads[car] = random_count_car
        for element in number_of_cars_on_the_roads:
            print("Светофор: ", element, ", Количество авто: ", number_of_cars_on_the_roads[element])
        for ctl in car_traffic_lights:
            if number_of_cars_on_the_roads[ctl] > 0 and car_traffic_lights[ctl][
                "зеленый"]:  # если на контролируемой светофором дороге есть автомобили и если свет светофора "зеленый"
                print("Светофор: ", ctl, "\n", "Свет светофора: ", car_traffic_lights[ctl], "\n", "Время: ",
                      traffic_light_time[ctl], "\n", "Количество автомобилей: ", number_of_cars_on_the_roads[ctl], "\n")

                optimization(ctl)

                # Переезд автомобилями дороги
                while number_of_cars_on_the_roads[ctl] > 0:
                    number_of_cars_on_the_roads[ctl] -= 1  # количество автомобилей на дороге уменьшается на один
                    traffic_light_time[ctl] -= car_speed
                    if car_speed > traffic_light_time[ctl]:
                        break

                # Пока горит зеленый, заполняются пешеходами переходы
                for pedestrian in number_of_pedestrians_at_crossing:
                    random_count_pedestrian = random.randint(0, 6)
                    number_of_pedestrians_at_crossing[pedestrian] = random_count_pedestrian
                traffic_light_change(ctl, "желтый")  # меняем в методе цвета взаимосвязанных светофоров

                print("Светофор: ", ctl, "\n", "Свет светофора: ", car_traffic_lights[ctl], "\n",
                      "Количество автомобилей: ", number_of_cars_on_the_roads[ctl], "\n")

                # меняем свет светофора на следующий
                traffic_light_change(ctl, "красный")
                print("Светофор: ", ctl, "\n", "Свет светофора: ", car_traffic_lights[ctl], "\n",
                      "Количество автомобилей: ", number_of_cars_on_the_roads[ctl], "\n")
            elif number_of_cars_on_the_roads[ctl] == 0 and car_traffic_lights[ctl]["зеленый"]:
                print("Светофор: ", ctl, "\n", "Свет светофора: ", car_traffic_lights[ctl], "\n", "Время: ",
                      traffic_light_time[ctl], "\n", "Количество автомобилей: ", number_of_cars_on_the_roads[ctl],
                      "\n")

        count += 1
        traffic_light_timer()
    flag = True
    for element in number_of_cars_on_the_roads:
        print("Светофор: ", element, ", Количество авто: ", number_of_cars_on_the_roads[element])


initial_colors_of_traffic_lights()
if flag == False:
    traffic_light_timer()
algorithm()





