# 🤖 Discord Advanced Macro

Uma ferramenta poderosa, visual e intuitiva desenvolvida em Python para automatizar sequências de cliques na tela de forma inteligente. Criada originalmente para interagir com o Discord (como automatizar tarefas repetitivas, trocar canais, mutar), mas totalmente funcional para **qualquer tipo de automação no seu computador**.

---

## ✨ Funcionalidades

- **⚙️ Sequências Dinâmicas:** Adicione e remova quantos passos de cliques quiser em sua sequência macro.
- **🎯 Gravação Automática:** Simplesmente clique em "Gravar" e o programa salva a posição do seu mouse após 4 segundos.
- **📝 Personalização de Passos:** Nomeie cada passo livremente (ex: *"Abrir canal de voz"*, *"Mutar microfone"*) para saber exatamente o que o robô está fazendo.
- **⏳ Delays Individuais:** Estipule o tempo exato (em segundos ou milissegundos) que o robô deve esperar antes de realizar a próxima ação.
- **👥 Múltiplos Perfis (Hotkeys):** Mantenha diferentes fluxos automatizados prontos engatilhados. Pressione a `Seta para Baixo` para rodar o Perfil 1, ou `Seta para Cima` para o Perfil 2.
- **🎨 Interface Moderna:** Aplicativo desenhado usando *Dark Theme* com paletas visuais responsivas muito semelhantes ao próprio Discord, focado na melhor experiência de usuário.

---

## 🚀 Como Usar no seu Computador

### 1. Pré-requisitos
Certifique-se de ter o [Python](https://www.python.org/downloads/) instalado na sua máquina.

Você vai precisar instalar as seguintes bibliotecas de dependência para que o programa consiga controlar seu mouse e teclado de forma autônoma:
```bash
pip install pyautogui keyboard
```

### 2. Rodando o Programa
Navegue até a pasta do projeto e execute:
```bash
python entra-sai-discord.py
```

### 3. Configurando a sua Primeira Automação
1. Com a janela aberta, clique em **"Configurar Perfil 1"**.
2. Clique no botão verde de **"Adicionar Nova Ação"**.
3. Dê um nome para a sua ação (Ex: *Clicar no chat*).
4. Clique em **"Gravar"**. Você terá 4 segundos para posicionar o seu mouse EXATAMENTE onde você quer que o programa clique. Mantenha o mouse parado lá até a notificação sumir.
5. Defina o tempo de "Espera" após aquele clique.
6. Volte e ligue a automação pressionando o atalho referente ao seu Perfil (`Seta p/ Baixo` para o Perfil 1).

---

## 🔒 Privacidade e Segurança
O projeto está configurado para **NÃO** versionar (ignorar) dados da sua tela. O arquivo `.gitignore` bloqueia as suas posições (`posicoes_advanced.json`) para que elas nunca sejam publicadas por acidente no GitHub e fiquem apenas no seu PC.

## 🤝 Créditos
Feito com dedicação para agilizar fluxos repetitivos e melhorar o engajamento através da tecnologia! Fique à vontade para fazer um *Fork* e contribuir com o projeto!
