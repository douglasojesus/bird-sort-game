import random
import pygame

# Inicializa o Pygame
pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((400, 800))
pygame.display.set_caption("Bird Sort Example")

# Configurações dos galhos
total_branches = 3  # Número total de galhos
birds_per_branch = 4  # Número de pássaros por galho
branch_width = 150
branch_height = 15
bird_radius = 10
branch_spacing = 100  # Espaço vertical entre galhos
branch_x_left = 0  # Posição inicial dos galhos à esquerda
branch_x_right = 250  # Posição inicial dos galhos à direita
galho_y = 200  # Posição inicial vertical do primeiro galho

# Gerar pássaros em galhos
birds = {i: [] for i in range(total_branches)}

for i in range(total_branches):
    # Determina se o galho está na esquerda ou direita
    if i % 2 == 0:  # Galhos na esquerda
        branch_x = branch_x_left
    else:  # Galhos na direita
        branch_x = branch_x_right

    # Determina a linha (posição vertical) do galho
    row = i // 2
    branch_y = galho_y + (row * branch_spacing)

    # Adiciona os pássaros ao galho
    for j in range(birds_per_branch):
        x = branch_x + (j * (branch_width // birds_per_branch)) + (branch_width // (2 * birds_per_branch))
        y = branch_y - bird_radius  # Ajusta o Y para alinhar os pássaros sobre o galho
        color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)])  # Paleta de cores
        birds[i].append({"pos": (x, y), "color": color})

# Inicializa a variável de controle do loop
running = True

# Loop principal
while running:
    # Desenho
    screen.fill((255, 255, 255))  # Tela branca

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Desenha galhos
    for i in range(total_branches + 2):
        # Recalcula a posição de cada galho
        if i % 2 == 0:  # Galhos na esquerda
            branch_x = branch_x_left
        else:  # Galhos na direita
            branch_x = branch_x_right

        row = i // 2
        branch_y = galho_y + (row * branch_spacing)
        pygame.draw.rect(screen, (0, 0, 0), (branch_x, branch_y, branch_width, branch_height), 2)

    # Desenha pássaros
    for branch_birds in birds.values():
        for bird in branch_birds:
            pygame.draw.circle(screen, bird["color"], bird["pos"], bird_radius)

    # Atualiza a tela
    pygame.display.update()

# Encerra o Pygame
pygame.quit()
