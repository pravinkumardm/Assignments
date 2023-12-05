import random
import math
import matplotlib.pyplot as plt

list_of_points_1 = [(random.randint(0,100), random.randint(0,100)) for x in range(200)]
list_of_points_2 = [(random.randint(40,100), random.randint(30,100)) for x in range(200)]
list_of_points = list_of_points_1 #+ list_of_points_2
er_threshold = 10


def compute_distance(x, y):
    return math.sqrt(
        ((x[0]-y[0])**2 ) + 
        ((x[1]-y[1])**2)
        )

def getting_class_points(list_of_points, center1, center2):
    class1 = []
    class2 = []
    for point in list_of_points:
        d1 = compute_distance(center1, point)
        d2 = compute_distance(center2, point)
        if d1 > d2:
            class1.append(point)
        else:
            class2.append(point)
    return [class1, class2]

def get_mean_centers(class_list):
    x_list = [i[0] for i in class_list]
    y_list = [i[1] for i in class_list]
    x = sum(x_list) / len(x_list)
    y = sum(y_list) / len(y_list)
    return (x,y)


def error_measure(center1_old, center1_new, center2_old, center2_new):
    class1_distance = compute_distance(center1_new, center1_old)
    class2_distance = compute_distance(center2_new, center2_old)
    return [class1_distance, class2_distance]


def kmeans_algo(list_of_points):
    center1 = (random.randint(0,100), random.randint(0,100))
    center2 = (random.randint(0,100), random.randint(0,100))
    iterate = True
    error_old = random.randint(1564897, 15647849)
    count = 0
    print(f"Starting with Centers : {center1} and {center2}")
    while iterate and count<20:
        print(f"\n\n======================Iteration Number : {count} ===================\n")
        class1, class2 = getting_class_points(list_of_points, center1, center2)
        print(f"Classified data = {len(class1)} and {len(class2)}")
        center1_new = get_mean_centers(class1)
        center2_new = get_mean_centers(class2)
        plt.scatter(x=[x[0] for x in class1], y=[x[1] for x in class1], c="#ff0000")
        plt.scatter(x=[x[0] for x in class2], y=[x[1] for x in class2], c="#0000ff")
        plt.scatter(x=[center1[0], center2[0]], y=[center1[1], center2[1]], marker="x", sizes=[200], c="#111")
        plt.scatter(x=[center1_new[0], center2_new[0]], y=[center1_new[1], center2_new[1]], marker="+", sizes=[200], c="#111")
        plt.show()
        print(f"Updated  Centers : {center1_new} and {center2_new}")
        error = error_measure(center1, center1_new, center2, center2_new)
        print(f"Measured_Error : {error_old/sum(error)} ")
        # print(f"{0.95 < error_old/sum(error) < 1.05}")
        count += 1
        if 0.99 < error_old/sum(error) < 1.02:
            iterate = False
        else:
            center1, center2 = center1_new, center2_new
            error_old = sum(error)

if __name__ == "__main__":
    kmeans_algo(list_of_points)
