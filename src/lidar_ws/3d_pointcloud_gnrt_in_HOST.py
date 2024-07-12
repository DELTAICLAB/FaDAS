"""import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x_vals = []
y_vals = []
z_vals = []

with open('point_cloud.csv', mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Başlık satırını atla
    for row in reader:
        x_vals.append(float(row[0]))
        y_vals.append(float(row[1]))
        z_vals.append(float(row[2]))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_vals, y_vals, z_vals, s=1)
ax.set_title('3D Point Cloud')
ax.set_xlabel('X (mm)')
ax.set_ylabel('Y (mm)')
ax.set_zlabel('Z (mm)')

plt.show()"""

import socket
import struct
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import threading
import queue

# UDP ayarları
UDP_IP = "0.0.0.0"
UDP_PORT = 5005

# Soket oluşturma
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Veri tamponu
data_queue = queue.Queue()

# Veri alma thread'i
def receive_data():
    while True:
        data, addr = sock.recvfrom(1024)  # Veri al
        if data:
            data_queue.put(data)

# Görselleştirme thread'i
def visualize_data():
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    x_vals = []
    y_vals = []
    z_vals = []
    
    while True:
        while not data_queue.empty():
            data = data_queue.get()
            if data:
                # Gelen veriyi çözümle (her veri noktası 3 adet float değer içeriyor)
                point = struct.unpack('fff', data[:12])
                x_vals.append(point[2])  # Z ekseni olarak eski X değerini kullan
                y_vals.append(point[1])
                z_vals.append(point[0])  # X ekseni olarak eski Z değerini kullan
        
        # Anlık güncelleme
        ax.clear()
        ax.scatter(x_vals, y_vals, z_vals, s=1)
        ax.set_title('3D Point Cloud')
        ax.set_xlabel('Z (mm)')  # X etiketi yerine Z
        ax.set_ylabel('Y (mm)')
        ax.set_zlabel('X (mm)')  # Z etiketi yerine X
        plt.draw()
        plt.pause(0.01)

# Thread'leri başlatma
receive_thread = threading.Thread(target=receive_data)
visualize_thread = threading.Thread(target=visualize_data)

receive_thread.start()
visualize_thread.start()

receive_thread.join()
visualize_thread.join()


