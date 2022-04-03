"""
  __  __       _          _____               
 |  \/  |     (_)        / ____|              
 | \  / | __ _ _ _ __   | |     ___  _ __ ___ 
 | |\/| |/ _` | | '_ \  | |    / _ \| '__/ _ \
 | |  | | (_| | | | | | | |___| (_) | | |  __/
 |_|  |_|\__,_|_|_| |_|  \_____\___/|_|  \___| v 0.2
                          
"""
from vpython import *
from ScreenCore import Widgets, Graphs
import math

class MainCore:
    def __init__(self) -> None:
        self.initialConditions()
        self.createObjects()
        self.widgets = Widgets(self)
        self.graphs = Graphs(self.WIDTH, self)
        scene.width = self.WIDTH
        self.is_running = True
        
    def createObjects(self):
        self.ground = box(pos = vector((self.ground_size.x * .5) + (self.wall_size.x * .5), -5, 0), size = self.ground_size, color = vector(1, 1, 1))
        self.friction_ground = box(pos = vector(self.ground.pos.x, self.ground.pos.y , (self.ground.pos.z)), size = self.friction_ground_size, color = vector(1,0,0))
        self.wall = box(pos = vector(0, self.ground.size.y * .5, 0), size = self.wall_size, color = vector(0, 1, 1))
        self.spring = helix(pos = vector(0, -3, 0), radius = 1.5, thickness = 0.5, coils = 5, color = vector(1, 1, 1), length = self.initial_spring_lenght)  # coils = n de argolas
        self.spring_head = box(pos = vector(self.spring.pos.x + self.spring.axis.x, -3, 0), size = vector(0.5, 4, 4), color = vector(0.030392, 0.447059, 0.301961))
        self.block = box(pos = vector(self.ground_size.x * .90, -3, 0), size = vector(6, 4, 4), color = vector(1, 1, 0))        
        self.spring.rotate(1.4*pi)
        scene.follow(self.spring_head)   
        
        self.block_min_pos = self.wall_size.x + self.spring.length + self.spring_head.size.x + (self.block.size.x * .5)     

    def initialConditions(self):
        # scene initial
        self.WIDTH = 1000
        self.ground_size = vector(100, 0.5, 10)
        self.friction_ground_size = vector(100, 0.6, 10.1)
        self.wall_size = vector(1, 10, 10)
        self.initial_spring_lenght = 20
        self.spring_head_vel = vector(0, 0, 0)
        self.block_vel = vector(0,0,0)
        self.is_coming = True
        self.is_block_repelled = False
        self.is_limit = False
        # calc initial
        self.k = 10 # constante elástica da mola
        self.block_mass = 0 # massa
        self.t = 0 # tempo
        self.dt = 0.001 # acréscimo de tempo
        self.epe = 0
        self.ce = 1
        self.me = 0
        self.force = 0
        self.aceleration = 0
        
       

    def getAllInfo(self):
        self.setSpringLength()
        self.setBlockVelocity()
        self.setBlockMass()
        self.updateCalcInfo()

    def setBlockVelocity(self):
        if self.widgets.block_initial_velocity_input.text == '':
            self.block_vel.x = 0    
        else:
            self.block_vel.x = float(self.widgets.block_initial_velocity_input.text)

    def setBlockMass(self):
        if self.widgets.block_mass_input.text == '':
            self.block_mass = 0    
        else:
            self.block_mass = float(self.widgets.block_mass_input.text)

    def setSpringLength(self):
        if self.widgets.spring_length_input.text == '':
            self.initial_spring_lenght = 1
            self.spring.length = self.initial_spring_lenght    
        else:
            self.initial_spring_lenght = float(self.widgets.spring_length_input.text) 
            self.spring.length = self.initial_spring_lenght
        self.linkAxis()
        
    def updateSpring(self):
        if self.is_block_repelled:
            if self.spring.length < self.initial_spring_lenght:
                self.spring.length = self.spring.length + (self.block_vel.x * self.dt)
                self.linkAxis()
        else:    
            self.spring.length = self.spring.length + (self.block_vel.x * self.dt)
            self.linkAxis()
        # if self.is_coming:
        #     self.spring.length = self.spring.length + (self.block_vel.x * self.dt)
        # else: 
        #     self.spring.length = self.spring.length - (self.block_vel.x * self.dt)
        
    def checkSpringLimit(self):
        if self.spring.length <= 1 and self.ce > 0:
            self.block_vel.x = 0
            self.aceleration = 0
            self.is_limit = True
            # self.block.pos.x = self.block_min_pos
        
    def linkAxis(self):       
        self.spring_head.pos.x = self.spring.pos.x + self.spring.axis.x
        
    def checkSpringColision(self):
        if self.block.pos.x <= self.spring_head.pos.x + (self.spring_head.size.x * .5) + (self.block.size.x * .5):
            return True
        return False

    def checkSpringComportament(self):
        if self.block_vel.x > 0:
            self.is_block_repelled = True
    
    def moveBlock(self):
        if not self.is_block_repelled:
            self.block.pos.x = self.block.pos.x - (self.block_vel.x * self.dt)
        else:
            self.block.pos.x = self.block.pos.x + (self.block_vel.x * self.dt)
            
    def updateCalcInfo(self):
        self.widgets.epe_info.text = f"{self.epe:.2f}"
        self.widgets.ce_info.text =  f"{self.ce:.2f}"
        self.widgets.me_info.text = f"{self.me:.2f}"
        self.widgets.block_vel_info.text = f"{self.block_vel.x}"
        self.widgets.block_pos_x_info.text = self.block.pos.x
        self.widgets.block_head_pos_x_info.text = self.spring_head.pos.x
        self.widgets.block_aceleration_info.text = self.aceleration
        
    #! equações
    #? k = intensidade de força necessária para deformação em 1 metro
    #* x = deformação ou variação do corpo (mola). Em tamanho original, x=0 (não apresenta energia potencial elástica)
    #? energia potencial elástica - EPel = (k * x²)/2 onde x = deformação da mola
    #* energia cinética - Ec = (mv²) /2

    def energyCalc(self):
        # Elatic Potential Energy        
        self.epe = (self.k * ((self.initial_spring_lenght - self.spring.length)**2))/2 
        # Cinectic Energy
        self.ce = (self.block_mass * (self.block_vel.x**2))/2
        # Mechanical Energy
        self.me = self.epe + self.ce
        
    def calcBlockVel(self):
        if not self.is_limit:
            self.force = -self.k * (self.initial_spring_lenght - self.spring.length) # Lei de Hooke; Força da mola
            self.aceleration = math.floor((self.force / self.block_mass)) * -1 # força / massa
            self.block_vel.x = self.block_vel.x + (self.aceleration * self.dt)
            self.block.pos.x = self.block.pos.x + (self.block_vel.x * self.dt) # incremento para movimentação do bloco

    def run(self):
        while True:
            while self.is_running:
                rate(500)
                # self.moveBlock()
                if self.checkSpringColision() or self.is_block_repelled: self.updateSpring()
                self.energyCalc()
                self.checkSpringLimit()
                self.calcBlockVel()
                self.checkSpringComportament()
                self.updateCalcInfo()
            
    def pause(self):
        if self.is_running:
            self.is_running = False
        else:
            self.is_running = True
            

MainCore()