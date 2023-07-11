import random
import math
import numpy as np
import csv
import os
import merge_csv
import itertools

# パラメータ
N = 100                 # 粒子数
MAX_ITERATION = 2000  # 世代数
D = 10                 # 次元数
# w = 1                # 慣性係数
# c1 = 2           # 加速係数(pbest)
# c2 = 2           # 加速係数(gbest)

#パラメータセット
function_set = ["rastrigin", "rosenbrock"]
# w_set = [0.5]
# c1_set = [1.5, 2]
# c2_set = [1.5, 2]

# parameter_set = [(0.5, 2, 2), (0.5, 1.5, 2), (0.5, 1, 1.5)]
parameter_set = [(1.0,2,2)]


# 粒子クラス
class Particle:
    def __init__(self, D):
        self.position = np.random.uniform(POS_MIN, POS_MAX, D)
        self.velocity = np.zeros(D)
        self.pbest = None
        self.pbest_fitness = math.inf
        self.gbest = None
        self.fitness = None

    def set_fitness(self, fitness):
        self.fitness = fitness

    def set_pbest(self):
        if self.pbest is None or self.fitness < self.pbest_fitness:
            self.pbest = self.position.copy()
            self.pbest_fitness = self.fitness

    def set_gbest(self, gbest):
        self.gbest = gbest

    def update_position(self):
        self.position += self.velocity
        self.position = np.clip(self.position, POS_MIN, POS_MAX)

    def update_velocity(self, w):
        rho1 = random.random()
        rho2 = random.random()
        self.velocity = w * self.velocity + c1 * rho1 * (self.pbest - self.position) + c2 * rho2 * (self.gbest - self.position)

# フィールドクラス
class Field:
    def __init__(self, N, D, function_name):
        self.N = N
        self.D = D
        self.function_name = function_name
        self.gbest = None
        self.gbest_fitness = math.inf
        self.particles = [Particle(D) for _ in range(N)]
        self.update_best()

    def fitness(self, position):
        if self.function_name == "rastrigin":
            return self.D * 10 + np.sum(position ** 2 - 10 * np.cos(2 * np.pi * position))
        elif self.function_name == "rosenbrock":
            return np.sum(100.0 * (position[1:] - position[:-1]**2.0)**2.0 + (1 - position[:-1])**2.0)
        else:
            raise ValueError("Invalid function name")

    def update_best(self):
        for particle in self.particles:
            particle.set_fitness(self.fitness(particle.position))
            particle.set_pbest()

        # Find the best particle in this generation
        p_index = np.argmin([p.pbest_fitness for p in self.particles])
        current_best_position = self.particles[p_index].pbest
        current_best_fitness = self.particles[p_index].pbest_fitness

        # Compare with the global best
        if current_best_fitness < self.gbest_fitness:
            self.gbest = current_best_position.copy()
            self.gbest_fitness = current_best_fitness

        for particle in self.particles:
            particle.set_gbest(self.gbest)


    def move_update(self, w):
        for particle in self.particles:
            particle.update_velocity(w)
            particle.update_position()
            particle.set_fitness(self.fitness(particle.position))

# wの値を更新する関数を定義します
def update_w(initial_w, iteration, decrease_interval=MAX_ITERATION//4, decrease_amount=0.1, min_w=0.7):
    w = initial_w - (iteration // decrease_interval) * decrease_amount
    return max(w, min_w) # wの最小値を0.7とします

#パラメータの組み合わせを作成
# parameter_set = itertools.product(function_set, w_set, c1_set, c2_set)
#パラメータの組み合わせを順に取り出す
for function in function_set:
    for  initial_w, c1, c2 in parameter_set:

        output_directory = f'./{function}_{initial_w}_{c1}_{c2}' #出力先のディレクトリを作成
        os.makedirs(output_directory, exist_ok=True) #ディレクトリを作成
        # functionの値に基づいてPOS_MAXとPOS_MINを設定
        if function == 'rastrigin':
            POS_MAX = 5.12
            POS_MIN = -5.12
        elif function == 'rosenbrock':
            POS_MAX = 2.048
            POS_MIN = -2.048
        else:
            print("Unknown function")
            POS_MAX = None
            POS_MIN = None

        #シード値を変えて実行
        for seed in range(11):
            np.random.seed(seed)
            random.seed(seed)
            # PSO Algorithm with Rastrigin or Rosenbrock Function
            pso = Field(N, D, function)

            #ファイル名を作成
            filename = f'{function}_seed{seed}.csv'

            filepath = os.path.join(output_directory, filename) #ファイルのパスを作成

            #ファイルを開く
            with open(filepath, 'w', newline='') as csvfile:
                #ファイルに書き込み
                csv_writer = csv.writer(csvfile)

                #ヘッダーを書き込み
                csv_writer.writerow(['iteration', 'gbest_fitness'])

                pso.update_best()
                csv_writer.writerow([0, pso.gbest_fitness])

                for i in range(MAX_ITERATION):
                    w = update_w(initial_w, i) # ここでwを更新します
                    pso.move_update(w)
                    pso.update_best()
                    #print(f"{function}, iteration: {i}, gbest: {pso.gbest}, gbest_fitness: {pso.gbest_fitness}")
                    csv_writer.writerow([i+1, pso.gbest_fitness])
        merge_csv.make_csv(output_directory)