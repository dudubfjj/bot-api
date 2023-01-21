# This example requires the 'message_content' privileged intents

import os
import discord
from discord.ext import commands
import requests
import datetime

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

#I'M READY
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def hello(ctx):
    await ctx.send("Choo choo! 🚅")
    
@bot.command('hora', help="!hora informa a Data e Hora atual.")
async def send_time(ctx):
    now = datetime.datetime.now()
    now = now.strftime("%d/%m/%Y às %H:%M:%S")
    

    await ctx.send("Data e hora atual: " + now)


#GAMERSCLUB LAST GAME
@bot.command(name='gc', help="Digite o id da GamersClub após o comando. Ex: !gc 322861")
async def get_url(ctx, id_gc):
    cookies = {
    '_gcl_au': '1.1.209042485.1667412074',
    '_tt_enable_cookie': '1',
    '_ttp': '07c8a5b2-ddbe-4b57-8db6-68428cd18630',
    'language': 'pt-br',
    'sib_cuid': '69ba150b-aa6a-481d-b287-e81cb7879e92',
    '_hjSessionUser_2263196': 'eyJpZCI6IjM5YzhlYjVjLTcyODctNWNlMy1hZmMzLWFhOWVlNDVmMGY1MSIsImNyZWF0ZWQiOjE2Njc0MTIxNTgyNTIsImV4aXN0aW5nIjp0cnVlfQ==',
    '_hjMinimizedPolls': '864076',
    '_hjSessionUser_1963917': 'eyJpZCI6IjU4N2MzMzlkLTJkMWUtNTlmNS1iNzE2LTZmODljMmU1YTZmMyIsImNyZWF0ZWQiOjE2Njc0MTIwNzQ1MjEsImV4aXN0aW5nIjp0cnVlfQ==',
    '_gid': 'GA1.3.195961545.1673814267',
    '_hjDonePolls': '864076%2C865658%2C872356%2C873600',
    'gclubsess': 'dc5fe6cfa591881570c87e2c0cc989ec16fe9f16',
    '_hjIncludedInSessionSample': '0',
    '_hjSession_2263196': 'eyJpZCI6ImEzZWNlZjAxLWVjZDEtNDM5Ny1hNjZjLWM4NjQyZjM0MGU5YiIsImNyZWF0ZWQiOjE2NzQyMzM1MDM1NTAsImluU2FtcGxlIjpmYWxzZX0=',
    '_hjAbsoluteSessionInProgress': '0',
    '_hjHasCachedUserAttributes': 'true',
    '__cf_bm': 'FaSi7Qur_bC7Ms8oMjKw3w38XsPQ7lD1aHfcT2g0Jj0-1674233353-0-Af90vhBup0uUKQMqGrOeK2c+x6QBLT/Uo3So7cPdLMGymPvjLdtSpDCLYcAT4wTGjiwfN69KpEVqM40YfXGYijBhTIHWdTBj6JYFTR8sMXiob7FWlI4xHAnoavMGhRuADdbSb+ReLAvsNbyCQdNBXfg=',
    '_ga': 'GA1.3.159586927.1667412074',
    'SL_C_23361dd035530_VID': 'LFlRfyq_0v',
    'SL_C_23361dd035530_KEY': 'a14d3638cda988422792e3613234743b983fdd9e',
    '_ga_H7ETJY03DT': 'GS1.1.1674233503.232.1.1674234592.60.0.0',
    '_ga_GDBFGFR1PC': 'GS1.1.1674233503.232.1.1674234592.60.0.0'}

    headers = {
        'authority': 'gamersclub.com.br',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}

    response = requests.get(f'https://gamersclub.com.br/api/box/init/{322861}', cookies=cookies, headers=headers)

    config = open('response.json', 'r', encoding='utf-8')

    await ctx.send(config)
   
    estatisticas = response['stats']

    stat = []
    value = []
    for itens_of_list in estatisticas:
        for key_of_dict, value_of_dict in itens_of_list.items():
            if key_of_dict in 'diff':
                pass       
            elif key_of_dict in 'stat':
                stat.append(value_of_dict)
            elif key_of_dict in 'value':
                value.append(value_of_dict)

    for s, v in zip(stat, value):
        await ctx.send(f'{s} = {v}')


#BANCO DE DADOS DE ID'S - GC
@bot.command(name='showids', help="!showids mostra o nosso cadastro de id's da GamersClub")
async def show_ids(ctx):    
    cadastro = open('cadastro_id.txt', 'r')
    for n in cadastro.readlines():
        n = n.split(':')
        await ctx.send(f'{n[0]}: id = {n[1]}')
    cadastro.close()
    
#CADASTRANDO NOVAS ID'S
@bot.command(name='cadastrar', help='!cadastrar e após o nick e id da GC para cadastrar uma nova id. Ex: !cadastrar dudu 322861')
async def cadastrar_ids(ctx, nickname, id_gc):
    cadastro = open('cadastro_id.txt','r+')
    if id_gc in cadastro.read():
        await ctx.send('Nosso banco de cadastros já possui este ID.')
    else:
        cadastro.writelines(f'\n{nickname}:{id_gc}')
        await ctx.send('Nickname e id cadastrados com sucesso!')
    cadastro.close()

#MUNDI UP
@bot.command(name='fm', help="!fm para saber como conseguir o update mais recente do Football Manager.")
async def get_fm_update(ctx):
    url = 'https://www.facebook.com/BrasilMundiUP'
    response = f"Para comprar o update mais recente do FM, acesse {url} e mande uma mensagem no chat da Brasil MundiUP"
    await ctx.send(response)



bot.run(os.environ["DISCORD_TOKEN"])
