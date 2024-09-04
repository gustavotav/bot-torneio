import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord import app_commands
from discord import Game, Streaming, Activity, ActivityType
from discord.ui import Button, View
from discord.ui import Select, View
from datetime import datetime, time, timedelta    
import asyncio
import json
import random
import os
import copy


id_do_servidor = discord.Object(id=) # Coloque o id de seu servidor

class MeuClient(discord.Client):
    def __init__(self, *, intents: discord.Intents, application_id=None):
        super().__init__(intents=intents, application_id=application_id)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=id_do_servidor)
        self.add_view(Ticket())
        self.add_view(Inscrição())
        await self.tree.sync()


client = MeuClient(intents=discord.Intents.all())
intents = discord.Intents.default()
intents.message_content = True
intents.members = True


###############################
# EMBED
###############################

embedTicket= discord.Embed(
    title="CENTRAL TICKET - ZERO CUP",
    description="Escolha alguma categoria de ticket abaixo.\n\n<:4_:1230214181102551080>  **SUPORTE** Se precisar esclarecer alguma dúvida com a equipe.\n\n<:3_:1230214182671089776> **PARCERIA** Se tem interesse em ingressar no grupo de parceiros do servidor. \n\n<:2_:1230214184277377087> **INSCRIÇÃO** A inscrição é necessária para que você e sua equipe participe dos torneios que ocorrerão.",
    colour=0x0000FF
)

embedTicket.set_footer(text="ZERO CUP © Todos os direitos reservados.")
embedTicket.set_thumbnail(url="https://media.discordapp.net/attachments/1229939011393552459/1230212630107394229/2c5a9b696005b7ec35b80983bbace788.jpg?ex=66327fcb&is=66200acb&hm=c47e4807ef56382b8ef2e6c4e1377d7dea74518cfe42fe9b3dce59be39c68037&=&format=webp&width=617&height=617")

embedInscrição= discord.Embed(
    title="CENTRAL INSCRIÇÃO - ZERO CUP",
    description="## <:2_:1230214184277377087> Para realizar a inscrição clique no botão abaixo \nA inscrição é necessária para que você e sua equipe **participe dos torneios** que ocorrerão. Certifique-se de ter **efetuado o pagamento** antes de se inscrever.",
    colour=0x0000FF
)

embedInscrição.set_footer(text="ZERO CUP © Todos os direitos reservados.")
embedInscrição.set_thumbnail(url="https://media.discordapp.net/attachments/1229939011393552459/1230212630107394229/2c5a9b696005b7ec35b80983bbace788.jpg?ex=66327fcb&is=66200acb&hm=c47e4807ef56382b8ef2e6c4e1377d7dea74518cfe42fe9b3dce59be39c68037&=&format=webp&width=617&height=617")

embedregistro= discord.Embed(
    title="CENTRAL REGISTRO - ZERO CUP",
    description="## <:2_:1230214184277377087> Para realizar a inscrição mencione os usuários da sua equipe nesse canal! \nÉ necessário que você mencione até **7 usuários** para que participem de sua equipe.\n Lembre-se de **apenas mencionar**.",
    colour=0x0000FF
)

embedregistro.set_footer(text="ZERO CUP © Todos os direitos reservados.")
embedregistro.set_thumbnail(url="https://media.discordapp.net/attachments/1229939011393552459/1230212630107394229/2c5a9b696005b7ec35b80983bbace788.jpg?ex=66327fcb&is=66200acb&hm=c47e4807ef56382b8ef2e6c4e1377d7dea74518cfe42fe9b3dce59be39c68037&=&format=webp&width=617&height=617")

###############################
# COMANDOS
###############################
class ModalEmbed(discord.ui.Modal, title="Criar Embed"):        
        Titulo = discord.ui.TextInput(
            label="Titulo",
            style=discord.TextStyle.short,
            placeholder="Coloque o titulo da embed"
        )

        Texto = discord.ui.TextInput(
            label="Texto",
            style=discord.TextStyle.long,
            placeholder="Digite o texto da embed"
        )

        Imagem = discord.ui.TextInput(
            label="Link de uma imagem (opcional)",
            style=discord.TextStyle.long,
            required=False,
            placeholder="Digite o link da imagem"
        )

        async def on_submit(self, interaction: discord.Interaction):
         titulo = self.Titulo.value
         texto = self.Texto.value
         imagem = self.Imagem.value

         embed = discord.Embed(
            title=titulo,
            description=texto,
            color=discord.Color.gold()  # Cor da embed, você pode alterar conforme necessário
         )
        
         if imagem:
             embed.set_image(url=imagem)

         channel = interaction.channel
         await channel.send(embed=embed)
         await interaction.response.send_message("Embed enviada ``:)``", ephemeral=True)


class ModalInscrição(discord.ui.Modal, title="Registrar Equipe"):
    Equipe = discord.ui.TextInput(
        label="Nome da equipe",
        style=discord.TextStyle.short,
        placeholder="Digite o nome da sua equipe"
    )

    async def on_submit(self, interaction: discord.Interaction):
        equipe_nome = self.Equipe.value  # Obtém o nome da equipe enviado pelo usuário
        member = interaction.user

        # Carrega os registros de registros.json como um dicionário
        try:
            with open('registros.json', 'r') as file:
                registros = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            registros = {}

        # Carrega os registros de permitidos.json como um dicionário
        try:
            with open('permitidos.json', 'r') as file:
                permitidos = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            permitidos = {}

        # Verifica se o usuário já está registrado em alguma equipe
        if str(member.id) in permitidos:
            await interaction.response.send_message("Erro: Você já está registrado em uma equipe.", ephemeral=True)
            return

        guild = interaction.guild

        # Verifica se há equipes disponíveis
        if not registros:
            await interaction.response.send_message("Erro: Não há equipes disponíveis para registro no momento.", ephemeral=True)
            return

        # Itera sobre os registros para encontrar um cargo disponível
        cargo_disponivel = None
        for equipe_nome_key, equipe_info in registros.items():
            cargo_id = equipe_info['cargo_id']
            role = guild.get_role(cargo_id)
            if role and role.members == []:
                cargo_disponivel = cargo_id
                # Remove a equipe do arquivo registros.json
                del registros[equipe_nome_key]
                with open('registros.json', 'w') as file:
                    json.dump(registros, file)
                break

        # Verifica se foi encontrado um cargo disponível
        if cargo_disponivel is None:
            await interaction.response.send_message("Erro: Todos os cargos de equipes estão em uso.", ephemeral=True)
            return

        # Adiciona o cargo ao usuário
        role = guild.get_role(cargo_disponivel)
        if not role:
            await interaction.response.send_message("Erro: O cargo da equipe não foi encontrado.", ephemeral=True)
            return
        try:
            await member.add_roles(role)
        except discord.Forbidden:
            await interaction.response.send_message("Erro: O bot não tem permissão para adicionar cargos aos usuários.", ephemeral=True)
            return

        # Renomeia o cargo para o nome da equipe fornecido pelo usuário
        try:
            await role.edit(name=equipe_nome)
        except discord.Forbidden:
            await interaction.response.send_message("Erro: O bot não tem permissão para editar o nome do cargo.", ephemeral=True)
            return
        

        # Adiciona o usuário e o cargo aos registros
        permitidos[str(member.id)] = {'cargo_id': cargo_disponivel}

        # Escreve os registros de volta no arquivo JSON
        with open('permitidos.json', 'w') as file:
            json.dump(permitidos, file)


        # Responde ao usuário
        await interaction.response.send_message(f"A equipe {equipe_nome} foi registrada com sucesso! Adicione os membros da sua equipe os mencionando em: https://discord.com/channels/1224826485047558244/1228093048601182308", ephemeral=True)


###############################
# VIEWS
###############################

class Inscrição(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None

    @discord.ui.button(label="Realizar Inscrição", style=discord.ButtonStyle.gray, emoji="<a:1_:1230214151737970853>", disabled=False, custom_id="persistent_view:botaoinscrição")
    async def botao8(self, interaction: discord.Interaction, button: discord.ui.Button):
        author = interaction.user
        member = interaction.guild.get_member(author.id)
        allowed_role_id = 1206479728735944804  # ID do cargo permitido a registrar uma equipe

        if allowed_role_id in [role.id for role in member.roles]:
            await interaction.response.send_modal(ModalInscrição())
        else:
            await interaction.response.send_message("Você não tem permissão para acessar este modal.", ephemeral=True)

class ViewTicketclosed(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None


    @discord.ui.button(label="Finalizar Ticket", style=discord.ButtonStyle.red, emoji="<:cadeado:1169469654880768040>", disabled=False, custom_id="persistent_view:botaofinalizarticket")
    async def botao8(self, interaction: discord.Interaction, button: discord.ui.Button):
    # Obter o canal atual
     canal = interaction.channel

    # Obter a lista de membros no canal
     membros = canal.members

    # Obter a lista de cargos que têm permissões para o canal
     roles_com_permissoes = [role for role in canal.guild.roles if canal.permissions_for(role).read_messages or canal.permissions_for(role).send_messages]

    # Iterar sobre os membros e negar permissões se não tiverem cargos com permissões
     for membro in membros:
        membros_roles = [role.id for role in membro.roles]
        if not any(role.id in membros_roles for role in roles_com_permissoes):
            overwrite = discord.PermissionOverwrite(read_messages=False, send_messages=False)
            await canal.set_permissions(membro, overwrite=overwrite)

    # Alterar o nome do canal para indicar que está fechado
     await canal.edit(name="⛔・ticket・fechado")

    # Enviar uma mensagem indicando que o ticket foi fechado
     await interaction.response.send_message(f"***Este ticket foi fechado por*** {interaction.user.mention}.", view=ViewTicketdelete())

class ViewTicketdelete(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None

    @discord.ui.button(label="Deletar Ticket", style=discord.ButtonStyle.red, emoji="<:Lixeira:1169471378349641799>", disabled=False, custom_id="persistent_view:botaodeletarticket")
    async def botao5(self, interaction: discord.Interaction, button: discord.ui.Button): 


        # Delete the channel
        await interaction.channel.delete()


class Ticket(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.timeout = None
        self.add_item(Menu())

class Menu(discord.ui.Select):
    def __init__(self):
        self.opened_tickets = {}
        self.category_mapping = {
            "Suporte": 000000000000000000, # Coloque id da categoria na qual quer que o ticket seja aberto
            "Parceria": 000000000000000000, # Coloque id da categoria na qual quer que o ticket seja aberto
            "Inscrição": 000000000000000000 # Coloque id da categoria na qual quer que o ticket seja aberto
        }
        options = [
            discord.SelectOption(value="Suporte", label="Suporte", emoji="<:4_:1230214181102551080>"),
            discord.SelectOption(value="Parceria", label="Parceria", emoji="<:3_:1230214182671089776>"),
            discord.SelectOption(value="Inscrição", label="Inscrição", emoji="<:2_:1230214184277377087>"),
        ]
        super().__init__(
            placeholder="Selecione uma opção...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:menu"
        )

    async def callback(self, interaction: discord.Interaction):
        selected_value = self.values[0]
        user = interaction.user
        guild = interaction.guild

        user_id = str(interaction.user.id)
        guild_id = str(guild.id)

        # Verificar se o usuário já abriu um ticket neste servidor
        if guild_id in self.opened_tickets and user_id in self.opened_tickets[guild_id]:
            # Verificar se o canal anterior ainda existe
            last_channel_id = self.opened_tickets[guild_id][user_id]
            last_channel = discord.utils.get(guild.channels, id=int(last_channel_id))
            if last_channel:
                await interaction.response.send_message("Você já possui um ticket aberto neste servidor.", ephemeral=True)
                return

        channel_name = f"👥・Ticket・{interaction.user.name}"

        # Obter a categoria
        category_id = self.category_mapping.get(selected_value)
        if category_id is None:
            await interaction.response.send_message(f"A categoria para {selected_value} não foi encontrada.", ephemeral=True)
            return

        category = discord.utils.get(guild.categories, id=category_id)
        if category is None:
            await interaction.response.send_message(f"A categoria com ID {category_id} não foi encontrada.", ephemeral=True)
            return

        # Criar o canal na categoria
        new_channel = await guild.create_text_channel(channel_name, category=category)

        # Configurar permissões
        role_id = 1210828430661128223  # ID do cargo com permissões de acesso ao canal
        role = discord.utils.get(guild.roles, id=role_id)
        if role is None:
            await interaction.response.send_message(f"O cargo com ID {role_id} não foi encontrado.", ephemeral=True)
            return
        
        # Adicionar permissões ao canal
        await new_channel.set_permissions(role, read_messages=True, send_messages=True)
        await new_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await new_channel.set_permissions(guild.default_role, read_messages=False, send_messages=False)

        await interaction.response.send_message(content=f"Seu ticket foi criado: {new_channel.mention}", ephemeral=True)

        # Criar mensagem inicial
        embedticket2 = discord.Embed(
            title="⛑️ TICKET ⛑️",
            description=f"Bem-vindo ao seu ticket {selected_value.lower()}\n\nDescreva abaixo algo para agilizarmos o seu ticket.\nAgradecemos pelo seu contato, lembre-se os tickets são privados e apenas responsáveis conseguem ver o ticket.",
            colour=0x0000FF
        )
        embedticket2.set_footer(text="ZERO CUP © Todos os direitos reservados.")

        await new_channel.send(interaction.user.mention, embed=embedticket2, view=ViewTicketclosed())

        # Registrar o ticket aberto
        if guild_id not in self.opened_tickets:
            self.opened_tickets[guild_id] = {}
        self.opened_tickets[guild_id][user_id] = str(new_channel.id)


@client.tree.command(
    description="Envie uma embed nesse canal"
)
@commands.has_permissions(administrator=True)
async def say(interaction: discord.Interaction):
 if interaction.user.guild_permissions.administrator:   
    await interaction.response.send_modal(ModalEmbed())
 else:
        # Código para quando o usuário NÃO tem permissão de administrador
        await interaction.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)


@client.tree.command(
        description="Envie o painel de ticket."
)
@commands.has_permissions(administrator=True)
async def painel_ticket(interaction: discord.Interaction):
 if interaction.user.guild_permissions.administrator:    
    
  await interaction.response.send_message(embed=embedTicket, view=Ticket())

 else:
        # Código para quando o usuário NÃO tem permissão de administrador
        await interaction.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)


@client.tree.command(
        description="Envie o painel de inscrição."
)
@commands.has_permissions(administrator=True)
async def painel_inscrição(interaction: discord.Interaction):
 if interaction.user.guild_permissions.administrator:    
    
  await interaction.response.send_message(embed=embedInscrição, view=Inscrição())

 else:
        # Código para quando o usuário NÃO tem permissão de administrador
        await interaction.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)

@client.tree.command(
        description="Envie a embed de equipes."
)
@commands.has_permissions(administrator=True)
async def painel_equipes(interaction: discord.Interaction):
 if interaction.user.guild_permissions.administrator:    
    
  await interaction.response.send_message(embed=embedregistro)

 else:
        # Código para quando o usuário NÃO tem permissão de administrador
        await interaction.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)


@client.tree.command(
    description="Crie os 16 cargos e canais correspondentes."
)
@commands.has_permissions(administrator=True)
async def criar_cargos(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator:
        # Coloque o id da categoria desejada
        category_id = 00000000000000 
        category = discord.utils.get(interaction.guild.categories, id=category_id)
        
        if category is None:
            await interaction.response.send_message("Não foi possível encontrar a categoria especificada.", ephemeral=True)
            return

        # Dicionário para armazenar os dados das equipes
        equipes_data = {}
        equipes_data2 = {}

        # Dicionário de cores correspondentes aos números dos cargos
        cores = {
            1: discord.Color(0x0000FF),
            2: discord.Color(0x00FF00),
            3: discord.Color(0xFF0000),
            4: discord.Color(0xFFFF00),
            5: discord.Color(0x4B0082),
            6: discord.Color(0xFFA500),
            7: discord.Color(0xFF1493),
            8: discord.Color(0xB8860B),
            9: discord.Color(0xC0C0C0),
            10: discord.Color(0x1C1C1C),
            11: discord.Color(0xFFFFFF),
            12: discord.Color(0x006400),
            13: discord.Color(0x191970),
            14: discord.Color(0xA52A2A),
            15: discord.Color(0xF0E68C),
            16: discord.Color(0x00FFFF)
        }

        await interaction.response.send_message("Cargos e canais estão sendo criados, basta aguardar a conclusão...", ephemeral=True)

        # Criando 16 cargos com cores específicas e nomes
        for i in range(1, 17):
            color = cores[i]
            cargo = await interaction.guild.create_role(name=f"Cargo {i}", color=color)
            equipes_data[f"equipe_{i}"] = {"cargo_id": cargo.id, "canal_texto_id": None, "canal_voz_id": None}

        # Espera 20 segundos antes de criar canais
        await asyncio.sleep(20)

        # Criando 16 canais de texto com permissões apropriadas e atualizando dados das equipes
        for i in range(1, 17):
            role = discord.utils.get(interaction.guild.roles, name=f"Cargo {i}")
            role_id_staff = 1210828430661128223
            staff = discord.utils.get(interaction.guild.roles, id=role_id_staff)
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                role: discord.PermissionOverwrite(read_messages=True),
                staff: discord.PermissionOverwrite(read_messages=True)
            }
            canal_texto = await interaction.guild.create_text_channel(name=f"🎯・Equipe・{i}", overwrites=overwrites, category=category)
            equipes_data[f"equipe_{i}"]["canal_texto_id"] = canal_texto.id

            
            # Criando canais de voz correspondentes
            canal_voz = await interaction.guild.create_voice_channel(name=f"🔊・Equipe {i}", overwrites=overwrites, category=category)
            equipes_data[f"equipe_{i}"]["canal_voz_id"] = canal_voz.id


        # Escrevendo dados das equipes em equipes.json
        with open("equipes.json", "w") as file:
            json.dump(equipes_data, file, indent=4)

        # Escrevendo dados das equipes em equipes.json
        with open("registros.json", "w") as file:
            json.dump(equipes_data, file, indent=4)

    else:
        await interaction.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)

@client.tree.command(
    description="Remove os 16 canais e cargos"
)
@commands.has_permissions(administrator=True)
async def remover_equipes(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator:
        
        await interaction.response.send_message("Os canais e cargos estão sendo removidos, basta aguardar.", ephemeral=True)

        with open('equipes.json', 'r') as file:
            data = json.load(file)

        for equipe in data.values():
            # Substitua os números abaixo pelos IDs dos canais e cargos a serem excluídos
            cargo_id = equipe.get('cargo_id')
            canal_texto_id = equipe.get('canal_texto_id')
            canal_voz_id = equipe.get('canal_voz_id')

            # Excluir cargo
            cargo = interaction.guild.get_role(cargo_id)
            if cargo:
                await cargo.delete()

            # Excluir canal de texto
            canal_texto = interaction.guild.get_channel(canal_texto_id)
            if canal_texto:
                await canal_texto.delete()

            # Excluir canal de voz
            canal_voz = interaction.guild.get_channel(canal_voz_id)
            if canal_voz:
                await canal_voz.delete()

            # Removendo dados de equipes.json
            os.remove("equipes.json")

            # Criando um novo arquivo equipes.json vazio
            with open("equipes.json", "w") as file:
                json.dump({}, file)

            # Removendo dados de equipes.json
            os.remove("registros.json")

            # Criando um novo arquivo equipes.json vazio
            with open("registros.json", "w") as file:
                json.dump({}, file)

            # Removendo dados de equipes.json
            os.remove("permitidos.json")

            # Criando um novo arquivo equipes.json vazio
            with open("permitidos.json", "w") as file:
                json.dump({}, file)

    else:
        await interaction.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)


@client.tree.command(
    description="Remova os cargos de perdir set"
)
@commands.has_permissions(administrator=True)
async def remoção_sets(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator:
        guild = interaction.guild
        role_id = 1206479728735944804  # ID do cargo a ser removido
        
        role = guild.get_role(role_id)
        if role:
            # Obtenha todos os membros que possuem o cargo
            members_with_role = role.members
            for member in members_with_role:
                # Remova o cargo do membro
                await member.remove_roles(role)
            await interaction.response.send_message("Cargos removidos com sucesso.", ephemeral=True)
        else:
            await interaction.response.send_message("Cargo não encontrado.", ephemeral=True)
    else:
        # Código para quando o usuário NÃO tem permissão de administrador
        await interaction.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)

@client.tree.command(
    description="Enviar uma embed para todos os canais de texto das equipes."
)
@commands.has_permissions(administrator=True)
async def mensagem_equipes(interaction: discord.Interaction, titulo: str, descricao: str):
    if interaction.user.guild_permissions.administrator:
        # Carregar o arquivo equipes.json
        with open('equipes.json', 'r') as file:
            equipes = json.load(file)

        # Construir a embed com título e descrição fornecidos pelo usuário
        embedaviso = discord.Embed(
            title=titulo,
            description=descricao,
            color=discord.Color.blue()
        )
        embedaviso.set_footer(text="ZERO CUP © Todos os direitos reservados.")
        embedaviso.set_thumbnail(url="https://media.discordapp.net/attachments/1229939011393552459/1230212630107394229/2c5a9b696005b7ec35b80983bbace788.jpg?ex=66327fcb&is=66200acb&hm=c47e4807ef56382b8ef2e6c4e1377d7dea74518cfe42fe9b3dce59be39c68037&=&format=webp&width=617&height=617")

        await interaction.response.send_message("Embed sendo enviada para todos os canais de texto das equipes, basta aguardar...", ephemeral=True)
        
        # Enviar a embed para cada canal de texto de cada equipe
        for equipe in equipes.values():
            canal_id = equipe['canal_texto_id']
            canal = client.get_channel(canal_id)
            if canal:
                await canal.send(embed=embedaviso)

    else:
        # Código para quando o usuário NÃO tem permissão de administrador
        await interaction.response.send_message("Você não tem permissão para usar este comando.", ephemeral=True)

# Função para verificar se um usuário está associado a um cargo no arquivo registros.json
def verificar_associacao(registros, user_id):
    return user_id in registros

mention_counts = {}

@client.event
async def on_message(message):
    if isinstance(message.channel, discord.TextChannel) and message.channel.id == : # Id da sala que quer fazer a verificação de jogadores por equipe
        guild = message.guild

        try:
            with open('permitidos.json', 'r') as file:
                registros = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            registros = {}

        for user in message.mentions:
            role_id = registros.get(str(message.author.id), {}).get('cargo_id')
            if role_id:
                role = guild.get_role(int(role_id))
                if role:
                    await user.add_roles(role)

# TOKEN DO BOT        
client.run("") #Coloque o token do bot