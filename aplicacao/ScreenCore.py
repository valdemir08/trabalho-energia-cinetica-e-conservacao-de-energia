"""
   _____                             _____               
  / ____|                           / ____|              
 | (___   ___ _ __ ___  ___ _ __   | |     ___  _ __ ___ 
  \___ \ / __| '__/ _ \/ _ \ '_ \  | |    / _ \| '__/ _ \
  ____) | (__| | |  __/  __/ | | | | |___| (_) | | |  __/
 |_____/ \___|_|  \___|\___|_| |_|  \_____\___/|_|  \___|
                                                          v0.5.1
"""

from vpython import *
import math

class Widgets:
    #? metodo construtor
    def __init__(self, MainCore):
        self.mainCore = MainCore
       
        #? vSpace() -> espaço na vertical
        #? hSpace() -> espaço na horizontal
        
        Util.vSpace(1)

        #? caixa de texto para a inserção da velocidade inicial do bloco
        self.block_initial_velocity_label = wtext(text = "Velocidade inicial do bloco (m/s):")
        Util.hSpace(2)
        self.block_initial_velocity_input = winput(bind = Util.nothing, type = "numeric", width = 100, _height = 20)
        Util.hSpace(3)

        #? caixa de texto para a inserção da massa do bloco
        self.block_mass_label = wtext(text = "Massa do bloco (Kg):")
        Util.hSpace(2)
        self.block_mass_input = winput(bind = Util.nothing, type = "numeric", width = 100, _height = 20)
        Util.hSpace(3)

        #? caixa de texto para a inserção dao comprimento da mola
        self.spring_length_label = wtext(text = "Comprimento da mola (cm):")
        Util.hSpace(2)
        self.spring_length_input = winput(bind = Util.nothing, type = "numeric", width = 100, _height = 20)
        Util.vSpace(2)

        #? caixa de texto para a inserção da constante elástica da mola
        self.spring_elastic_constant_label = wtext(text = "Constante elástica da mola:")
        Util.hSpace(2)
        self.spring_elastic_constant_input = winput(bind = Util.nothing, type = "numeric", width = 100, _height = 20)
        Util.hSpace(3)

        #? caixa de texto para a inserção do coeficiente de atrito dinâmico
        self.dynamic_friction_coefficient_label = wtext(text = "Coeficiente de atrito dinâmico:")
        Util.hSpace(2)
        self.dynamic_friction_coefficient_input = winput(bind = Util.nothing, type = "numeric", width = 100, _height = 20)
        Util.vSpace(2)

        #? botão de atualizar a animação de acordo com os dados informados pelo usuario
        self.update_button = button(bind = self.mainCore.setAllInfo, text = "Capturar dados")
        Util.hSpace(3)

        #? botão de iniciar a animação junto com os graficos
        self.run_button = button(bind = self.mainCore.run, text = "Executar")
        Util.hSpace(3)

        #? botão para reiniciar todos os valores
        self.pause_button = button(bind = self.mainCore.pause, text = "Pausar")
        Util.hSpace(3)
         
        #? botão para reiniciar todos os valores
        self.reset_button = button(bind = self.mainCore.reset, text = "Resetar")
        Util.vSpace(2)
        
        #? slider do tamanho da area de atrito
        self.friction_ground_size_label = wtext(text = "Tamanho da area de atrito (cm)")
        Util.vSpace(2)
        self.friction_ground_size_slider = slider(bind = self.updateFrictionGroundSize, step = 1, min = 0, max = self.mainCore.friction_ground.size.x, length = self.mainCore.WIDTH)
        self.friction_ground_size_slider.value = self.mainCore.friction_ground.size.x * .05
        self.friction_ground_size_info = wtext(text = self.friction_ground_size_slider.value)
        Util.vSpace(2)
        
        #? slider da posicao da area de atrito
        self.friction_ground_position_label = wtext(text = "Posição da area de atrito (cm)")
        Util.vSpace(2)
        self.friction_ground_position_slider = slider(bind = self.updateFrictionGroundPosition, step = .5, min = 0, max = self.mainCore.friction_ground.size.x, length = self.mainCore.WIDTH)
        self.friction_ground_position_slider.value = self.mainCore.friction_ground.pos.x * 1.25
        self.friction_ground_position_info = wtext(text = self.friction_ground_position_slider.value)
        Util.vSpace(2)   
    
        #? atualiza o tamanho do chão de atrito de acordo com o valor inicial
        self.updateFrictionGroundSize()

    #? atualiza o tamanho do chão de atrito de acordo com o slider            
    def updateFrictionGroundSize(self):
        self.friction_ground_size_info.text = self.friction_ground_size_slider.value
        self.mainCore.friction_ground.size.x = float(self.friction_ground_size_info.text)
        
        #? caso o tamanho seja 0, desliga a visibilidade (necessário por causa de problemas da biblioteca)
        if self.friction_ground_size_slider.value <= 0:
            self.mainCore.friction_ground.visible = False
        else:
            self.mainCore.friction_ground.visible = True
            
        #? atualização a posição do chão de atrito para não ultrapassar o chão normal    
        self.updateFrictionGroundPosition()
    
    #? atualiza a posição do chão de atrito        
    def updateFrictionGroundPosition(self): 
        self.mainCore.friction_ground.pos.x = float(self.friction_ground_position_info.text)
        self.updateFrictionGroundPositionSliderInfo()
        
        #? regra para o chão de atrito não ultrapassar o chão normal
        if self.mainCore.friction_ground.pos.x < (self.mainCore.friction_ground.size.x * .5) + (self.mainCore.wall.size.x * .5):
            self.mainCore.friction_ground.pos.x = (self.mainCore.friction_ground.size.x * .5) + (self.mainCore.wall.size.x * .5)
            self.updateFrictionGroundPositionSliderInfo()
        
        if self.mainCore.friction_ground.pos.x > self.mainCore.ground.size.x - (self.mainCore.friction_ground.size.x * .5) + (self.mainCore.wall.size.x * .5):
            self.mainCore.friction_ground.pos.x = self.mainCore.ground.size.x - (self.mainCore.friction_ground.size.x * .5) + (self.mainCore.wall.size.x * .5)
            self.updateFrictionGroundPositionSliderInfo()
            
    #? atualiza a numeração ao lado do slider que atualiza a posição do chão de atrito        
    def updateFrictionGroundPositionSliderInfo(self):
        self.friction_ground_position_info.text = self.friction_ground_position_slider.value
class Graphs:
    #? metodo construtor
    def __init__(self, WIDTH, MainCore):
        self.mainCore = MainCore
        #? grafico 1 | Energia mecânica
        self.graph1_config = graph(width = WIDTH, _height = 400, title = 'Energia Mecânica(J) X Tempo(s)', xtitle = 'Tempo(s)', ytitle = 'Energia Mecânica(J)', foreground = color.black, background = color.white, fast = False)
        self.graph1 = gcurve(graph = self.graph1_config, color = color.blue, width = 5)

        #? grafico 2 | Energia Cinética e Potencial Elástica(J)
        self.graph2_config = graph(width = WIDTH, _height = 400, title = 'Energia Cinética(J) e Potencial Elástica(J) X Tempo(s)', xtitle = 'Tempo(s)', ytitle = 'Energia Cinética(J) e Potencial Elástica(J)', foreground = color.black, background = color.white, fast = False)
        self.graph2_ce = gcurve(graph = self.graph2_config, color = color.red, width = 5, label = "Energia Cinética(J)")
        self.graph2_epe = gcurve(graph = self.graph2_config, color = color.black, width = 5, label = "Energia Potencial Elástica(J)")

        #? grafico 3 | velocidade
        self.graph3_config = graph(width = WIDTH, _height = 400, title = 'Velocidade(m/s) X Tempo(s)', xtitle = 'Tempo(s)', ytitle = 'Velocidade(m/s)', foreground = color.black, background = color.white, fast = False)
        self.graph3 = gcurve(graph = self.graph3_config, color = color.green, width = 5)

        self.update()

    #? função para atualizar os gráficos
    def update(self):
        self.graph1.plot(self.mainCore.t, self.mainCore.me)
        self.graph2_ce.plot(self.mainCore.t, self.mainCore.ce)
        self.graph2_epe.plot(self.mainCore.t, self.mainCore.epe)
        self.graph3.plot(self.mainCore.t, self.mainCore.block_vel.x)
    
    #? função para resetar os gráficos    
    def reset(self):
        self.graph1.delete()
        self.graph2_ce.delete()
        self.graph2_epe.delete()
        self.graph3.delete()

class Util:
    #? espaço na vertical
    def vSpace(times):
        scene.append_to_caption(f'\n' * times)

    #? espaço na horizontal
    def hSpace(times):
        scene.append_to_caption(f' ' * times)

    #? reseta todos os valores
    def reset(self):
        pass

    #? literalmente nada
    def nothing(self):
        pass