"""
  __  __       _          _____               
 |  \/  |     (_)        / ____|              
 | \  / | __ _ _ _ __   | |     ___  _ __ ___ 
 | |\/| |/ _` | | '_ \  | |    / _ \| '__/ _ \
 | |  | | (_| | | | | | | |___| (_) | | |  __/
 |_|  |_|\__,_|_|_| |_|  \_____\___/|_|  \___| v 0.1
                          
"""
from vpython import *
from ScreenCore import Widgets, Graphs

class MainCore:
    def __init__(self) -> None:
        self.createObjects()
        self.linkAxis()
        self.initialConditions()
        self.WIDTH = 1000
        self.widgets = Widgets(self)
        self.graphs = Graphs(self.WIDTH, self)
        scene.width = self.WIDTH
        self.run()

    def createObjects(self):
        self.wall = box(pos = vector(-20, 0, 0), size = vector(1, 10, 10), color = color.yellow)
        self.block = box(pos = vector(5, -3, 0), size = vector(4, 4, 4), color = color.red)
        self.ground = box(pos = vector(0, -5, 0), size = vector(50, 0.5, 10), color = color.green)
        self.spring = helix(pos = vector(-20, -3, 0), radius = 1.5, thickness = 0.5, coils = 5, color = color.blue)  # coils = n de argolas
    
    def linkAxis(self):
        self.spring.axis = self.block.pos - self.spring.pos
    
    def initialConditions(self):
        self.block.vel = vector(0, 0, 0)
        self.k = 400 # constante elástica da mola
        self.m = 5 # massa
        self.t = 0 # tempo
        self.dt = 0.001 # acréscimo de tempo

    def updateSpring(self):
        if self.widgets.spring_length_input.text == '':
            self.spring.length = 0    
        else:
            self.spring.length = float(self.widgets.spring_length_input.text)

    # equações
    # k = intensidade de força necessária para deformação em 1 metro
    # x = deformação ou variação do corpo (mola). Em tamanho original, x=0 (não apresenta energia potencial elástica)
    #nergia potencial elástica - EPel = (k * x²)/2 onde x  =deformação da mola
    #energia cinética - Ec = mv² /2
    def run(self):
        while True:
            rate(500)
            self.f = vector(-self.k * self.block.pos.x , 0, 0) # Lei de Hooke; Força da mola
            self.ace = self.f / self.m # força / massa
            self.block.pos = self.block.pos + (self.block.vel * self.dt) # incremento para movimentação do bloco
            self.block.vel = self.block.vel + (self.ace * self.dt)
            self.t = self.t + self.dt
            self.linkAxis()
