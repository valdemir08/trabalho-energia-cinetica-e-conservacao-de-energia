from turtle import color
from numpy import block
from vpython import *

class TrabalhoEnergiaCineticaEConservacaoDeEnergia:
    def __init__(self) -> None:
        self.createObjects()
        self.linkAxis()
        self.initialConditions()
        self.run()

    def createObjects(self):
        self.wall = box(pos = vector(-20, 0, 0), size = vector(1, 10, 10), color = color.yellow)
        self.block = box(pos = vector(5, -3, 0), size = vector(4, 4, 4), color = color.red)
        self.ground = box(pos = vector(0, -5, 0), size = vector(50, 0.5, 10), color = color.green)
        self.spring = helix(pos = vector(-20.5, -3, 0), radius = 1.5, thickness = 0.5, coils = 5, color = color.blue)#coils = n de argolas
    
    def linkAxis(self):
         self.spring.axis = self.block.pos  - self.spring.pos
    
    def initialConditions(self):
        self.block.vel = vector(0, 0, 0)
        self.k = 400 #constante elástica da mola
        self.m = 5 #massa
        self.t = 0 #tempo
        self.dt = 0.001 #acréscimo de tempo

    #equações
    def run(self):
        while True:
            rate(500)
            self.f = vector(-self.block.pos.x * self.k, 0, 0)#Lei de Hookie; Força da mola
            self.ace = self.f/self.m # força / massa
            self.block.pos = self.block.pos + (self.block.vel * self.dt) #incremento para movimentação do bloco
            self.block.vel = self.block.vel + (self.ace * self.dt)
            self.t = self.t + self.dt
            self.linkAxis()

