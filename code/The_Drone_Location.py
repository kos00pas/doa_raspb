import time
import pandas as pd
import numpy as np
import haversine
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class The_Drone_Location:
    def __init__(self):
        self.fig = plt.figure()
        self.axis_tdoa3d = self.fig.add_subplot(111, projection='3d')
        self.max_radius = 250
        self.set_sphere()
        self.process_csv()
        plt.show()

    def process_csv(self):
        data_frame = pd.read_csv('data3.csv', delimiter=';')
        column2_data = data_frame.iloc[:, 1].tolist()  # 2nd column
        column5_data = pd.to_numeric(data_frame.iloc[:, 4], errors='coerce').tolist()  # 5th column
        column6_data = pd.to_numeric(data_frame.iloc[:, 5], errors='coerce').tolist()  # 6th column
        column7_data = pd.to_numeric(data_frame.iloc[:, 6], errors='coerce').tolist()  # 7th column
        column23_data = pd.to_numeric(data_frame.iloc[:, 22], errors='coerce').tolist()  # 23rd column

        data = []

        for i in range(len(column2_data)):
            if not np.isnan(column5_data[i]) and not np.isnan(column6_data[i]) and not np.isnan(column7_data[i]) and not np.isnan(column23_data[i]):
                current_data = {
                    't': column2_data[i],
                    'x': column5_data[i],
                    'y': column6_data[i],
                    'z': column7_data[i] * 0.3048,
                    'yaw': column23_data[i]
                }
                data.append(current_data)

        center = np.array([data[0]['x'], data[0]['y'], data[0]['z']])
        center_xy = (data[0]['x'], data[0]['y'])

        for i in range(len(data)):
            current_xy = (data[i]['x'], data[i]['y'])
            x1 = haversine.haversine(center_xy, current_xy, unit='m')
            z1 = data[i]['z']
            d2 = math.sqrt(x1**2 + z1**2)
            t = data[i]['t']
            if x1 == 0:
                x1 = 0.1
            elev_rad = math.atan(z1 / x1)
            elev_deg = math.degrees(elev_rad)
            azimuth_deg = data[i]['yaw']

            print(f"d:{d2:.1f} | elv:{elev_deg:.1f} | azm:{azimuth_deg:.1f} | t:{t} ||xy{current_xy}")
            self.update_plot(d2, elev_deg, azimuth_deg)
            # time.sleep(1)  # Adjust delay for better visualization

    def update_plot(self, dist, elev_deg, azim_deg):
        # Clear the previous plot
        self.axis_tdoa3d.cla()  # Use cla() to clear the axis instead of clear()
        self.set_sphere()

        elev_deg= 15.4  ;azim_deg=44.3
        dist= 224.9

        azimuth_rad = np.radians(azim_deg)
        elevation_rad = np.radians(elev_deg)

        if dist > self.max_radius:
            dist = self.max_radius
        x = dist * np.cos(azimuth_rad) * np.cos(elevation_rad)
        y = dist * np.sin(azimuth_rad) * np.cos(elevation_rad)
        z = np.abs(dist * np.sin(elevation_rad))  # Ensuring positive Z values

        print(x, y, z)

        # Plot the new data
        self.axis_tdoa3d.plot([0, x], [0, y], [0, z], color='red')
        self.axis_tdoa3d.scatter(x, y, z, color='black')  # Black dot at the end of the line
        self.axis_tdoa3d.plot([x, x], [y, y], [0, z], color='black')  # Vertical line to z-axis
        self.axis_tdoa3d.plot([0, x], [0, y], [0, 0], color='black')  # Horizontal projection

        plt.show()
        # plt.pause(0.01)  # Allow the plot to update

    def set_sphere(self):
        def plot_sphere():
            u = np.linspace(0, 2 * np.pi, 100)
            v = np.linspace(0, np.pi / 2, 100)  # Only plotting the upper hemisphere
            x = self.max_radius * np.outer(np.cos(u), np.sin(v))
            y = self.max_radius * np.outer(np.sin(u), np.sin(v))
            z = self.max_radius * np.outer(np.ones(np.size(u)), np.cos(v))
            self.axis_tdoa3d.plot_wireframe(x, y, z, color='blue', alpha=0.1)
            self.axis_tdoa3d.plot([0, self.max_radius], [0, 0], [0, 0], color='black', alpha=0.6)

        def plot_angles():
            angles_degrees = [0, 45, 90, 135, 180, 225, 270, 315]  # Angles to plot
            for angle_degrees in angles_degrees:
                azimuth_degrees = angle_degrees
                elevation_degrees = 0  # At z=0
                distance = self.max_radius * 1.2  # To position outside the sphere
                if distance > self.max_radius:
                    distance = self.max_radius
                azimuth_rad = np.radians(azimuth_degrees)
                elevation_rad = np.radians(elevation_degrees)

                x = distance * np.cos(azimuth_rad) * np.cos(elevation_rad)
                y = distance * np.sin(azimuth_rad) * np.cos(elevation_rad)
                z = np.abs(distance * np.sin(elevation_rad))  # Ensuring positive Z values
                self.axis_tdoa3d.text(x, y, z, f'{angle_degrees}°', fontsize=12, color='green')

        plot_sphere()
        plot_angles()
        self.axis_tdoa3d.set_xlim([-self.max_radius, self.max_radius])
        self.axis_tdoa3d.set_ylim([-self.max_radius, self.max_radius])
        self.axis_tdoa3d.set_zlim([0, self.max_radius])
        self.axis_tdoa3d.set_xlabel('-X / X')
        self.axis_tdoa3d.set_ylabel('-Y / Y')
        self.axis_tdoa3d.set_zlabel('Z')

# Create an instance of the class to run the process
The_Drone_Location()
