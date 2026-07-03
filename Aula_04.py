##############################################################################
###                       P Y T H O N   C R A S H                          ###
##############################################################################
#### versão 1.0 Alpha (em desenvolvimento)                                 ###
##############################################################################
### By Pedro Henrique De Oliveira  (github.com/pdrho) e Arthur Lincke (github.com/Lickerere)
##############################################################################
import pygame
import sys
import random
import os

# =============================================================================
# BLOCO 1: INICIALIZAÇÃO E CONFIGURAÇÕES GERAIS
# Responsável por iniciar a engine, definir cores, tela e variáveis de estado.
# =============================================================================
pygame.init()
pygame.mixer.init()
pygame.font.init()

LARGURA_TELA = 800
ALTURA_TELA = 600
TITULO = "Python Crash - Aula 04: Configuração Dinâmica de Áudio e Efeitos Visuais"

COR_FUNDO_PADRAO = (30, 41, 59)
COR_CABECA = (34, 197, 94)
COR_CORPO = (22, 163, 74)
COR_MACA = (239, 68, 68)
COR_BOMBA = (244, 63, 94)
COR_TEXTO = (248, 250, 252)

VELOCIDADE_STROBO = 150
CORES_STROBO = [
    (239, 68, 68),  # Vermelho
    (34, 197, 94),  # Verde
    (59, 130, 246),  # Azul
    (234, 179, 8)  # Amarelo
]

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption(TITULO)
relogio = pygame.time.Clock()
fonte_game = pygame.font.SysFont("Fira Code", 24, bold=True)

score = 0
vidas = 3
fase_atual = 1
vidas_ganhas_consecutivas = 0
pontos_acumulados_proxima_vida = 0
textos_flutuantes = [] # Vai guardar listas no formato: [texto, x, y, tempo_de_vida]

tam_personagem = 30
velocidade_base = tam_personagem

pos_x = 0
pos_y = 0
dir_x = 0
dir_y = 0
corpo_cobra = []
cobra_viva = True

pode_mudar_direcao = True

# =============================================================================
# BLOCO 2: CONFIGURAÇÃO DINÂMICA DE FASES E DIFICULDADE
# Dicionário central que dita as regras, áudios e metas de cada nível.
# =============================================================================
CONFIG_FASES = {
    1: {"fps":  8, "chance_bomba": 0.15, "tempo_item": 6000, "musica": "Pixel adventures.mp3", "meta_vidas": 1, "meta_score": 50},
    2: {"fps":  9, "chance_bomba": 0.25, "tempo_item": 5000, "musica": "8bit Bossa.mp3", "meta_vidas": 2, "meta_score": 70},
    3: {"fps":  10, "chance_bomba": 0.35, "tempo_item": 4500, "musica": "2012_november_fakeAwake04 back to A minor.wav", "meta_vidas": 3, "meta_score": 90},
    4: {"fps":  11, "chance_bomba": 0.45, "tempo_item": 4000, "musica": "fight_looped.wav", "meta_vidas": 4, "meta_score": 110},
    5: {"fps": 12, "chance_bomba": 0.60, "tempo_item": 5000, "musica": "Orbital Colossus.mp3","meta_vidas": None, "meta_score": None}  # Fase final não possui metas de avanço
}

FASE_MAXIMA = max(CONFIG_FASES.keys()) # identifica qual é a "última" fase.

# =============================================================================
# BLOCO 3: CARREGAMENTO DE ASSETS (IMAGENS E SONS)
# Carrega arquivos de mídia com tratamento de erro (Fallback).
# =============================================================================
sprites = {}
usa_sprites = True
pasta_imagens = "Imagens"

arquivos_sprites = {
    "cabeca": "4.png",
    "morta": "snake_green_xx.png",
    "corpo": "Corpo.png",
    "maca_vermelha": "Maçã.png",
    "maca_verde": "Maçã.png",
    "bomba": "bomba3.png"
}

try:
    fundo_tile = pygame.image.load(
        os.path.join(pasta_imagens, "Fundo.png")
    ).convert()

    fundo_tile = pygame.transform.scale(
        fundo_tile,
        (tam_personagem, tam_personagem)
    )
except (FileNotFoundError, pygame.error):
    fundo_tile = None
    print("[Aviso] Fundo não encontrado. Será usado apenas preenchimento de cor.")
try:
    parede_tile = pygame.image.load(
        os.path.join(pasta_imagens, "Parede.png")
    ).convert_alpha()

    parede_tile = pygame.transform.scale(
        parede_tile,
        (tam_personagem, tam_personagem)
    )
except (FileNotFoundError, pygame.error):
    parede_tile = None
    print("[Aviso] Parede.png não encontrada.")
try:
    game_over_img = pygame.image.load(
        os.path.join(pasta_imagens, "gameover.png")
    ).convert_alpha()

    game_over_img = pygame.transform.scale(game_over_img, (500, 200))
except (FileNotFoundError, pygame.error):
    game_over_img = None
    print("[Aviso] gameover.png não encontrada.")

print("[INFO] Carregando recursos visuais...")

print("[INFO] Carregando recursos visuais...")
for chave, arquivo in arquivos_sprites.items():
    caminho = os.path.join(pasta_imagens, arquivo)
    try:
        img = pygame.image.load(caminho).convert_alpha()
        sprites[chave] = pygame.transform.scale(img, (tam_personagem, tam_personagem))
    except (FileNotFoundError, pygame.error):
        print(f"[Aviso] Falha ao carregar '{caminho}'. Fallback geométrico ativado para {chave}.")
        usa_sprites = False

pasta_sons = "Sons"

som_morte = None
try:
    caminho_som = os.path.join(pasta_sons, "roblox-death-sound-effect.mp3")
    som_morte = pygame.mixer.Sound(caminho_som)
    print("[INFO] Efeito sonoro 'roblox-death-sound-effect.mp3' carregado com sucesso!")
except (FileNotFoundError, pygame.error):
    print("[Aviso] Arquivo de som 'Sons/roblox-death-sound-effect.mp3' não encontrado. O jogo rodará em modo silencioso para mortes.")

som_mordida = None
try:
    caminho_mordida = os.path.join(pasta_sons, "crunchybite.ogg")
    som_mordida = pygame.mixer.Sound(caminho_mordida)
    print("[INFO] Efeito sonoro 'crunchybite.ogg' carregado com sucesso!")
except (FileNotFoundError, pygame.error):
    print("[Aviso] Arquivo de som 'Sons/crunchybite.ogg' não encontrado. Som de nutrição desativado.")

# =============================================================================
# BLOCO 4: MECÂNICAS DE JOGO (GERENCIAMENTO DE ITENS, ÁUDIO E COLISÕES)
# Funções que controlam as regras de negócio antes e durante a partida.
# =============================================================================
musica_atual_tocando = None

def gerenciar_musica_fase(fase):
    global musica_atual_tocando
    arquivo_fase = CONFIG_FASES[fase].get("musica")

    if arquivo_fase != musica_atual_tocando:
        musica_atual_tocando = arquivo_fase
        if arquivo_fase:
            caminho_musica = os.path.join(pasta_sons, arquivo_fase)
            try:
                pygame.mixer.music.load(caminho_musica)
                pygame.mixer.music.play(-1)
                print(f"[INFO] Música alterada para Fase {fase}: '{arquivo_fase}'")
            except (FileNotFoundError, pygame.error) as e:
                print(
                    f"[Aviso] Falha ao carregar música '{caminho_musica}'. O jogo continuará sem áudio de fundo para esta fase. ({e})")
        else:
            pygame.mixer.music.stop()


momento_geracao = 0
lista_frutas = []
lista_bombas = []


def gerar_posicao_aleatoria():
    colunas = LARGURA_TELA // tam_personagem
    linhas = ALTURA_TELA // tam_personagem

    while True:
        # Evita a primeira e a última coluna (paredes)
        x = random.randint(1, colunas - 2) * tam_personagem

        # Evita a primeira e a última linha (paredes)
        y = random.randint(1, linhas - 2) * tam_personagem

        # Não gera em cima da cobra
        if [x, y] not in corpo_cobra:
            return x, y


def spawnar_itens():
    global momento_geracao
    tempo_atual = pygame.time.get_ticks()
    chance_bomba = CONFIG_FASES[fase_atual]["chance_bomba"]

    # Mantém sempre 3 maçãs na tela
    while len(lista_frutas) < 3:
        pos = gerar_posicao_aleatoria()
        tipo = random.choice(["vermelha", "verde"])
        lista_frutas.append([pos, tipo, tempo_atual])

    # Coloca bombas baseado na chance, limitando a até 2 bombas simultâneas
    # Nova estrutura da bomba: [ [x, y], tempo_em_que_nasceu ]
    if random.random() < chance_bomba and len(lista_bombas) < 2:
        pos_b = gerar_posicao_aleatoria()
        lista_bombas.append([pos_b, tempo_atual])

def reiniciar_posicao_cobra():
    global pos_x, pos_y, dir_x, dir_y, corpo_cobra, cobra_viva
    pos_x = (LARGURA_TELA // 2) // tam_personagem * tam_personagem
    pos_y = (ALTURA_TELA // 2) // tam_personagem * tam_personagem
    dir_x = velocidade_base
    dir_y = 0
    corpo_cobra = [
        [pos_x, pos_y],
        [pos_x - tam_personagem, pos_y],
        [pos_x - (2 * tam_personagem), pos_y]
    ]
    cobra_viva = True


def aplicar_morte_por_colisao(motivo):
    global vidas, vidas_ganhas_consecutivas, pontos_acumulados_proxima_vida
    vidas -= 1
    vidas_ganhas_consecutivas = 0
    pontos_acumulados_proxima_vida = 0
    print(f"[MORTE] Motivo: {motivo} | Vidas restantes: {vidas}")
    if som_morte:
        som_morte.play()
    if vidas > 0:
        reiniciar_posicao_cobra()
        lista_frutas.clear()  # Limpa as frutas antigas ao morrer
        lista_bombas.clear()  # Limpa as bombas antigas ao morrer
        spawnar_itens()


def aplicar_morte_por_bomba():
    global score, vidas, vidas_ganhas_consecutivas, pontos_acumulados_proxima_vida
    vidas -= 1
    vidas_ganhas_consecutivas = 0
    score = max(0, score - 100)
    pontos_acumulados_proxima_vida = 0
    print(f"[EXPLOSÃO] Atingiu uma bomba! Vidas restantes: {vidas} | Score atual: {score}")
    if som_morte:
        som_morte.play()
    if vidas > 0:
        reiniciar_posicao_cobra()
        spawnar_itens()


# Setup Inicial antes do loop
reiniciar_posicao_cobra()
spawnar_itens()
pygame.mixer.music.load(
    os.path.join(pasta_sons, "pixelmaniax-neon-reverie-377201.mp3")
)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# =============================================================================
# BLOCO 5: O GAME LOOP (EVENTOS, ATUALIZAÇÃO E RENDERIZAÇÃO)
# O coração do jogo. Roda continuamente a cada frame atualizando a tela.
# =============================================================================
rodando = True
while rodando:
    tempo_atual = pygame.time.get_ticks()
    config_fase_atual = CONFIG_FASES[fase_atual]
    tempo_limite_item = config_fase_atual["tempo_item"]

    # --- 5.1: PROCESSAMENTO DE EVENTOS (Inputs do Usuário) ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        elif evento.type == pygame.KEYDOWN:  # <--- O teste de teclas começa AQUI
            if vidas <= 0:
                score = 0
                vidas = 3
                fase_atual = 1
                vidas_ganhas_consecutivas = 0
                pontos_acumulados_proxima_vida = 0
                reiniciar_posicao_cobra()
                spawnar_itens()
                continue

            if pode_mudar_direcao:
                if evento.key in [pygame.K_LEFT, pygame.K_a] and dir_x == 0:
                    dir_x = -velocidade_base
                    dir_y = 0
                    pode_mudar_direcao = False
                elif evento.key in [pygame.K_RIGHT, pygame.K_d] and dir_x == 0:
                    dir_x = velocidade_base
                    dir_y = 0
                    pode_mudar_direcao = False
                elif evento.key in [pygame.K_UP, pygame.K_w] and dir_y == 0:
                    dir_x = 0
                    dir_y = -velocidade_base
                    pode_mudar_direcao = False
                elif evento.key in [pygame.K_DOWN, pygame.K_s] and dir_y == 0:
                    dir_x = 0
                    dir_y = velocidade_base
                    pode_mudar_direcao = False




    # --- 5.2: LÓGICA DE ATUALIZAÇÃO DO JOGO (Física e Regras) ---
    if vidas > 0:
        # 1. Verificar e remover frutas que passaram do tempo limite
        frutas_validas = []
        for fruta in lista_frutas:
            tempo_nascimento = fruta[2]
            # Se a fruta ainda não expirou, ela continua no jogo
            if tempo_atual - tempo_nascimento < tempo_limite_item:
                frutas_validas.append(fruta)
        lista_frutas = frutas_validas

        # 2. Verificar e remover bombas que passaram do tempo limite
        bombas_validas = []
        for bomba in lista_bombas:
            tempo_nascimento = bomba[1]
            if tempo_atual - tempo_nascimento < tempo_limite_item:
                bombas_validas.append(bomba)
        lista_bombas = bombas_validas

        # 3. Chama o spawn para repor os itens que sumiram (ou criar novos se faltar)
        spawnar_itens()

        proximo_x = pos_x + dir_x
        proximo_y = pos_y + dir_y

        # Validação de Colisões
        if (
                proximo_x <= 0 or
                proximo_x >= LARGURA_TELA - tam_personagem or
                proximo_y <= 0 or
                proximo_y >= ALTURA_TELA - tam_personagem
        ):
            aplicar_morte_por_colisao("Colisão com a Parede")
            continue

        nova_cabeca = [proximo_x, proximo_y]

        if nova_cabeca in corpo_cobra:
            aplicar_morte_por_colisao("Auto-colisão com o Corpo")
            continue

        colidiu_com_bomba = False
        bomba_colidida = None  # <--- Nova variável para lembrar qual bomba foi atingida

        for bomba in lista_bombas:
            pos_bomba_atual = bomba[0]

            # Verifica se a cabeça bateu na bomba
            if nova_cabeca == list(pos_bomba_atual):
                colidiu_com_bomba = True
                bomba_colidida = bomba  # Guarda a bomba exata
                break

            # Verifica se alguma parte do corpo bateu na bomba
            for parte in corpo_cobra:
                if parte == list(pos_bomba_atual):
                    colidiu_com_bomba = True
                    bomba_colidida = bomba  # Guarda a bomba exata
                    break

            if colidiu_com_bomba:
                break

        if colidiu_com_bomba:
            lista_bombas.remove(bomba_colidida)  # <--- Remove a bomba explodida do jogo!
            aplicar_morte_por_bomba()
            continue

        pos_x = proximo_x
        pos_y = proximo_y
        corpo_cobra.insert(0, nova_cabeca)
        pode_mudar_direcao = True

        # Lógica de Nutrição e Dificuldade Dinâmica [MELHORIA APLICADA]
        # Nutrição com lista de frutas
        comeu_fruta = False
        fruta_comida = None

        for fruta in lista_frutas:
            posicao = fruta[0]
            if nova_cabeca == list(posicao):
                comeu_fruta = True
                fruta_comida = fruta
                break

        if comeu_fruta:
            lista_frutas.remove(fruta_comida)  # Tira a fruta que foi comida da tela

            if som_mordida:
                som_mordida.play()

            score += 10

            # Buscando a posição X e Y de dentro da estrutura da fruta que foi comida
            pos_x_fruta = fruta_comida[0][0]
            pos_y_fruta = fruta_comida[0][1]
            textos_flutuantes.append(["+10!", pos_x_fruta, pos_y_fruta, 30])

            if pontos_acumulados_proxima_vida >= 100:
                pontos_acumulados_proxima_vida -= 100
                if vidas < 6:
                    vidas += 1
                    vidas_ganhas_consecutivas += 1

            # Verifica as metas dinâmicas da fase atual para avançar
            if fase_atual < FASE_MAXIMA:
                meta_vidas_fase = CONFIG_FASES[fase_atual]["meta_vidas"]
                meta_score_fase = CONFIG_FASES[fase_atual]["meta_score"]

                if vidas_ganhas_consecutivas >= meta_vidas_fase or score >= meta_score_fase:
                    fase_atual += 1
                    vidas_ganhas_consecutivas = 0


            spawnar_itens()

        if not comeu_fruta:
            corpo_cobra.pop()

    # --- 5.3: RENDERIZAÇÃO GRÁFICA (Desenho na Tela) ---
    if fase_atual == FASE_MAXIMA and vidas > 0:
        indice_cor = (tempo_atual // VELOCIDADE_STROBO) % len(CORES_STROBO)
        cor_fundo_atual = CORES_STROBO[indice_cor]
    else:
        cor_fundo_atual = COR_FUNDO_PADRAO

    if fundo_tile:
        for x in range(0, LARGURA_TELA, tam_personagem):
            for y in range(0, ALTURA_TELA, tam_personagem):
                tela.blit(fundo_tile, (x, y))
    else:
        tela.fill(cor_fundo_atual)
    if parede_tile:
        # Parede superior e inferior
        for x in range(0, LARGURA_TELA, tam_personagem):
            tela.blit(parede_tile, (x, 0))
            tela.blit(parede_tile, (x, ALTURA_TELA - tam_personagem))

        # Parede esquerda e direita
        for y in range(tam_personagem, ALTURA_TELA - tam_personagem, tam_personagem):
            tela.blit(parede_tile, (0, y))
            tela.blit(parede_tile, (LARGURA_TELA - tam_personagem, y))

    for fruta in lista_frutas:
        pos_f = fruta[0]
        tipo_f = fruta[1]
        if usa_sprites:
            sprite_maca = sprites["maca_vermelha"] if tipo_f == "vermelha" else sprites["maca_verde"]
            tela.blit(sprite_maca, pos_f)
        else:
            pygame.draw.rect(tela, COR_MACA, (pos_f[0] + 5, pos_f[1] + 5, tam_personagem - 10, tam_personagem - 10))

        # --- Desenhando a lista de bombas ---
    for bomba in lista_bombas:
        pos_bomba_atual = bomba[0]  # Pega apenas o [x, y], ignorando o tempo de nascimento
        if usa_sprites:
            tela.blit(sprites["bomba"], pos_bomba_atual)
        else:
            pygame.draw.rect(tela, COR_BOMBA,
                             (pos_bomba_atual[0] + 5, pos_bomba_atual[1] + 5, tam_personagem - 10, tam_personagem - 10))

    for indice, parte in enumerate(corpo_cobra):
        if indice == 0:
            if usa_sprites:
                sprite_cabeca = sprites["cabeca"] if vidas > 0 else sprites["morta"]
                tela.blit(sprite_cabeca, (parte[0], parte[1]))
            else:
                cor_cabeca_atual = COR_CABECA if vidas > 0 else (127, 136, 140)
                pygame.draw.rect(tela, cor_cabeca_atual, (parte[0], parte[1], tam_personagem, tam_personagem))
        else:
            if usa_sprites:
                tela.blit(sprites["corpo"], (parte[0], parte[1]))
            else:
                pygame.draw.rect(tela, COR_CORPO, (parte[0] + 2, parte[1] + 2, tam_personagem - 4, tam_personagem - 4))


        # === DESENHANDO TEXTOS FLUTUANTES ===
    textos_vivos = []
    for txt in textos_flutuantes:
            texto_string = txt[0]
            txt_x = txt[1]
            txt_y = txt[2]
            tempo_vida = txt[3]

            if tempo_vida > 0:
                # Renderiza o texto verde
                sup_txt = fonte_game.render(texto_string, True, (134, 239, 172))
                tela.blit(sup_txt, (txt_x, txt_y))

                # Move o texto para cima e diminui o tempo de vida
                txt[2] -= 2
                txt[3] -= 1
                textos_vivos.append(txt)

    textos_flutuantes = textos_vivos  # Atualiza a lista só com os que não sumiram


    # Desenho do Placar
    texto_score = f"SCORE: {score}"
    texto_vidas = f"VIDAS: {vidas}"
    texto_fase = f"FASE: {fase_atual}" if fase_atual < 5 else "FASE: FINAL (5)"

    if vidas <= 0:
        if game_over_img:
            tela.blit(
                game_over_img,
                (
                    (LARGURA_TELA - game_over_img.get_width()) // 2,
                    (ALTURA_TELA - game_over_img.get_height()) // 2
                )
            )

    # ===== Painel HUD =====

    painel_x = LARGURA_TELA - 190
    painel_y = 10
    painel_largura = 180
    painel_altura = 95

    # Cria uma superfície transparente
    painel = pygame.Surface((painel_largura, painel_altura), pygame.SRCALPHA)

    # Fundo do painel (último número = transparência)
    pygame.draw.rect(
        painel,
        (25, 25, 35, 60),
        (0, 0, painel_largura, painel_altura),
        border_radius=10
    )

    # Coloca o painel na tela
    tela.blit(painel, (painel_x, painel_y))

    # Fundo transparente
    pygame.draw.rect(
        painel,
        (25, 25, 35, 120),
        (0, 0, painel_largura, painel_altura),
        border_radius=10
    )

    # Borda transparente
    pygame.draw.rect(
        painel,
        (255, 215, 0, 60),  # último número = transparência
        (0, 0, painel_largura, painel_altura),
        3,
        border_radius=10
    )

    # Desenha tudo de uma vez
    tela.blit(painel, (painel_x, painel_y))

    # Textos
    sup_score = fonte_game.render(f"⭐ Score: {score}", True, (255, 255, 255))
    sup_vidas = fonte_game.render(f"❤ Vidas: {vidas}", True, (255, 80, 80))
    sup_fase = fonte_game.render(f"⚡ Fase: {fase_atual}", True, (80, 220, 255))

    tela.blit(sup_score, (painel_x + 12, painel_y + 10))
    tela.blit(sup_vidas, (painel_x + 12, painel_y + 38))
    tela.blit(sup_fase, (painel_x + 12, painel_y + 66))

    pygame.display.flip()
    relogio.tick(config_fase_atual["fps"])

pygame.quit()
sys.exit()