import numpy
import random
import pyglet

colours = [(0, 0, 0), (255, 255, 255)]


class Universe:
    def __init__(self, size=50, pixel=10, prob=0.3):
        self.size = size
        self.pixel = pixel
        self.prob = prob

    # initialize seed
    def init_grid(self):
        self.grid = []
        for i in range(self.size):
            a = []
            for j in range(self.size):
                if random.random() <= self.prob:
                    a.append(1)
                else:
                    a.append(0)
            self.grid.append(a)

    # neighbours in a square grid
    def count_neighbours(self, i, j):
        neighbours = 0
        g = self.grid
        if i in range(1, self.size-1) and j in range(1, self.size-1):
            neighbours = [g[i-1][j-1], g[i-1][j], g[i-1][j+1], g[i]
                          [j-1], g[i][j+1], g[i+1][j], g[i+1][j+1], g[i+1][j-1]]
        else:
            if i in range(1, self.size-1):
                if j == self.size-1:
                    neighbours = [g[i-1][j-1], g[i-1][j],
                                  g[i][j-1], g[i+1][j-1], g[i+1][j]]
                elif j == 0:
                    neighbours = [g[i-1][0], g[i-1][1],
                                  g[i][1], g[i+1][0], g[i+1][1]]
            elif j in range(1, self.size-1):
                if i == self.size-1:
                    neighbours = [g[i-1][j-1], g[i-1][j],
                                  g[i][j-1], g[i-1][j+1], g[i][j+1]]
                elif i == 0:
                    neighbours = [g[1][j], g[1][j+1],
                                  g[0][j+1], g[1][j-1], g[0][j-1]]
            else:
                if i == 0:
                    if j == 0:
                        neighbours = [g[0][1], g[1][1], g[1][0]]
                    elif j == self.size-1:
                        neighbours = [g[0][j-1], g[1][j-1], g[1][j]]
                elif i == self.size - 1:
                    if j == 0:
                        neighbours = [g[i][1], g[i-1][1], g[i-1][0]]
                    elif j == self.size-1:
                        neighbours = [g[i][j-1], g[i-1][j-1], g[i-1][j]]
        return neighbours.count(1)

    # rules as a function
    def next_cell(self, i, j):
        n = self.count_neighbours(i, j)
        g = self.grid[i][j]
        if g == 1 and (n < 2 or n > 3):
            return 0
        elif g == 1 and (n == 2 or n == 3):
            return 1
        elif g == 0 and n == 3:
            return 1
        else:
            return 0

    # update the whole grid
    def next_gen(self):
        new = []
        for i in range(self.size):
            x = []
            for j in range(self.size):
                x.append(self.next_cell(i, j))
            new.append(x)
        return new

    # render the grid in graphics
    def render(self, dt, window=None):
        if not window:
            window = pyglet.window.Window()

        @window.event
        def on_draw():
            window.clear()
            for i in range(self.size):
                for j in range(self.size):
                    pyglet.shapes.Rectangle(
                        x=self.pixel*i, y=self.pixel * j, width=self.pixel, height=self.pixel, color=colours[self.grid[i][j]]).draw()
        if not window:
            pyglet.app.run()
        if window:
            self.grid = self.next_gen()

    # animations
    def animate(self):
        window = pyglet.window.Window(
            width=self.pixel*self.size, height=self.pixel*self.size)
        pyglet.clock.schedule_interval(self.render, 1./60., window)
        pyglet.app.run()


# implimentation
def main():
    size = int(input("Enter the number of pixels you want to be in a row: "))
    pixel = int(input("Enter the size of a pixel you want to see (in pixels): "))
    probability = float(
        input("Enter probability for a cell to be living in initial state: "))
    uni = Universe(size, pixel, probability)
    uni.init_grid()
    uni.animate()


# final call
main()
