from city import City
from view.drawer import Drawer
import threading
from time import sleep
from random import choice

def run_genetics(city):
    number_of_lights = len(city.grid.roads_with_lights)

    for i in range(1000):
        # print(i)
        lights = [choice([True, False]) for i in range(number_of_lights)]
        city.step(lights)
        sleep(0.1)
    finess = city.cars_despawned
    print('fitness:',finess)


if __name__ == "__main__":

    # City
    city = City(rows=100, cols=100, n_intersections=1)
    city.grid.generate(seed=27367)



    # Graphics
    drawer = Drawer(fps_target=30, city=city, width=800, height=800, margin=0)

    # Run
    t = threading.Thread(target=run_genetics, args=[city])
    t.start()
    drawer.run()
    t.join()



