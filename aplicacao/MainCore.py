"""
  __  __       _          _____               
 |  \/  |     (_)        / ____|              
 | \  / | __ _ _ _ __   | |     ___  _ __ ___ 
 | |\/| |/ _` | | '_ \  | |    / _ \| '__/ _ \
 | |  | | (_| | | | | | | |___| (_) | | |  __/
 |_|  |_|\__,_|_|_| |_|  \_____\___/|_|  \___| v 0.4.1
                          
"""
from turtle import pos
from numpy import block
from vpython import *
from ScreenCore import Widgets, Graphs
import math

class MainCore:
    def __init__(self) -> None:
        self.initialConditions()
        self.createObjects()
        self.createScreenText()
        self.configCamera()
        self.widgets = Widgets(self)
        self.graphs = Graphs(self.WIDTH, self)
        self.linkAxis()
        
    def createObjects(self):
        #? chão (branco)
        self.ground = box(pos = vector((self.ground_size.x * .5) + (self.wall_size.x * .5), -5, 0), size = self.ground_size, color = vector(1, 1, 1))
        #? chão com atrito (vermelho)
        self.friction_ground = box(pos = vector(self.ground.pos.x, self.ground.pos.y , (self.ground.pos.z)), size = self.friction_ground_size, color = vector(1,0,0))
        #? parede
        self.wall = box(pos = vector(0, self.ground.size.y * .5, 0), size = self.wall_size, color = vector(0, 1, 1))
        #? mola
        self.spring = helix(pos = vector(0, -3, 0), radius = 1.5, thickness = 0.5, coils = 5, color = vector(1, 1, 1), length = self.initial_spring_lenght)  
        self.spring.rotate(1.4*pi)
        #? cabeça da mola
        self.spring_head = box(pos = self.initial_block_pos, size = vector(0.5, 4, 4), color = vector(0.030392, 0.447059, 0.301961))
        #? block
        self.block = box(pos = vector(self.ground_size.x * .90, -3, 0), size = vector(6, 4, 4), color = vector(1, 1, 0))        
        #? posição minima do block (evita o bloco de atravessar a parede)
        self.block_min_pos = self.wall_size.x + self.spring.length + self.spring_head.size.x + (self.block.size.x * .5)     
        
    def createScreenText(self):
        #? texto da velocidade
        self.block_vel_text = label(text = f"V: {str(self.block_vel.x)} m/s", height = 15, box = False, line = False, opacity = 0, aling = 'right', pos = vector(self.block.pos.x, self.block.pos.y + 5, self.block.pos.z))
        
        #? texto da energia cinética
        self.block_ce_text = label(text = f"EC: {self.ce:.0f} J", height = 15, box = False, line = False, opacity = 0, aling = 'right', pos = vector(self.block.pos.x, self.block.pos.y + 8, self.block.pos.z))
        
        #? texto da energia potencial elástica
        self.block_epe_text = label(text = f"EPE: {self.epe:.0f} J", height = 20, box = False, line = False, opacity = 0, aling = 'right', pos = vector(self.ground.pos.x * .15, self.ground.pos.y - 7, self.ground.pos.z))
        
        #? texto da energia potencial elástica
        self.block_me_text = label(text = f"ME: {self.me:.0f} J", height = 20, box = False, line = False, opacity = 0, aling = 'right', pos = vector(self.ground.pos.x, self.ground.pos.y - 7, self.ground.pos.z))  
        
    #? configura a camera da simulação    
    def configCamera(self):
        scene.camera.pos = vector(50.5, 16.216, 42.8217)
        scene.camera.axis = vector(3.94291e-16, -16.8615, -42.2158)  
        
    #? configura os valores iniciais    
    def initialConditions(self):
        #? valores iniciais dos objetos
        self.is_running = True
        self.WIDTH = 1000
        scene.width = self.WIDTH
        self.wall_size = vector(1, 10, 10)
        self.ground_size = vector(100, 0.5, 10)
        self.friction_ground_size = vector(100, 0.6, 10.1)
        self.initial_block_pos = vector(self.ground_size.x * .90, -3, 0)
        self.initial_spring_lenght = 20
        self.spring_head_vel = vector(0, 0, 0)
        self.block_vel = vector(0,0,0)
        self.is_coming = True
        self.is_block_repelled = False
        self.is_limit = False
        
        #? valores iniciais dos calculos
        self.t = 0 # tempo
        self.dt = 0.001 # acréscimo de tempo
        self.k = 0 # constante elástica da mola
        self.block_mass = 0 # massa
        self.block_weight = 0
        self.epe = 0
        self.ce = 0
        self.me = 0
        self.force = 0
        self.aceleration = 0
        self.dynamic_friction_coefficient = 0
        self.is_friction = False
        self.friction_force = 0
        self.work = 0
        self.friction_d = 0
        self.gravity = 9.8
    
    #? captura toda informação cedida pelo usuário    
    def setAllInfo(self):
        self.setSpringLength()
        self.setBlockVelocity()
        self.setBlockMass()
        self.setSpringElasticConstant()
        self.setDynamicFrictionCoefficient()

    #? determina a velocidade do bloco de acordo com a informação do usuário
    def setBlockVelocity(self):
        if self.widgets.block_initial_velocity_input.text == '':
            self.block_vel.x = 0    
        else:
            self.block_vel.x = float(self.widgets.block_initial_velocity_input.text)

    #? determina a massa do bloco de acordo com a informação do usuário
    def setBlockMass(self):
        if self.widgets.block_mass_input.text == '':
            self.block_mass = 0    
        else:
            self.block_mass = float(self.widgets.block_mass_input.text)
        self.block_weight = self.block_mass * self.gravity
    
    #? movimenta o bloco    
    def moveBlock(self):
        self.block_vel.x = self.block_vel.x + (self.aceleration * self.dt)
        self.block.pos.x = self.block.pos.x + (self.block_vel.x * self.dt)

    #? determina o tamanho da mola acordo com a informação do usuário
    def setSpringLength(self):
        if self.widgets.spring_length_input.text == '':
            self.initial_spring_lenght = 1
            self.spring.length = self.initial_spring_lenght    
        else:
            self.initial_spring_lenght = float(self.widgets.spring_length_input.text) 
            self.spring.length = self.initial_spring_lenght
        self.linkAxis()
    
    #? determina a constante elática da mola de acordo com a informação do usuário    
    def setSpringElasticConstant(self):
        if  self.widgets.spring_elastic_constant_input.text == '':
            self.k = 0  
        else:
            self.k = float(self.widgets.spring_length_input.text) 
                   
    #? determina o coeficiente de atrito dinamico de acordo com a informação do usuário
    def setDynamicFrictionCoefficient(self):
        if  self.widgets.dynamic_friction_coefficient_input.text == '':
            self.dynamic_friction_coefficient = 0  
        else:
            self.dynamic_friction_coefficient = float(self.widgets.dynamic_friction_coefficient_input.text)
            
    #? atualiza o tamanho da mola    
    def updateSpring(self):
        if self.is_block_repelled:
            if self.spring.length < self.initial_spring_lenght:
                self.update()
        else:    
            self.update()
    
    #? complemento da função anterior (updateSpring)
    def update(self):
        self.spring.length = self.spring.length + (self.block_vel.x * self.dt)
        self.linkAxis()
    
    #? move a cabeça da mola de acordo com o movimento da mesma    
    def linkAxis(self):       
        self.spring_head.pos.x = self.spring.pos.x + self.spring.axis.x
    
    #? checa se o bloco colidiu com a cabeça da mola
    def checkSpringColision(self):
        if self.block.pos.x <= self.spring_head.pos.x + (self.spring_head.size.x * .5) + (self.block.size.x * .5):
            return True
        return False
    
    #? verifica se a mola está comprimida ao maximo e tambem se há enercia cinetica no bloco
    def checkSpringLimit(self):
        if self.spring.length <= 1 and self.ce > 0:
            self.block_vel.x = 0
            self.aceleration = 0
            self.is_limit = True
    
    #? determina o ponto em que a mola irá empurrar o bloco        
    def checkSpringComportament(self):
        if self.block_vel.x > 0:
            self.is_block_repelled = True
    
    #? calcula a velocidade do bloco em contato com a mola    
    def calcBlockVelOnSpring(self):
        if not self.is_limit:
            self.force = -self.k * (self.initial_spring_lenght - self.spring.length) # Lei de Hooke; Força da mola
            self.aceleration = math.floor((self.force / self.block_mass)) * -1 # força / massa  # incremento para movimentação do bloco
    
    #? verifica se o bloco está em um ponto de atrito        
    def checkFrictionArea(self):
        if self.block.pos.x - (self.block.size.x * .5) > self.friction_ground.pos.x + (self.friction_ground.size.x * 0.5):
            return False
        
        if self.block.pos.x + (self.block.size.x * .5) < self.friction_ground.pos.x - (self.friction_ground.size.x * 0.5):
            return False
        
        return True

    #? calcula os 3 tipos de energia
    def calcEnergy(self):
        # Elatic Potential Energy        
        self.epe = (self.k * ((self.initial_spring_lenght - self.spring.length)**2))/2 
        # Cinectic Energy
        self.ce = (self.block_mass * (self.block_vel.x**2))/2
        # Mechanical Energy
        self.me = self.epe + self.ce
   
   #? aplica o atrito no bloco
    def applyFriction(self, current_ce, current_block_vel):
        self.friction_force = self.dynamic_friction_coefficient * self.block_weight
        self.friction_d = self.friction_d + (abs(self.block_vel.x) * self.dt)
        self.work = -self.friction_force * self.friction_d
        ce = self.ce + (self.work * self.dt)
        # self.block_vel.x = self.block_vel.x + sqrt((2 * ce)/ self.block_mass) * self.dt
        if not ce <= 0: self.block_vel.x = (ce * current_block_vel) / current_ce
        else:
            self.block_vel.x = 0
            
    #? atualiza as informações do bloco na tela
    def updateCalcInfo(self):        
        #? atualiza o a posição e o texto da aceleração
        self.block_vel_text.text = f"V: {self.block_vel.x:.0f} m/s"
        self.block_vel_text.pos.x = self.block.pos.x       
        #? atualiza o a posição e o texto da energia cinetica
        self.block_ce_text.text = f"EC: {self.ce:.0f} J"
        self.block_ce_text.pos.x = self.block.pos.x
        #? atualiza o texto da energia potencial elástica
        self.block_epe_text.text = f"EPE: {self.epe:.0f} J"
        #? atualiza o texto da energia mecanica
        self.block_me_text.text = f"ME: {self.me:.0f} J"
        
    #? loop central onde o código funciona se ultizando de quase todas as funções anteriores  
    def run(self):
        self.calcEnergy()
        while True:
            while self.is_running:
                rate(500)
                self.checkSpringLimit()
                self.checkSpringComportament()
                
                if self.checkSpringColision() or self.is_block_repelled:
                        self.updateSpring()
                        self.calcBlockVelOnSpring()
                        self.calcEnergy()

                if self.checkFrictionArea(): 
                    self.is_friction = True 
                    self.applyFriction(self.ce, self.block_vel.x)
                    self.calcEnergy()
                else:
                    self.is_friction = False
                    self.friction_d = 0
                
                self.updateCalcInfo()
                self.graphs.updateGraphs()
                self.moveBlock()
                self.t = self.t + self.dt
                
    #? pausa e retoma o funcionamento do código        
    def pause(self):
        if self.is_running:
            self.is_running = False
            self.widgets.pause_button.text = "Retomar"
        else:
            self.is_running = True
            self.widgets.pause_button.text = "Pausar"
    
    #? reseta todas as informações
    def reset(self):
        self.graphs.reset()
        self.block.pos.x = self.initial_block_pos.x
            
MainCore()