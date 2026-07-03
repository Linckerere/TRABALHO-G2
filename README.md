# 🐍 Python Crash

Um jogo inspirado no clássico **Snake**, desenvolvido em **Python** utilizando a biblioteca **Pygame**. O projeto foi criado com foco em aprendizado de programação, organização de código e implementação de mecânicas mais avançadas do que o jogo original.

## 📖 Sobre o projeto

O jogador controla uma cobra que deve coletar maçãs para aumentar sua pontuação enquanto evita:

* Colidir com as paredes;
* Colidir com o próprio corpo;
* Explodir ao tocar em bombas.

O jogo possui um sistema de fases com dificuldade dinâmica, efeitos sonoros, músicas diferentes para cada fase e interface gráfica personalizada.

---

## 🎮 Funcionalidades

* ✅ Sistema de fases (1 a 5)
* ✅ Dificuldade progressiva
* ✅ Velocidade variável conforme a fase
* ✅ Sistema de vidas
* ✅ Sistema de pontuação
* ✅ Bombas com tempo de vida
* ✅ Frutas com tempo para desaparecer
* ✅ HUD com Score, Vidas e Fase
* ✅ Textos flutuantes ao ganhar pontos
* ✅ Música diferente em cada fase
* ✅ Efeitos sonoros
* ✅ Sprites personalizados
* ✅ Fundo e paredes customizados
* ✅ Fallback automático caso imagens ou sons não sejam encontrados

---

## 🕹️ Controles

| Tecla  | Função              |
| ------ | ------------------- |
| W ou ↑ | Mover para cima     |
| S ou ↓ | Mover para baixo    |
| A ou ← | Mover para esquerda |
| D ou → | Mover para direita  |

Após o Game Over, pressione qualquer tecla de movimentação para reiniciar.

---

## 📈 Progressão

Cada fase aumenta a dificuldade do jogo modificando:

* velocidade da cobra (FPS);
* chance de surgimento de bombas;
* tempo de permanência dos itens na tela;
* música de fundo.

A progressão acontece ao atingir determinada pontuação ou quantidade de vidas conquistadas.

---

## ❤️ Sistema de vidas

O jogador inicia com **3 vidas**.

É possível ganhar vidas extras conforme acumula pontos, respeitando o limite máximo definido pelo jogo.

Ao perder uma vida:

* a cobra retorna ao centro;
* frutas e bombas são reiniciadas;
* a sequência de vidas conquistadas é zerada.

---

## 💣 Bombas

As bombas aparecem aleatoriamente durante a partida.

Ao tocar em uma bomba:

* o jogador perde uma vida;
* perde 100 pontos (sem ficar negativo);
* a cobra é reiniciada.

---

## 🍎 Frutas

Durante toda a partida existem até **3 frutas** simultaneamente.

Cada fruta:

* concede +10 pontos;
* possui tempo máximo de permanência na tela;
* desaparece automaticamente caso não seja coletada.

---

## 🎨 Recursos gráficos

O projeto utiliza sprites personalizados para:

* Cabeça da cobra
* Corpo da cobra
* Cobra morta
* Maçã
* Bomba
* Parede
* Fundo
* Tela de Game Over

Caso algum arquivo não exista, o jogo utiliza formas geométricas automaticamente.

---

## 🔊 Recursos de áudio

O jogo possui:

* música de fundo;
* música específica para cada fase;
* efeito sonoro ao comer frutas;
* efeito sonoro ao morrer.

Caso algum arquivo esteja ausente, o jogo continua funcionando normalmente.

---

## 📂 Estrutura do projeto

```text
Python-Crash/
│
├── Imagens/
│   ├── Fundo.png
│   ├── Parede.png
│   ├── Corpo.png
│   ├── bomba3.png
│   ├── Maçã.png
│   ├── 4.png
│   ├── snake_green_xx.png
│   └── gameover.png
│
├── Sons/
│   ├── Pixel adventures.mp3
│   ├── 8bit Bossa.mp3
│   ├── Orbital Colossus.mp3
│   ├── fight_looped.wav
│   ├── 2012_november_fakeAwake04 back to A minor.wav
│   ├── crunchybite.ogg
│   └── roblox-death-sound-effect.mp3
│
├── main.py
└── README.md
```

---

## 🛠️ Tecnologias utilizadas

* Python 3
* Pygame

---

## 📦 Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/Python-Crash.git
```

Entre na pasta:

```bash
cd Python-Crash
```

Instale o Pygame:

```bash
pip install pygame
```

Execute:

```bash
python main.py
```

---

## 👨‍💻 Desenvolvedores

* Pedro Henrique de Oliveira
* Arthur Lincke

---

## 🚀 Melhorias futuras

* Menu inicial
* Sistema de pause
* Ranking de pontuação
* Salvamento de recordes
* Mais tipos de frutas
* Novos obstáculos
* Power-ups
* Animações
* Efeitos de partículas
* Configurações de áudio
* Sistema de conquistas

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais e de aprendizado em programação utilizando Python e Pygame.
