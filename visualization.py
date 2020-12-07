import numpy as np
from tkinter import *
from graphics import *

class Visualization:
    width = 800
    height = 600
    panel_width = 200
    numberOfVertex = 5
    window = GraphWin("graph", width, height)
    jams_color = np.full((5, 5), 255)
    node_info = [('A', 0, 50, 50), ('B', 1, 200, 50), ('C', 2, 400, 200), ('D', 3, 50, 400), ('E', 4, 200, 400)]
    panel_padding = 2
    source_ibbox = Entry(Point(width - panel_width // 2 - panel_padding, 30 + panel_padding * 2), 12)
    dest_ibbox = Entry(Point(width - panel_width // 2 - panel_padding, 100 + panel_padding * 2), 12)

    def __init__(self, matrix, jams) -> None:
        self.matrix = matrix
        self.jams = jams

    def drawGraph(self,matrix, n):
        jams_color = np.full((5, 5), 255)

        for x in self.node_info:
            c = Circle(Point(x[2], x[3]), 30)
            c.setFill("blue")
            c.draw(self.window)
            node_name = Text(Point(x[2], x[3]), x[0])
            node_name.setSize(30)
            node_name.draw(self.window)

            # draw edge, distance cost
            i = x[1]
            for j in range(n):
                if i != j and matrix[i][j] < 1000:
                    line = Line(Point(self.node_info[i][2], self.node_info[i][3]), Point(self.node_info[j][2], self.node_info[j][3]))

                    # jam detect
                    if self.jams[i][j][0] != -1:
                        jams_color[i][j] = max(self.jams_color[i][j] - 255 * self.jams[i][j][1], 0)
                        line.setWidth(5)
                        line.setOutline(color_rgb(255, np.int32(self.jams_color[i][j]), 0))

                    line.draw(self.window)
                    text_point = Point(np.abs(self.node_info[i][2] + self.node_info[j][2]) / 2,
                                       np.abs(self.node_info[i][3] + self.node_info[j][3]) / 2)
                    text = Text(text_point, matrix[i][j])
                    text.setSize(20)
                    text.draw(self.window)


    def drawDirectionPanel(self,panel_width):
        panel_area = Rectangle(Point(self.width - panel_width, 0), Point(self.width, self.height))
        panel_area.setFill(color_rgb(110, 119, 240))
        panel_area.setOutline("white")
        panel_area.draw(self.window)

        self.source_ibbox.setSize(20)
        self.source_ibbox.setFill("white")
        self.source_ibbox.draw(self.window)

        self.dest_ibbox.setSize(20)
        self.dest_ibbox.setFill("white")
        self.dest_ibbox.draw(self.window)

        bt_rect_find = Rectangle(Point(self.width - panel_width + 30, 150 + self.panel_padding * 2),
                                 Point(self.width - 30, 150 + self.panel_padding * 2 + 35))
        bt_rect_find.setFill(color_rgb(75, 86, 235))
        bt_rect_find.draw(self.window)
        text_bt_find = Text(bt_rect_find.getCenter(), "Find path")
        text_bt_find.draw(self.window)


    def find_min(self,result_matrix, unvisited, n):
        min = 1000
        index_min = unvisited[0]
        for i in unvisited:
            if (i != -1):
                if result_matrix[i][0] < min:
                    min = result_matrix[i][0]
                    index_min = i

        return index_min


    def find_path(self, matrix, n, source, dest):
        visited = np.zeros(n)
        unvisited = np.arange(0, n)
        result_matrix = np.full((5, 2), 1000)
        for i in range(n):
            result_matrix[i][1] = i
        result_matrix[source][0] = 0
        print(result_matrix)

        for i in range(n):
            current_city = self.find_min(result_matrix, unvisited, n)
            unvisited[current_city] = -1
            visited[current_city] = 1
            for j in unvisited:
                if j != -1:
                    if matrix[current_city][j] > 0 and matrix[current_city][j] < 1000:
                        if result_matrix[current_city][0] + matrix[current_city][j] < result_matrix[j][0]:
                            result_matrix[j][0] = result_matrix[current_city][0] + matrix[current_city][
                                j]  # update shortest path
                            result_matrix[j][1] = current_city  # update prev city
        print(result_matrix)

        return result_matrix


    def drawResultPath(self,result_matrix, source, dest):
        current_city = dest
        prev_city = result_matrix[dest][1]
        while prev_city != source:
            line = Line(Point(self.node_info[current_city][2], self.node_info[current_city][3]),
                        Point(self.node_info[prev_city][2], self.node_info[prev_city][3]))
            line.setFill(color_rgb(52, 235, 140))
            line.setWidth(5)
            line.draw(self.window)

            current_city = prev_city
            prev_city = result_matrix[current_city][1]

        line = Line(Point(self.node_info[current_city][2], self.node_info[current_city][3]),
                    Point(self.node_info[prev_city][2], self.node_info[prev_city][3]))
        line.setFill(color_rgb(52, 235, 140))
        line.setWidth(5)
        line.draw(self.window)


    def dijkstra(self,matrix, n):
        self.drawGraph(matrix, n)
        self.drawDirectionPanel(self.panel_width)

        while True:
            mouse = self.window.getMouse()
            if mouse.getX() > self.width - self.panel_width + 30 and mouse.getX() < self.width - 30 and mouse.getY() > 150 and mouse.getY() < 185:
                self.window.update()
                self.drawGraph(matrix, n)

                source = ord(self.source_ibbox.getText().upper()) - 65
                dest = ord(self.dest_ibbox.getText().upper()) - 65
                result_matrix = self.find_path(matrix, n, source, dest)

                self.drawResultPath(result_matrix, source, dest)

            else:
                mouse = self.window.getMouse()


def draw(matrix, jams, numberOfVertex=5):
    visualizator = Visualization(matrix, jams)
    visualizator.dijkstra(matrix, numberOfVertex)


if __name__ == '__main__':
    # data
    # [jam area, muy, v]
    jams = [[(-1, 0.4, 0.5), (1, 0.1, 0.6), (2, 0.8, 0.15), (1, 0.7, 0.12), (0, 0.5, 0.3)],
            [(1, 0.1, 0.6), (-1, 0, 0), (-1, 0.8, 0.15), (1, 0.7, 0.12), (-1, 0.5, 0.3)],
            [(2, 0.8, 0.15), (-1, 0.8, 0.15), (-1, 0, 0), (-1, 0.7, 0.12), (-0, 0.5, 0.3)],
            [(1, 0.7, 0.12), (1, 0.7, 0.12), (-1, 0.7, 0.12), (-1, 0, 0), (-1, 0.5, 0.3)],
            [(0, 0.5, 0.3), (-1, 0.5, 0.3), (-0, 0.5, 0.3), (-1, 0.5, 0.3), (-1, 0, 0)],
            ]

