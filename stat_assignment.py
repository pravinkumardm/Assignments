import random
from datetime import datetime, timedelta
import numpy as np

def miles_per_hour_to_minute(mph):
    return mph/60

class Highway:
    def __init__(self, length, min_speed, max_speed):
        self.length = length
        self.min_speed = miles_per_hour_to_minute(min_speed)
        self.max_speed = miles_per_hour_to_minute(max_speed)
        
    
    def traverse(self, start_time):
        speed = random.uniform(self.min_speed, self.max_speed)
        timetaken = self.length / speed
        return start_time + timetaken
    

class Crossing:
    def __init__(self, frequency, wait_min, wait_max):
        self.frequency = frequency
        self.wait_min = wait_min
        self.wait_max = wait_max
    
    def cross(self, entry_time):
        if entry_time % self.frequency == 0:
            add_time = random.uniform(self.wait_min, self.wait_max)
        else:
            add_time = 0
        return entry_time + add_time

def get_travel_stats(route, start_time, iterations):
    travel_time = []
    for _ in range(iterations):
        iteration_time = start_time
        for item in route:
            if isinstance(item, Highway):
                iteration_time = item.traverse(iteration_time)
            elif isinstance(item, Crossing):
                iteration_time = item.cross(iteration_time)
        travel_time.append(iteration_time)
    return travel_time


if __name__ == "__main__":
    A = Highway(50, 45, 55)
    B = Highway(60, 45, 60)
    C = Highway(80, 50, 70)

    I = Crossing(15, 4, 8)
    II = Crossing(20, 5, 10)

    Route = [A, I, B, II, C]
    start_at = 30
    times = np.array(get_travel_stats(Route, start_at, 100000))
    # print(f'The stats of the travel time is mean = {np.mean(times)} min and standard deviation = {np.std(times)} min')
    st_time = datetime(2023,10,1,7,00,00)
    print(f'Start Time = {st_time+timedelta(minutes=start_at)}\nMean Time Reaching = {st_time + timedelta(minutes=np.mean(times))} with standard deviation of {np.std(times)} min')


    