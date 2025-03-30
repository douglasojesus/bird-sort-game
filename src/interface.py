import pygame
import sys
import threading  # NOVA IMPORTAÇÃO
import queue      # NOVA IMPORTAÇÃO
from pygame.locals import *
from src.functions import *
from src.algorithm import *
from copy import deepcopy

# Configurações de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
BUTTON_COLOR = (0, 128, 255)

# Cores dos pássaros
bird_colors = {
    1: (255, 0, 0),    # Vermelho
    2: (0, 255, 0),    # Verde
    3: (0, 0, 255),    # Azul
    4: (255, 165, 0),  # Laranja
    5: (128, 0, 128),  # Roxo
    6: (255, 192, 203),# Rosa
    7: (0, 255, 255),  # Ciano
    8: (255, 99, 71),  # Tomate
}

class BirdSortGame:
    def __init__(self, tabuleiro):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Bird Sort Puzzle")
        
        self.tabuleiro = tabuleiro
        
        # Configurações visuais
        self.branch_width = 100
        self.branch_height = 15
        self.bird_radius = 15
        self.branch_spacing = 80
        self.branch_x_left = 150
        self.branch_x_right = 550
        self.galho_y = 100
        
        # Estado do jogo
        self.selected_bird = None
        self.from_branch = None
        self.show_hint = False
        self.hint_move = None
        self.auto_solving = False       
        self.solution_moves = []         
        self.current_move = 0            
        self.temp_message = ""           
        self.temp_message_end = 0        
        self.solution_queue = queue.Queue()
        self.solving_thread = None        
        self.move_timer = 0               
        
        # Fontes
        self.font = pygame.font.SysFont('Arial', 20)
        self.big_font = pygame.font.SysFont('Arial', 30)
        
        # Botões
        self.hint_button = pygame.Rect(350, 500, 100, 40)
        self.solve_button = pygame.Rect(500, 500, 100, 40)
        
        self.update_visualization()

    
    def update_visualization(self):
        """Atualiza a representação visual baseada no estado do tabuleiro"""
        self.birds = {}
        
        for idx, (galho_name, passaros) in enumerate(self.tabuleiro.items()):
            self.birds[idx] = []
            
            if passaros == 'X':  # Galho quebrado
                continue
            
            branch_x = self.branch_x_left if idx % 2 == 0 else self.branch_x_right
            branch_y = self.galho_y + (idx // 2) * self.branch_spacing
            
            for j, bird_type in enumerate(passaros):
                if idx % 2 == 0:
                    x = branch_x + (j * (self.branch_width // 4)) + (self.branch_width // 8)
                else:
                    x = branch_x + ((3 - j) * (self.branch_width // 4)) + (self.branch_width // 8)
                
                y = branch_y - self.bird_radius
                color = bird_colors.get(bird_type, BLACK)
                self.birds[idx].append({"pos": (x, y), "color": color, "type": bird_type})

    def get_selectable_bird(self, branch_idx):
        """Retorna o pássaro que pode ser selecionado em um galho específico"""
        if branch_idx not in self.birds or not self.birds[branch_idx]:
            return None
        return self.birds[branch_idx][-1]
    
    def draw(self):
        """Desenha todos os elementos na tela"""
        self.screen.fill(WHITE)
        
        # Desenha galhos e pássaros
        for idx, (galho_name, passaros) in enumerate(self.tabuleiro.items()):
            branch_x = self.branch_x_left if idx % 2 == 0 else self.branch_x_right
            branch_y = self.galho_y + (idx // 2) * self.branch_spacing
            
            if passaros == 'X':
                pygame.draw.rect(self.screen, RED, (branch_x, branch_y, self.branch_width, self.branch_height), 2)
                text = self.font.render("QUEBRADO", True, RED)
            else:
                pygame.draw.rect(self.screen, BROWN, (branch_x, branch_y, self.branch_width, self.branch_height))
                pygame.draw.rect(self.screen, BLACK, (branch_x, branch_y, self.branch_width, self.branch_height), 2)
                text = self.font.render(galho_name, True, BLACK)
            
            self.screen.blit(text, (branch_x, branch_y - 25))
        
        for branch in self.birds.values():
            for bird in branch:
                pygame.draw.circle(self.screen, bird["color"], bird["pos"], self.bird_radius)
                pygame.draw.circle(self.screen, BLACK, bird["pos"], self.bird_radius, 1)
                text = self.font.render(str(bird["type"]), True, BLACK)
                text_rect = text.get_rect(center=bird["pos"])
                self.screen.blit(text, text_rect)
        
        if self.selected_bird:
            pygame.draw.circle(self.screen, self.selected_bird["color"], pygame.mouse.get_pos(), self.bird_radius, 3)
        
        # Botões 
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.hint_button)
        text = self.font.render("Dica", True, WHITE)
        self.screen.blit(text, (self.hint_button.x + 30, self.hint_button.y + 10))
        
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.solve_button)
        solve_text = self.font.render("Resolver", True, WHITE)
        self.screen.blit(solve_text, (self.solve_button.x + 15, self.solve_button.y + 10))
        
        # Dica
        if self.show_hint and self.hint_move:
            hint = self.hint_move
            text = self.big_font.render(f"{hint}", True, BLACK)
            self.screen.blit(text, (200, 450))
        
        # Mensagem de vitória
        if verifica_se_ganhou(self.tabuleiro):
            text = self.big_font.render("Parabéns! Você venceu!", True, GREEN)
            self.screen.blit(text, (250, 400))
        
        # Mensagem temporária
        if self.temp_message and pygame.time.get_ticks() < self.temp_message_end:
            text = self.big_font.render(self.temp_message, True, BLUE)
            self.screen.blit(text, (300, 400))
        
        pygame.display.flip()
    
    def get_hint(self):
        """Procura um movimento válido para sugerir ao jogador"""
        algoritmo = Algoritmo()
        hint = algoritmo.consegue_dica(tabuleiro=self.tabuleiro)
        self.hint_move = hint
    
    def run(self):
        """Loop principal do jogo"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            current_time = pygame.time.get_ticks()
            
            # Verifica resultados da thread
            if not self.solution_queue.empty():
                solucao = self.solution_queue.get()
                if solucao:
                    self.solution_moves = solucao
                    self.auto_solving = True
                    self.current_move = 0
                    self.move_timer = current_time
                else:
                    self.temp_message = "Sem solução!"
                    self.temp_message_end = current_time + 2000
                self.solving_thread = None
            
            # Execução dos movimentos
            if self.auto_solving:
                self.executar_movimento_auto()
            
            # Processamento de eventos
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                
                if event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if self.hint_button.collidepoint(mouse_pos):
                        self.show_hint = True
                        self.get_hint()
                        continue
                    
                    if self.solve_button.collidepoint(mouse_pos):
                        self.iniciar_resolucao()
                        continue
                    
                    if self.selected_bird is None:
                        for branch_idx in self.birds:
                            selectable_bird = self.get_selectable_bird(branch_idx)
                            if selectable_bird:
                                bx, by = selectable_bird["pos"]
                                if (bx - self.bird_radius <= mouse_pos[0] <= bx + self.bird_radius and
                                    by - self.bird_radius <= mouse_pos[1] <= by + self.bird_radius):
                                    self.selected_bird = selectable_bird
                                    self.from_branch = list(self.tabuleiro.keys())[branch_idx]
                                    break
                    else:
                        for branch_idx in range(len(self.tabuleiro)):
                            if self.is_click_on_branch(mouse_pos, branch_idx):
                                destino = list(self.tabuleiro.keys())[branch_idx]
                                if self.from_branch != destino:
                                    if realiza_voo_passaro(self.tabuleiro, self.from_branch, destino):
                                        self.show_hint = False
                                        self.update_visualization()
                                break

                        self.selected_bird = None
                        self.from_branch = None
            
            self.draw()
            clock.tick(60)
        
        pygame.quit()
    
    def is_click_on_branch(self, mouse_pos, branch_idx):
        """Verifica se o clique foi em um galho específico"""
        branch_x = self.branch_x_left if branch_idx % 2 == 0 else self.branch_x_right
        branch_y = self.galho_y + (branch_idx // 2) * self.branch_spacing
        return (branch_x <= mouse_pos[0] <= branch_x + self.branch_width and
                branch_y <= mouse_pos[1] <= branch_y + self.branch_height)

    
    def iniciar_resolucao(self):
        """Inicia o processo de solução em thread separada"""
        if not self.auto_solving and not self.solving_thread:
            self.temp_message = "Calculando solução..."
            self.temp_message_end = pygame.time.get_ticks() + 2000
            self.solving_thread = threading.Thread(target=self.executar_algoritmo)
            self.solving_thread.start()

    def executar_algoritmo(self):
        """Executa o algoritmo em background"""
        tabuleiro_copia = deepcopy(self.tabuleiro)
        solver = Algoritmo()
        solucao = solver.resolver_com_bfs(tabuleiro_copia) # Inserir qual dos algoritmos deseja que a interface use para resolver automaticamente (Algoritmos presentes na classe "Algoritmo" no arquivo "algorithm.py")
        self.solution_queue.put(solucao)

    def executar_movimento_auto(self):
        """Executa movimentos com timing controlado"""
        current_time = pygame.time.get_ticks()
        if current_time - self.move_timer > 800:  # 0.8s entre movimentos
            if self.current_move < len(self.solution_moves):
                origem, destino = self.solution_moves[self.current_move]
                if realiza_voo_passaro(self.tabuleiro, origem, destino):
                    self.update_visualization()
                    self.current_move += 1
                    self.move_timer = current_time
                else:
                    self.auto_solving = False
                    self.temp_message = "Erro na solução!"
                    self.temp_message_end = current_time + 2000
            else:
                self.auto_solving = False
                self.temp_message = "Solução completa!"
                self.temp_message_end = current_time + 2000

if __name__ == "__main__":
    game = BirdSortGame(qntd_galhos=4)
    game.run()