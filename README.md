# Discord Bot Para Campeonatos 

Este bot para Discord é projetado para simplificar a gestão de torneios e fornecer suporte dentro de um servidor Discord. Ele oferece uma variedade de recursos, incluindo sistema de tickets, registro de equipes e criação automática de cargos e canais.

## Recursos

### 1. Sistema de Tickets
O bot permite que os usuários abram tickets para:
- **Suporte**: Esclareça quaisquer dúvidas com a equipe do servidor.
- **Parcerias**: Junte-se ao grupo de parceiros do servidor.
- **Registro**: Registre sua equipe para participar dos torneios.

Cada ticket é tratado em um canal privado acessível apenas pelo usuário e pela equipe do servidor.

### 2. Registro de Equipes
Os usuários podem registrar suas equipes para torneios através de uma interface simples. O bot:
- Verifica se o usuário já está registrado em uma equipe.
- Garante que há cargos disponíveis para a criação da equipe.
- Atribui um cargo ao usuário e cria um canal de texto e voz correspondente para a equipe.

### 3. Criação de Cargos e Canais
Os administradores podem automatizar a criação de até 16 cargos e canais para as equipes de torneio. O bot:
- Atribui cores a cada cargo.
- Cria canais de texto e voz dedicados para cada equipe com as permissões apropriadas.

### 4. Gestão de Permissões
O acesso a certos recursos do bot é restrito aos administradores do servidor, garantindo a gestão segura dos processos de torneio e suporte.

## Configuração

1. Instale as dependências necessárias:
   ```sh
   pip install discord.py
2. Configure seu token do bot e o ID do servidor no código. Edite o arquivo bot.py e adicione suas credenciais:
   ```sh
   import discord
   client = discord.Client()
   id_do_servidor = discord.Object(id=<SEU_ID_DO_SERVIDOR>)
   client.run('<SEU_TOKEN_DO_BOT>')
3. Execute o bot:
   ```sh
   python bot.py

## Uso

- Criar Tickets: Os usuários podem abrir tickets para suporte, parcerias ou registro de torneios através de uma interface simples.
- Registrar Equipes: Usuários com o cargo apropriado podem registrar sua equipe, incluindo a seleção de um nome para a equipe e a atribuição de membros.
- Comandos de Admin: Administradores podem criar cargos, canais e enviar várias mensagens automatizada para a sala de cada equipe.




