import random
import pygame

# Inicializa o Pygame
pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((400, 800))
pygame.display.set_caption("Bird Sort Example")

# Configurações dos galhos
galho_width = 50
galho_height = 15
galho_positions = [150, 350, 550]  # X-coordenadas das torres
galho_y = 200  # Posição vertical das torres

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
COLORS = [RED, BLUE, (0, 255, 0), (255, 255, 0)]  # Paleta de cores dos pássaros

# Variáveis configuráveis
num_branches = 4  # Número de galhos por lado
birds_per_branch = 4  # Número de pássaros por galho
branch_width = 150
branch_height = 15
bird_radius = 10
branch_spacing = 20  # Espaço entre galhos
branch_x_left = 0  # Posição inicial dos galhos à esquerda
branch_x_right = 250  # Posição inicial dos galhos à direita
branch_positions_left = [branch_x_left for _ in range(num_branches)]
branch_positions_right = [branch_x_right for _ in range(num_branches)]
branch_positions = branch_positions_left + branch_positions_right

# Gerar pássaros em galhos
birds = {i: [] for i in range(num_branches * 2)}
print(birds)
print(birds_per_branch)
count = 0
for i in range(num_branches * 2):
    row = i % num_branches  # Determina a linha (posição vertical) do galho
    for j in range(birds_per_branch):
        if i < num_branches:  # Galhos à esquerda
            x = branch_positions_left[i] + (j * (branch_width // birds_per_branch)) + (branch_width // (2 * birds_per_branch))
            y = galho_y + (row * 100) - bird_radius  # Calcula a posição vertical
            print("Esquerdaaa")
        else:  # Galhos à direita
            x = branch_positions_right[i - num_branches] + (j * (branch_width // birds_per_branch)) + (branch_width // (2 * birds_per_branch))
            y = galho_y + (row * 100) - bird_radius  # Calcula a posição vertical
            print("Direitaaa")

        color = random.choice(COLORS)
        birds[i].append({"pos": (x, y), "color": color})

        
print(birds)
print(birds_per_branch)

# Inicializa a variável de controle do loop
running = True

# Loop principal
while running:
    # Desenho
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Desenha galhos
    count = 0
    for i, branch_x in enumerate(branch_positions):
        pygame.draw.rect(screen, BLACK, (branch_x, galho_y + count * 100, branch_width, branch_height), 2)
        count += 1
        if count == num_branches:
            count = 0
        
        
    
    # Desenha pássaros
    for branch_birds in birds.values():
        for bird in branch_birds:
            pygame.draw.circle(screen, bird["color"], bird["pos"], bird_radius)
    
    # Atualiza a tela
    pygame.display.update()

# Encerra o Pygame
pygame.quit()
