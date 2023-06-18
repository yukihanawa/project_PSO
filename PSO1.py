# オブジェクト指向PSO
import random
import math
from typing import Any
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#パラメータ
#粒子数
N = 10
#最大繰り返し回数
MAX_ITERATION = 100
#最大位置
X_MAX = 10
Y_MAX = 10
#最小位置
X_MIN = -10
Y_MIN = -10
w = 0.5
rho_max = 0.5

#評価関数
def fitness(x1,x2):
    return x1**2 + x2**2

#粒子
class Particle:
    def __init__(self,x,y):
        #位置
        self.x, self.y = x, y
        #速度
        self.vx, self.vy = 0.0, 0.0
        #パーソナルベスト
        self.pbest = None
        #グローバルベスト
        self.gbest = None
        #評価値
        self.fitness = None
    #適応度更新
    def set_fitness(self,fitness):
        self.fitness = fitness
    #pbest更新
    def set_pbest(self):
        if self.pbest is None or self.fitness < self.pbest_fitness:
            self.pbest = (self.x,self.y)
            self.pbest_fitness = self.fitness
    #gbest更新
    def set_gbest(self,gbest):
        self.gbest = gbest
    #位置更新
    def update_position(self):
        self.x += self.vx
        self.y += self.vy
    #速度更新
    def update_velocity(self,w,rho_max):
        rhox = random.uniform(0,rho_max)
        rhoy = random.uniform(0,rho_max)
        self.vx = w*self.vx + rhox*(self.pbest[0]-self.x) + rhoy*(self.gbest[0]-self.x)
        self.vy = w*self.vy + rhox*(self.pbest[1]-self.y) + rhoy*(self.gbest[1]-self.y)

#フィールド
class Field:
    def __init__(self,N,X_MIN,X_MAX,Y_MIN,Y_MAX):
        self.N = N #粒子数
        self.x_min, self.x_max = X_MIN, X_MAX #最小位置,最大位置
        self.y_min, self.y_max = Y_MIN, Y_MAX #最小位置,最大位置
        self.gbest = None #グローバルベスト
        self.particles = [Particle(random.uniform(X_MIN,X_MAX),random.uniform(Y_MIN,Y_MAX)) for i in range(N)] #粒子生成
        self.update_best() #グローバルベスト更新
    #評価関数
    def fitness(self,x1,x2):
        return x1**2 + x2**2
    #gbest計算
    def __set_g_best(self):
        p_index = np.argmin([p.fitness for p in self.particles])
        self.gbest = self.particles[p_index].pbest
        self.gbest_fitness = self.particles[p_index].pbest_fitness
    #pbest, gbest更新
    def update_best(self):
        self.__set_g_best()
        for particle in self.particles:
            particle.set_gbest(self.gbest)
            particle.set_pbest()
    #位置更新, 速度更新
    def move_update(self):
        for particle in self.particles:
            particle.update_velocity(w,rho_max)
            particle.update_position()
            particle.set_fitness(self.fitness(particle.x,particle.y))