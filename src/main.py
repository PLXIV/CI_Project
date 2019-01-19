from city import City
from view.drawer import Drawer
import threading
from time import sleep

def run_city(city):
    for i in range(10000):
        city.step()
        sleep(0.5)

if __name__ == "__main__":

    # City
    city = City(rows=20, cols=20, n_intersections=4)
    city.grid.generate(seed=27367)

    # Graphics
    drawer = Drawer(fps_target=120, city=city, width=800, height=800, margin=0)

    # Run
    t = threading.Thread(target=run_city, args=[city])
    t.start()
    drawer.run()
    t.join()
