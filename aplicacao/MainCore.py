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
        self.initialConditions()
        self.createObjects()
        self.WIDTH = 1000
        self.widgets = Widgets(self)
        self.graphs = Graphs(self.WIDTH, self)
        scene.width = self.WIDTH
        self.run()
        
    def createObjects(self):
        self.wall = box(pos = vector(-20, 0, 0), size = vector(1, 10, 10), color = color.red)
        self.ground = box(pos = vector(0, -5, 0), size = vector(50, 0.5, 10), color = color.blue)
        self.spring = helix(pos = vector(-20, -3, 0), radius = 1.5, thickness = 0.5, coils = 5, color = color.white, length = self.initialSpringLenght)  # coils = n de argolas
        self.spring_head = box(pos = vector(self.spring.pos.x +self.spring.axis.x, -3, 0), size = vector(0.5, 4, 4), color = vector(0.030392, 0.447059, 0.301961))
        self.block = box(pos = vector(7, -3, 0), size = vector(6, 4, 4), color = vector(1, 1, 0))

        self.block_text = label(text = str(self.block.pos.x), height = 20, box = False, line = False, opacity = 0)
        self.spring_head_text = label(text = str(self.spring_head.pos.x), height = 20, box = False, line = False, opacity = 0)
        self.colision_text = label(text = str(self.checkSpringColision()), height = 20, box = False, line = False, opacity = 0)

    def initialConditions(self):
        self.spring_head_vel = vector(0, 0, 0)
        self.k = 400 # constante elástica da mola
        self.m = 5 # massa
        self.t = 0 # tempo
        self.dt = 0.001 # acréscimo de tempo
        self.initialSpringLenght = 20

    def updateSpring(self):
        if self.widgets.spring_length_input.text == '':
            self.spring.length = 0    
        else:
            self.spring.length = float(self.widgets.spring_length_input.text)
        #print(self.spring.pos)
        print(self.spring.axis)
        print(self.spring.length)
        #print(self.spring_head.pos)
        #print(self.spring_head.size.x)
        self.linkAxis()

    def linkAxis(self):
        self.spring.axis = self.spring_head.pos - self.spring.pos        
        self.spring_head.pos.x = self.spring.pos.x +self.spring.axis.x
        
    # equações
    # k = intensidade de força necessária para deformação em 1 metro
    # x = deformação ou variação do corpo (mola). Em tamanho original, x=0 (não apresenta energia potencial elástica)
    # energia potencial elástica - EPel = (k * x²)/2 onde x  =deformação da mola
    # energia cinética - Ec = (mv²) /2

    def checkSpringColision(self):
        if self.block.pos.x <= self.spring_head.pos.x + self.block.size.x:
            return True
        return False
    
    def testBlock(self):
        self.block.pos.x = self.block.pos.x - (1 * self.dt) 

    def energyCalc(self):
        # Elatic Potential Energy        
        self.epe = (self.k * ((self.spring.lenght - self.initialSpringLenght)**2))/2 
        # Cinectic Energy
        self.ce = (self.m * (self.v**2))/2
        # Mechanical Energy
        self.me = self.epe + self.ce


    def run(self):
        while True:
            rate(500)
            #self.f = vector(-self.k * self.spring_head.pos.x , 0, 0) # Lei de Hooke; Força da mola
            #self.aceleration = self.f / self.m # força / massa
            #self.spring_head.pos = self.spring_head.pos + (self.spring_head_vel * self.dt) # incremento para movimentação do bloco
            #self.spring_head_vel = self.spring_head_vel + (self.aceleration * self.dt)
            self.t = self.t + self.dt
            self.testBlock()
            print(self.checkSpringColision())
            # self.linkAxis()
            # print(f"ace {self.aceleration}")
            # print(f"pos {self.spring_head.pos}")
            # print(f"vel {self.spring_head_vel}")

MainCore()