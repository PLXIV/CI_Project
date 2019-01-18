from timeit import default_timer as timer


class FPSCounter:

    UPDATE_INTERVAL = 1  # seconds

    def __init__(self):
        self.ticks = 0
        self.elapsed = 0
        self.last = timer()
        self.fps = 0

    def tick(self):
        self.ticks += 1
        self.elapsed += timer() - self.last
        self.last = timer()

        if self.elapsed > FPSCounter.UPDATE_INTERVAL:
            self.fps = self.ticks / self.elapsed
            self.ticks = 0
            self.last = timer()
            self.elapsed = 0

        return self.fps
