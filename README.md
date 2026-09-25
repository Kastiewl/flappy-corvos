# 🦅 Flappy Raven

Um remake estilizado em pixel art do clássico *Flappy Bird*, desenvolvido em **Python** utilizando **Pygame-CE** (*Community Edition*). O projeto conta com física vetorial com *Delta Time*, cenário dinâmico com *parallax* contínuo de múltiplas camadas, sistema de persistência de recordes em **SQLite**, múltiplos níveis de dificuldade e efeitos sonoros clássicos de 8-bit.

---

## 🎮 Demonstração & Visuais

**Menu do Jogo**

<img width="790" height="451" alt="image" src="https://github.com/user-attachments/assets/004d448b-aac4-4dab-8ae6-0029c0ba5f51" />




**Jogo Rodando**

<img width="794" height="446" alt="image" src="https://github.com/user-attachments/assets/e8e4145b-779b-4a36-aea5-ba0345defa13" />

---

## ✨ Funcionalidades Principais

* **Física Fluida e Consistente:** Movimentação, gravidade e colisões AABB calibradas com *Delta Time* ($dt$), garantindo a mesma taxa de resposta em monitores de qualquer taxa de atualização (60Hz, 144Hz, etc.).
* **Cenário Dinâmico em Parallax:** Fundo urbano multicamadas com rolagem horizontal infinita e velocidades independentes para profundidade visual.
* **Tipografia Pixel Art com Outline:** Renderização personalizada da fonte retro *Press Start 2P*, com contorno escuro (*stroke/outline*) para máxima legibilidade contra o cenário.
* **Seletor de Dificuldades:**
  * **Fácil:** Vão maior entre os canos e velocidade reduzida.
  * **Médio:** Ritmo e espaçamento balanceados.
  * **Difícil:** Menor vão vertical, velocidade acelerada e menor tempo de reação.
* **Placar de Líderes Local (Top 5):** Banco de dados **SQLite** integrado (`ranking.db`) para persistência automática das maiores pontuações.
* **Motor de Áudio Integrado:** Gerenciamento de canais via `pygame.mixer` com baixa latência para reprodução de efeitos sonoros de bater de asas, pontuação, navegação e colisão.
* **Pronto para Distribuição:** Configuração para compilação standalone (`.exe`) via **PyInstaller** sem dependência de terminal ou interpretador Python instalado.

---

## 🕹️ Controles

| Ação | Teclas |
| :--- | :--- |
| **Bater Asas / Pular** | `Barra de Espaço` |
| **Navegar nos Menus** | `Setas (Cima / Baixo)` ou `W` / `S` |
| **Confirmar Seleção** | `Enter` ou `Barra de Espaço` |
| **Voltar ao Menu / Pausar** | `ESC` |
| **Tentar Novamente (Game Over)** | `Barra de Espaço` |

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Motor / Biblioteca Gráfica:** [Pygame-CE](https://pyga.me/)
* **Banco de Dados:** SQLite3
* **Empacotamento:** PyInstaller

---

## 📂 Estrutura do Projeto

```text
flappy-bird/
├── audio/                      # Efeitos sonoros em formato PCM .wav
│   ├── die.wav
│   ├── hit.wav
│   ├── point.wav
│   ├── swoosh.wav
│   └── wing.wav
├── fonts/                      # Tipografia retro
│   └── PressStart2P-Regular.ttf
├── sprites/                    # Recursos visuais e camadas de pixel art
│   ├── background city/        # Camadas do parallax urbano
│   ├── bird/                   # Animações de voo do corvo
│   └── pipes/                  # Sprites dos obstáculos
├── src/                        # Código modular
│   ├── entities/               # Classes de entidades (Bird, Pipe)
│   ├── audio.py                # Gerenciador SoundManager
│   ├── config.py               # Constantes globais e balanceamento
│   ├── database.py             # Operações SQL e persistência do ranking
│   └── utils.py                # Funções utilitárias
├── main.py                     # Game loop e máquina de estados principal
├── ranking.db                  # Banco de dados de recordes (gerado em runtime)
├── requirements.txt            # Dependências do ecossistema Python
└── README.md
