# -*-coding:utf-8-*-

import random
import copy
from math import sqrt
import matplotlib.pyplot as plt

"""
Pc:  probability of cross
Pm:  probability of mutation
N:   the number of individual in group
"""

Pc = 0.85
Pm = 0.15
N = 300


def getData()->dict:
    """
    get data from data.txt
    :return: return a dict type datas like this
    datas
    {
        key1(int type): [city1, longitude, altitude],
        key2(int type): [city2, longitude, altitude],
                        .
                        .
                        .
        keyn(int type): [cityn, longitude, altitude]
    }
    """
    datas = {}
    with open("../data/data.txt", "r") as f:
        data_list = f.readlines()
    for i in range(len(data_list)):
        str = data_list[i].replace("\n", "")
        temp = str.split(',')
        datas[i] = temp
    return datas


def initRoute(n: int, data: dict)->list:
    """
    generate n routes
    :return: routes like this
    [route1, route2, route3, ......]
    route1,route2 ... are list type
    """
    cities_list = list(data)
    count = n
    routes = []
    flag = 0
    while count > 0:
        if flag > 300:
            print("please choose reasonable size of according to the length of route.")
            break
        flag += 1
        temp = cities_list.copy()
        route = []
        while temp != []:
            gene = random.choice(temp)
            route.append(gene)
            temp.remove(gene)
        if route not in routes:
            routes.append(copy.deepcopy(route))
            count -= 1
    return routes


def initIndividual(route_list: list, data: dict)->list:
    """
    according to the route set initial individual set
    :param route_list: route set, different route(list) in in route_list
    :param data: refer to value of getData()
    :return: a list contains instance of class Individual
    """
    result = []
    for i in range(len(route_list)):
        result.append(Individual(route_list[i], data))
    return result


class Individual:
    """
    data(dict type): value return getData()
    route(list type): a route travel all the cities
    distance(float): value of fitness function as well as distance of route
    """

    def __init__(self, route, data):
        self.data = data
        self._route = copy.deepcopy(route)
        self.distance = 0
        self._getinstance()

    @property
    def route(self):
        return self._route

    def _getinstance(self):
        """
        calculate a route distance
        """
        length = len(self.route)
        for i in range(length - 1):
            curr_location = self.route[i]
            next_location = self.route[i + 1]
            x = abs(float(self.data[curr_location][1]) - float(self.data[next_location][1]))
            y = abs(float(self.data[curr_location][2]) - float(self.data[next_location][2]))
            self.distance += sqrt(x * x + y * y)
        end_location = self.route[::-1][0]
        start_location = self.route[0]
        x = abs(float(self.data[start_location][1]) - float(self.data[end_location][1]))
        y = abs(float(self.data[start_location][2]) - float(self.data[end_location][2]))
        self.distance += sqrt(x * x + y * y)


def plot(city_data: dict, route: list, start_point):
    route.append(route[0])
    start_x = float(city_data[start_point][1])
    start_y = float(city_data[start_point][2])
    plt.rcParams['font.sans-serif'] = ['SimHei']
    x = []
    y = []
    plt.figure()
    plt.ion()
    for i in city_data:
        longitude = float(city_data[i][1])
        latitude = float(city_data[i][2])
        x.append(longitude)
        y.append(latitude)
    a = []
    b = []
    for i in route:
        a.append(float(city_data[i][1]))
        b.append(float(city_data[i][2]))
    a_ = []
    b_ = []
    for i in range(len(a) - 1):
        temp = [a[i], a[i + 1]]
        a_.append(temp)
        temp = [b[i], b[i + 1]]
        b_.append(temp)
        plt.clf()
        plt.plot(x, y, 'o')
        for i in range(len(x)):
            plt.text(x[i], y[i] + 0.05, u"%s" % city_data[i][0], ha='center', va='bottom', fontsize=9)
        plt.text(start_x - 0.2, start_y - 0.7, u"起点", color='r', ha='center', va='bottom', fontsize=9)
        plt.plot(a_, b_, color='r')
        plt.draw()
        plt.pause(0.5)
    #plt.ioff()
    plt.plot(x, y, 'o')
    plt.plot(a_, b_, color='r')
    plt.show(block=False)


class GA:
    def __init__(self, individuals: list):
        """
        self.individuals: top N individuals
        self.cream: the best individual
        self.new_born_num: the number of new born individuals made by cross procedure
        :param individuals: instances of class Individual in a list
        """
        self.individuals = individuals
        self._cream = 0
        self.new_born_num = 0

    @property
    def cream(self):
        return self._cream

    def getCream(self):
        """
        get the best one according to the distance of individual
        """
        distance = self.individuals[0].distance
        flag = 0
        for i in range(len(self.individuals)):
            if distance > self.individuals[i].distance:
                distance = self.individuals[i].distance
                flag = i
        self._cream = self.individuals[flag]

    def select(self):
        """
        I use elitist preservation strategy, maintain the best solution found over time before selection.
        preserve top N individuals
        """
        if len(self.individuals) == N:
            """
            if self.individuals is initial individuals, return
            """
            return
        for count in range(self.new_born_num):
            distance = self.individuals[0].distance
            flag = 0
            for i in range(len(self.individuals)):
                if distance < self.individuals[i].distance:
                    distance = self.individuals[i].distance
                    flag = i
            worst = self.individuals[flag]
            self.individuals.remove(worst)

    def cross(self):
        """
        cross method produces new born individuals and add it to the self.individuals
        self.new_born_num counts new born individuals in total

        """
        self.new_born_num = 0
        for i in range(len(self.individuals)-1):
            rate = random.random()
            if rate < Pc:
                parent1 = copy.deepcopy(self.individuals[i])
            else:
                continue
            parent2 = copy.deepcopy(self.individuals[i+1])
            if parent1.route == parent2.route:
                continue
            gene_length = len(self.individuals[0].route)
            index1 = random.randint(0, gene_length - 1)
            index2 = random.randint(index1, gene_length - 1)
            gene_segment1 = parent2.route[index1:index2]
            route1 = []
            flag = 0
            for gene in parent1.route:
                if gene not in gene_segment1:
                    if flag == index1:
                        route1 += gene_segment1
                    route1.append(gene)
                    flag += 1
            flag = 0
            gene_segment2 = parent1.route[index1:index2]
            route2 = []
            for gene in parent2.route:
                if gene not in gene_segment2:
                    if flag == index1:
                        route2 += gene_segment2
                    route2.append(gene)
                    flag += 1
            new_individual2 = Individual(route2, self.individuals[0].data)
            self.individuals.append(new_individual2)
            new_individual1 = Individual(route1, self.individuals[0].data)
            self.individuals.append(new_individual1)
            self.new_born_num += 2

    def mutate(self):
        gene_length = len(self.individuals[0].route)
        for i in range(len(self.individuals)):
            while True:
                index1 = random.randint(0, gene_length - 1)
                index2 = random.randint(0, gene_length - 1)
                if index1 != index2:
                    self.individuals[i].route[index1], self.individuals[i].route[index2] = self.individuals[i].route[index1], self.individuals[i].route[index2]
                    break

    @classmethod
    def start(cls, n=100, N=300, data=None):
        """
        :param n: the number of generation
        :param N: size of group
        :param data: dict type data
        :return: the best individual
        """
        if data is None:
            data = getData()
        route = initRoute(N, data)
        individuals = initIndividual(route, data)
        ins = cls(individuals)
        plt.ion()
        plt.figure(1)
        x = []
        y = []
        i = 0
        while True:
            plt.clf()
            ins.getCream()
            ins.select()
            ins.cross()
            ins.mutate()
            x.append(i)
            y.append(ins.cream.distance)
            if i == n:
                plt.xlabel("generation")
                plt.ylabel("distance")
                plt.plot(x, y)
                plt.show(block=False)
                break
            plt.xlabel("generation")
            plt.ylabel("distance")
            plt.plot(x, y)
            plt.draw()
            plt.pause(0.001)
            i += 1

        return ins.cream


if __name__ == "__main__":
    top = GA.start(200)
    data = getData()
    plot(data, top.route, top.route[0])
    print("route -> ", top.route)
    print("distance -> ", top.diatance)
