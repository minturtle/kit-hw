# 데이터 파일 읽기
file = open("point20.txt", "r")
data = file.read().split()
data = [eval(i) for i in data]
import threading


# 지정시간이 지나면 프로그램을 종료하는 함수
def timeout():
    print("10분이 지나 프로그램이 종료됩니다.")
    # 프로그램 종료
    import os
    os._exit(0)


# 도시 좌표 데이터 만들기
#city_count = data[0]
city_count = 10
city_coords = []
for i in range(1, len(data), 2):
    city_coords.append((data[i], data[i + 1]))


# 두 도시 좌표 사이의 거리 구하기
import math
def GetDistance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

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

def FindShortestPath():
    # 600초가 지나면 프로그램이 종료되도록 함.
    timer = threading.Timer(600, timeout)
    timer.start()

    shortest_distance = math.inf
    shortest_path = None
    start_time = time.time()

    iter = itertools.permutations(range(1, city_count))
    for path in iter:
        dist = distance[0][path[0]]
        for i in range(len(path) - 1):
            dist += distance[path[i]][path[i + 1]]
        dist += distance[path[-1]][0]

        if dist < shortest_distance:
            shortest_distance = dist
            shortest_path = path
            print(shortest_distance, path)
            DrawTour(path)

    print("탐색 끝")
    print(f"탐색시간 : {(time.time() - start_time)}초")
    timer.cancel()
    label.configure(text = shortest_distance)

# GUI : 경로에 따라 그림 그리기
# tour : 시작 도시(0)를 제외한 경로 (예, [1, 2, 3, 4, 5])
import tkinter as tk

def DrawTour(path):
    canvas.delete(tk.ALL)
    x, y = city_coords[0]
    canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red")

    for city in path:
        next_x, next_y = city_coords[city]
        canvas.create_line(x, y, next_x, next_y)
        x, y = next_x, next_y
        canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue")

    next_x, next_y = city_coords[0]
    canvas.create_line(x, y, next_x, next_y)

# GUI 화면 만들기
window = tk.Tk()
canvas = tk.Canvas(window, width = 600, height = 600, bg = "white")
canvas.pack(expand = 1, fill = tk.BOTH)

label = tk.Label(window, text="distance")
label.pack(fill = tk.X)

btn = tk.Button(window, text = "Start", command = lambda : threading.Thread(target=FindShortestPath).start())
btn.pack(fill = tk.X)
DrawTour(list(range(1, city_count)))

window.mainloop()
