import random
import pygame

# Mapeamento dos tipos de pássaros (números) para cores
bird_colors = {
    1: (255, 0, 0),        # Cor para pássaro 1 (vermelho)
    2: (0, 255, 0),        # Cor para pássaro 2 (verde)
    3: (0, 0, 255),        # Cor para pássaro 3 (azul)
    4: (255, 165, 0),      # Cor para pássaro 4 (laranja)
    5: (128, 0, 128),      # Cor para pássaro 5 (roxo)
    6: (255, 192, 203),    # Cor para pássaro 6 (rosa)
    7: (0, 255, 255),      # Cor para pássaro 7 (ciano)
    8: (255, 99, 71),      # Cor para pássaro 8 (tomate)
}

def startGame(galhos, tabuleiro):
    # Inicializa o Pygame
    pygame.init()

    # Configurações da tela
    screen = pygame.display.set_mode((400, 800))
    pygame.display.set_caption("Bird Sort Example")

    # Configurações dos galhos
    total_branches = galhos  # Número total de galhos
    total_branches_with_extra = total_branches + 2  # Total de galhos com os galhos extras
    birds_per_branch = 4  # Número de pássaros por galho
    branch_width = 150
    branch_height = 15
    bird_radius = 10
    branch_spacing = 100  # Espaço vertical entre galhos
    branch_x_left = 0  # Posição inicial dos galhos à esquerda
    branch_x_right = 250  # Posição inicial dos galhos à direita
    galho_y = 200  # Posição inicial vertical do primeiro galho

    # Inicializando a estrutura de pássaros
    birds = {i: [] for i in range(total_branches_with_extra)}  # Apenas para os galhos preenchidos

    # Preenche os galhos de acordo com o tabuleiro
    for idx, (branch_name, branch_birds) in enumerate(tabuleiro.items()):
        if idx < total_branches:  # Verifica se o galho está dentro dos limites
            # Determina se o galho está na esquerda ou direita
            if idx % 2 == 0:  # Galhos na esquerda
                branch_x = branch_x_left
            else:  # Galhos na direita
                branch_x = branch_x_right

            # Determina a linha (posição vertical) do galho
            row = idx // 2
            branch_y = galho_y + (row * branch_spacing)

            # Adiciona os pássaros ao galho com base no dicionário `tabuleiro`
            for j, bird_num in enumerate(branch_birds):
                x = branch_x + (j * (branch_width // birds_per_branch)) + (branch_width // (2 * birds_per_branch))
                y = branch_y - bird_radius  # Ajusta o Y para alinhar os pássaros sobre o galho
                color = bird_colors.get(bird_num, (0, 0, 0))  # Cor baseada no número do pássaro, ou preto como fallback
                birds[idx].append({"pos": (x, y), "color": color})

    # Função para verificar se o clique está dentro do pássaro
    def is_click_on_bird(mouse_pos, bird):
        bx, by = bird["pos"]
        return (bx - bird_radius <= mouse_pos[0] <= bx + bird_radius) and (by - bird_radius <= mouse_pos[1] <= by + bird_radius)

    # Inicializa a variável de controle do loop
    running = True
    selected_bird = None  # Nenhum pássaro selecionado inicialmente
    from_branch = None  # Galho de origem do pássaro

    # Loop principal
    while running:
        # Desenho
        screen.fill((255, 255, 255))  # Tela branca

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Se não há pássaro selecionado, tentamos selecionar um
                if selected_bird is None:
                    for i, branch_birds in birds.items():
                        if branch_birds:  # Só considera galhos com pássaros
                            if i % 2 == 0:  # Galho da esquerda
                                bird = branch_birds[-1]  # Pássaro mais à direita
                            else:  # Galho da direita
                                bird = branch_birds[0]  # Pássaro mais à esquerda

                            if is_click_on_bird(mouse_pos, bird):
                                selected_bird = bird
                                from_branch = i
                                print(f"Pássaro selecionado no galho {i}")
                                break
                else:
                    # Se há um pássaro selecionado, tentamos mover para o galho clicado
                    for i in range(total_branches_with_extra):
                        # Determina se o galho está na esquerda ou direita
                        if i % 2 == 0:  # Galhos na esquerda
                            branch_x = branch_x_left
                        else:  # Galhos na direita
                            branch_x = branch_x_right

                        row = i // 2
                        branch_y = galho_y + (row * branch_spacing)

                        # Verifica se o clique foi dentro de algum galho
                        if branch_x <= mouse_pos[0] <= branch_x + branch_width and branch_y <= mouse_pos[1] <= branch_y + branch_height:
                            # Adiciona o pássaro ao novo galho, removendo do galho original
                            if i != from_branch and len(birds[i]) < birds_per_branch:
                                # Recalcular a posição do pássaro no novo galho
                                if i % 2 == 0:  # Galho à esquerda
                                    new_x = branch_x + (len(birds[i]) * (branch_width // birds_per_branch)) + (branch_width // (2 * birds_per_branch))
                                    new_y = branch_y - bird_radius
                                    selected_bird["pos"] = (new_x, new_y)
                                    birds[i].append(selected_bird)  # Adiciona na posição mais à esquerda
                                else:  # Galho à direita
                                    new_x = branch_x + ((birds_per_branch - len(birds[i]) - 1) * (branch_width // birds_per_branch)) + (branch_width // (2 * birds_per_branch))
                                    new_y = branch_y - bird_radius
                                    selected_bird["pos"] = (new_x, new_y)
                                    birds[i].insert(0, selected_bird)  # Adiciona na posição mais à direita

                                birds[from_branch].remove(selected_bird)
                                selected_bird = None  # Limpa a seleção
                                from_branch = None
                                print(f"Pássaro movido para o galho {i}")
                            break

        # Desenha todos os galhos (incluindo os dois galhos extras, que ficam vazios)
        for i in range(total_branches_with_extra):
            if i % 2 == 0:  # Galhos na esquerda
                branch_x = branch_x_left
            else:  # Galhos na direita
                branch_x = branch_x_right

            row = i // 2
            branch_y = galho_y + (row * branch_spacing)
            pygame.draw.rect(screen, (0, 0, 0), (branch_x, branch_y, branch_width, branch_height), 2)

        # Desenha os pássaros apenas nos galhos preenchidos
        for branch_birds in birds.values():
            for bird in branch_birds:
                pygame.draw.circle(screen, bird["color"], bird["pos"], bird_radius)

        # Atualiza a tela
        pygame.display.update()

    # Encerra o Pygame
    pygame.quit()
