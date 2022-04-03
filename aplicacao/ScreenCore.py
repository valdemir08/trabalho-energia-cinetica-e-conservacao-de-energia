"""
   _____                             _____               
  / ____|                           / ____|              
 | (___   ___ _ __ ___  ___ _ __   | |     ___  _ __ ___ 
  \___ \ / __| '__/ _ \/ _ \ '_ \  | |    / _ \| '__/ _ \
  ____) | (__| | |  __/  __/ | | | | |___| (_) | | |  __/
 |_____/ \___|_|  \___|\___|_| |_|  \_____\___/|_|  \___|
                                                          v0.2
"""

from turtle import update
from vpython import *

class Widgets:
    def __init__(self, MainCore):
        self.mainCore = MainCore
       
        # vSpace() -> espaço na vertical
        # hSpace() -> espaço na horizontal
        Util.vSpace(1)

        # caixa de texto para a inserção da velocidade inicial do bloco
        self.block_initial_velocity_label = wtext(text = "Velocidade inicial (bloco):")
        Util.hSpace(2)
        self.block_initial_velocity_input = winput(bind = Util.nothing, type = "numeric", width = 100, _height = 20)
        Util.hSpace(3)

        # caixa de texto para a inserção da massa do bloco
        self.block_mass_label = wtext(text = "Massa (bloco):")
        Util.hSpace(2)
        self.block_mass_input = winput(bind = Util.nothing, type = "numeric", width = 100, _height = 20)
        Util.hSpace(3)

        # caixa de texto para a inserção dao comprimento da mola
        self.spring_length_label = wtext(text = "Comprimento (mola):")
        Util.hSpace(2)
        self.spring_length_input = winput(bind = Util.nothing, type = "numeric", width = 100, _height = 20)
        Util.vSpace(3)

        # caixa de texto para a inserção da constante elástica da mola
        self.spring_elastic_constant_label = wtext(text = "Constante elástica (mola):")
        Util.hSpace(2)
        self.spring_elastic_constant_input = winput(bind = Util.nothing, type = "numeric", width = 100, _height = 20)
        Util.hSpace(3)

        # caixa de texto para a inserção do coeficiente de atrito dinâmico
        self.dynamic_friction_coefficient_label = wtext(text = "Coeficiente de atrito dinâmico:")
        Util.hSpace(2)
        self.dynamic_friction_coefficient_input = winput(bind = Util.nothing, type = "numeric", width = 100, _height = 20)
        Util.hSpace(3)

        # botão de atualizar a animação de acordo com os dados informados pelo usuario
        self.update_button = button(bind = self.mainCore.getAllInfo, text = "Atualizar")
        Util.hSpace(3)

        # botão de iniciar a animação junto com os graficos
        self.run_button = button(bind = self.mainCore.run, text = "Executar")
        Util.hSpace(3)

        # botão para reiniciar todos os valores
        self.reset_button = button(bind = self.mainCore.pause, text = "Resetar")
        Util.vSpace(2)
        
        # slider do tamanho da area de atrito
        self.friction_ground_size_label = wtext(text = "Tamanho da area de atrito")
        Util.vSpace(2)
        self.friction_ground_size_slider = slider(bind = self.updateFrictionGroundSize, step = 1, min = 0, max = self.mainCore.friction_ground.size.x, length = self.mainCore.WIDTH)
        self.friction_ground_size_slider.value = self.mainCore.friction_ground.size.x * .25
        self.friction_ground_size_info = wtext(text = self.friction_ground_size_slider.value)
        Util.vSpace(2)
        
        # slider da posicao da area de atrito
        self.friction_ground_position_label = wtext(text = "Posição da area de atrito")
        Util.vSpace(2)
        self.friction_ground_position_slider = slider(bind = self.updateFrictionGroundPosition, step = .5, min = 0, max = self.mainCore.friction_ground.size.x, length = self.mainCore.WIDTH)
        self.friction_ground_position_slider.value = self.mainCore.friction_ground.pos.x * 1.25
        self.friction_ground_position_info = wtext(text = self.friction_ground_position_slider.value)
        Util.vSpace(2)
        
        self.epe_label = wtext(text = "Epe ")
        Util.hSpace(2)
        self.epe_info = wtext(text = f"{self.mainCore.epe:.2f}")
        Util.hSpace(4)
        
        self.ce_label = wtext(text = "Ce ")
        Util.hSpace(2)
        self.ce_info = wtext(text = f"{self.mainCore.ce:.2f}")
        Util.hSpace(4)
        
        self.me_label = wtext(text = "Me ")
        Util.hSpace(2)
        self.me_info = wtext(text = f"{self.mainCore.me:.2f}")
        Util.hSpace(4)
        
        self.block_vel_label = wtext(text = "Vel(block) ")
        Util.hSpace(2)
        self.block_vel_info = wtext(text = f"{self.mainCore.block_vel.x:.2f}")
        
        self.block_pos_x_label = wtext(text = "X(block) ")
        Util.hSpace(2)
        self.block_pos_x_info = wtext(text = f"{self.mainCore.block.pos.x}")
        Util.hSpace(2)
        
        self.block_head_pos_x_label = wtext(text = "X(block head) ")
        Util.hSpace(2)
        self.block_head_pos_x_info = wtext(text = f"{self.mainCore.block.pos.x}")
        Util.vSpace(3)
        
        self.block_aceleration_label = wtext(text = " Ace(block) ")
        Util.hSpace(2)
        self.block_aceleration_info = wtext(text = f"{self.mainCore.aceleration}")
        Util.vSpace(3)
        
        self.updateFrictionGroundSize()
                
    def updateFrictionGroundSize(self):
        self.friction_ground_size_info.text = self.friction_ground_size_slider.value
        self.mainCore.friction_ground.size.x = float(self.friction_ground_size_info.text)
        if self.friction_ground_size_slider.value <= 0:
            self.mainCore.friction_ground.visible = False
        else:
            self.mainCore.friction_ground.visible = True
            
        self.updateFrictionGroundPosition()
            
    def updateFrictionGroundPosition(self): 
        self.mainCore.friction_ground.pos.x = float(self.friction_ground_position_info.text)
        self.updateFrictionGroundPositionSliderInfo()
        
        if self.mainCore.friction_ground.pos.x < (self.mainCore.friction_ground.size.x * .5) + (self.mainCore.wall.size.x * .5):
            self.mainCore.friction_ground.pos.x = (self.mainCore.friction_ground.size.x * .5) + (self.mainCore.wall.size.x * .5)
            self.updateFrictionGroundPositionSliderInfo()
        
        if self.mainCore.friction_ground.pos.x > self.mainCore.ground.size.x - (self.mainCore.friction_ground.size.x * .5) + (self.mainCore.wall.size.x * .5):
            self.mainCore.friction_ground.pos.x = self.mainCore.ground.size.x - (self.mainCore.friction_ground.size.x * .5) + (self.mainCore.wall.size.x * .5)
            self.updateFrictionGroundPositionSliderInfo()
            
    def updateFrictionGroundPositionSliderInfo(self):
        self.friction_ground_position_info.text = self.friction_ground_position_slider.value
        
class Graphs:
    def __init__(self, WIDTH, mainCore):
        # grafico 1 | Energia mecânica
        self.graph1_config = graph(width = WIDTH, _height = 400, title = 'Energia mecânica / Tempo', xtitle = 'Tempo', ytitle = 'Energia mecânica', foreground = color.black, background = vector(0, 0.090196, 0.121569), fast = False)
        self.graph1 = gcurve(graph = self.graph1_config, color = color.white, width = 5)

        # grafico 2 | Energia cinética
        self.graph2_config = graph(width = WIDTH, _height = 400, title = 'Energia cinética / Tempo', xtitle = 'Tempo', ytitle = 'Energia cinética', foreground = color.black, background = vector(0.030392, 0.447059, 0.301961), fast = False)
        self.graph2 = gcurve(graph = self.graph2_config, color = color.white, width = 5)

        # grafico 3 | Energia potencial elástica
        self.graph3_config = graph(width = WIDTH, _height = 400, title = 'Energia elástica / Tempo', xtitle = 'Tempo', ytitle = 'Energia elástica', foreground = color.black, background = vector(0.784314, 0.188235, 0.329412), fast = False)
        self.graph3 = gcurve(graph = self.graph3_config, color = color.white, width = 5)

        # grafico 4 | velocidade
        self.graph4_config = graph(width = WIDTH, _height = 400, title = 'Velocidade / Tempo', xtitle = 'Tempo', ytitle = 'Velocidade', foreground = color.black, background = vector(0, 0.090196, 0.121569), fast = False)
        self.graph4 = gcurve(graph = self.graph4_config, color = color.white, width = 5)

        self.updateGraphs()

    def updateGraphs(self):
        self.graph1.plot(0, 0)
        self.graph2.plot(0, 0)
        self.graph3.plot(0, 0)
        self.graph4.plot(0, 0)

class Util:
    def vSpace(times):
        # espaço na vertical
        scene.append_to_caption(f'\n' * times)

    def hSpace(times):
        # espaço na horizontal
        scene.append_to_caption(f' ' * times)

    def reset(self):
        # reseta todos os valores
        pass

    def nothing(self):
        pass