# 데이터 파일 읽기
file = open("tsp299.txt", "r")
data = file.read().split()
data = [eval(i) for i in data]
import threading
import random



# 지정시간이 지나면 프로그램을 종료하는 함수
def timeout():
    print("10분이 지나 프로그램이 종료됩니다.")
    # 프로그램 종료
    import os
    os._exit(0)


# 도시 좌표 데이터 만들기
#city_count = data[0]
city_count = data[0]
city_coords = []
for i in range(1, len(data), 3):
    city_coords.append((data[i + 1], data[i + 2], data[i]))


# 두 도시 좌표 사이의 거리 구하기
import math
def GetDistance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

# path를 기반으로 총 거리를 구하는 함수
def GetDistanceFromRoute(path):
    # path는 경로, path를 기반으로 총거리를 구할 수 있음.
    dist = distance[0][path[0]]
    for i in range(len(path) - 1):
        dist += distance[path[i]][path[i + 1]]
    dist += distance[path[-1]][0]

    return dist
# 도시 사이의 거리 미리 구해놓기
distance = [[0 for i in range(city_count)] for j in range(city_count)]
for i in range(city_count - 1):
    for j in range(i + 1, city_count):
        distance[i][j] = GetDistance(city_coords[i], city_coords[j])
        distance[j][i] = distance[i][j]

# itertools.permutations()을 사용하여 각 경로(순열)의 거리를 구하고
# 현재 shortest 거리보다 더 짧은 거리가 나오면 shortest 값 갱신하기
import itertools
import time

def ExhaustiveSearch():
    # 600초가 지나면 프로그램이 종료되도록 함.
    timer = threading.Timer(600, timeout)
    timer.start()

    shortest_distance = math.inf
    shortest_path = None
    start_time = time.time()

    # 1~ city_count 까지 존재하는 모든 순열의 리스트가 iter, 이 순열이 경로가 됨.
    iter = itertools.permutations(range(1, city_count))
    for path in iter:
        dist = int(GetDistanceFromRoute(path) + 0.5)

        if dist < shortest_distance:
            shortest_distance = dist
            shortest_path = path
            print(shortest_distance, path)
            DrawTour(path)

    print("탐색 끝")
    print(f"탐색시간 : {(time.time() - start_time)}초")
    timer.cancel()
    label.configure(text = shortest_distance)

def FirstChoice():
    # 600초가 지나면 프로그램이 종료되도록 함.
    timer = threading.Timer(600, timeout)
    timer.start()
    start_time = time.time()

    # 초기해
    current = list(range(1, city_count))

    # TODO : 종료 조건을 어떻게 설정해야 할까..
    while True:
        # 랜덤한 이웃해 생성
        exchange_idx1 = random.randint(0, city_count-2)
        exchange_idx2 = random.randint(0, city_count-2)

        neighbor = [ i for i in current ]
        neighbor[exchange_idx2], neighbor[exchange_idx1] = neighbor[exchange_idx1], neighbor[exchange_idx2]

        # 2개의 해의 거리 계산
        current_dist = int(GetDistanceFromRoute(current) + 0.5)
        neighbor_dist = int(GetDistanceFromRoute(neighbor) + 0.5)

        # 랜덤하게 찾은 이웃해가 더 좋은 해라면 current 업데이트
        if(current_dist > neighbor_dist):
            current = neighbor
            print(neighbor_dist, neighbor)
            DrawTour(current)




    print("탐색 끝")
    print(f"탐색시간 : {(time.time() - start_time)}초")
    timer.cancel()

def SimulatedAnnealing():
    # 600초가 지나면 프로그램이 종료되도록 함.
    timer = threading.Timer(600, timeout)
    timer.start()
    start_time = time.time()

    temperature = 100


    # 초기해
    current = list(range(1, city_count))

    while temperature >= 0.00001:
        # 랜덤한 이웃해 생성
        exchange_idx1 = random.randint(0, city_count - 2)
        exchange_idx2 = random.randint(0, city_count - 2)

        neighbor = [i for i in current]
        neighbor[exchange_idx2], neighbor[exchange_idx1] = neighbor[exchange_idx1], neighbor[exchange_idx2]

        # 2개의 해의 거리 계산
        current_dist = int(GetDistanceFromRoute(current) + 0.5)
        neighbor_dist = int(GetDistanceFromRoute(neighbor) + 0.5)


        # 랜덤하게 찾은 이웃해가 더 좋은 해라면 current 업데이트
        if (current_dist >= neighbor_dist):
            current = neighbor
            print(neighbor_dist, neighbor)
            DrawTour(current)
        #simulated annealing은 이웃해가 좋지 않아도 확률적으로 이동이 가능
        else:
            probablity = math.exp((neighbor_dist - current_dist) / temperature)
            if random.random() < probablity:
                current = neighbor
                print(neighbor_dist, neighbor)
                DrawTour(current)

        # Scheduled(T) 작업 수행
        temperature *= 0.999
        temperature -= 0.01

    print("탐색 끝")
    print(f"탐색시간 : {(time.time() - start_time)}초")
    timer.cancel()

def GeneticAlgorithm():
    # 600초가 지나면 프로그램이 종료되도록 함.
    timer = threading.Timer(600, timeout)
    timer.start()
    start_time = time.time()

    print("탐색 끝")
    print(f"탐색시간 : {(time.time() - start_time)}초")
    timer.cancel()



class FirstChoiceWorker:

    #랜덤한 초깃값
    best_path = random.sample(range(1, city_count), city_count-1)
    best_distance = None
    # 랜덤한 초깃값에 대해 First-Choice 탐색 수행, 이때 스레드는 10분동안 동작한다.
    def run(self):
        end_time = time.time()+600

        while time.time() < end_time:
            # 랜덤한 이웃해 생성
            exchange_idx1 = random.randint(0, city_count - 2)
            exchange_idx2 = random.randint(0, city_count - 2)

            neighbor = [i for i in self.best_path]
            neighbor[exchange_idx2], neighbor[exchange_idx1] = neighbor[exchange_idx1], neighbor[exchange_idx2]

            # 2개의 해의 거리 계산
            self.best_distance = int(GetDistanceFromRoute(self.best_path) + 0.5)
            neighbor_dist = int(GetDistanceFromRoute(neighbor) + 0.5)

            # 랜덤하게 찾은 이웃해가 더 좋은 해라면 current 업데이트
            if (self.best_distance > neighbor_dist):
                self.best_path = neighbor
                self.best_distance = neighbor_dist
                print(self.best_distance, self.best_path)
                DrawTour(self.best_path)


def RandomRestartFirstChoice():
    start_time = time.time()

    threads = []
    workers = []
    for i in range(5):
        worker = FirstChoiceWorker()
        thread = threading.Thread(target=worker.run)

        workers.append(worker)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


    # 스레드가 10분동안 동작하고 난 후, 가장 최적의 해를 찾아 출력
    best_distance = math.inf
    best_path = None
    for worker in workers:
        if(best_distance > worker.best_distance):
            best_distance = worker.best_distance
            best_path = worker.best_path

    print("탐색 끝")
    print(f"{best_distance} {best_path}")
    print(f"탐색시간 : {(time.time() - start_time)}초")


# GUI : 경로에 따라 그림 그리기
# tour : 시작 도시(0)를 제외한 경로 (예, [1, 2, 3, 4, 5])
import tkinter as tk

def DrawTour(path):
    canvas.delete(tk.ALL)
    x, y, idx = city_coords[0]

    x /= 10
    y /= 10
    canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")

    for city in path:
        next_x, next_y, next_idx = city_coords[city]

        next_x /= 10
        next_y /= 10

        canvas.create_line(x, y, next_x, next_y)
        x, y = next_x, next_y


        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue")

    next_x, next_y, next_idx = city_coords[0]

    next_x /= 10
    next_y /= 10

    canvas.create_line(x, y, next_x, next_y)


def Init():
    DrawTour(list(range(1, city_count)))

# GUI 화면 만들기
window = tk.Tk()
canvas = tk.Canvas(window, width = 1200, height = 600, bg = "white")
canvas.pack(expand = 1, fill = tk.BOTH)

label = tk.Label(window, text="distance")
label.pack(fill = tk.X)

btn = tk.Button(window, text = "Exhaustive Search", command = lambda : threading.Thread(target=ExhaustiveSearch).start())
btn2 = tk.Button(window, text = "First Choice", command = lambda : threading.Thread(target=FirstChoice).start())
btn3 = tk.Button(window, text = "Simulated Annealing", command = lambda : threading.Thread(target=SimulatedAnnealing).start())
btn4 = tk.Button(window, text = "Genetic Algorithm", command = lambda : threading.Thread(target=GeneticAlgorithm).start())
btn5 = tk.Button(window, text = "Random Restart First Choice", command = lambda : threading.Thread(target=RandomRestartFirstChoice).start())

btnInit = tk.Button(window, text = "Initialize", command = lambda : threading.Thread(target=Init).start())

btnInit.pack(fill = tk.X)
btn.pack(side="left", fill="both", expand=True)
btn2.pack(side="left", fill="both", expand=True)
btn3.pack(side="left", fill="both", expand=True)
btn4.pack(side="left", fill="both", expand=True)
btn5.pack(side="left", fill="both", expand=True)

Init()
window.mainloop()
