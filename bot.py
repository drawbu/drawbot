import discord
import json
import random
import os
from art import *
from datetime import datetime


with open('config.json') as jsonFile:
    jsonData = json.load(jsonFile)
    jsonFile.close()
    token = jsonData['token']


class MyClient(discord.Client):


    async def on_ready(self):
        
        date = str(datetime.now())[0:19]
        print(date +' : Connecté en temps que {0} !'.format(self.user))
        main_channel = client.get_channel(693103058086789130)
        


    async def on_member_join(self, member):
        await client.send_message(member, 'Prompt.')


    async def on_message(self, message):
        date = str(datetime.now())[0:19]
        print(date + ' : Message de {0.author} ({0.author.id}) : {0.content}'.format(message))


        if message.content.startswith('!help'): #affiche toutes les commandes du bot

            arguments = 'Message invoqué par {0.author}'.format(message)

            embed=discord.Embed(title='Commande disponibles par drawbot 2.0 :', description='Aujourd\'hui, je suis assez limité comme bot, mais avec le temps, je deviendrais extremement puissant haha\n\n!help : affiche ce message \n!counter : compte le nombre de caractères de votre message \n!tesbg : ajoute un réaction \'spéciale\' au message \n!pierrefeuilleciseaux ou !chifoumi : partie de pierre feuille ciseaux contre moi \n!ascii : tranforme du texte en ascii \n!issou : issou \n!score : affiche le score du joueur demandé \n!casino : permet de jouer au casino', color=0x11a4d4)
            embed.add_field(name=arguments, value= 'Pour apprendre comment utiliser les commandes, il suffit de taper la commande', inline=False)
            await message.channel.send(embed=embed)

        if message.content.startswith('!counter'): #compte le nombre de caractères du message
            
            alphabet="abcdefghijklmnopqrstuvwxyz0123456789éèêëàâäôöîïùûüç!\"#$%&'()*+,-./0123456789:;<=>?@[]^_`{|}~"
            texte = message.content
            texte = texte[8:len(texte)]
            lettre = int(0)
            arguments = ''

            while lettre != (len(alphabet)) :
                if alphabet[lettre] in texte :
                    arguments = str(alphabet[lettre]) + ' est présent ' + str(texte.count(alphabet[lettre])) + ' fois !'
                    await message.channel.send(arguments)
                lettre += 1

        if message.content.startswith('!tesbg'): #ajoute un réaction au message

            await message.add_reaction('🇹')
            await message.add_reaction('🇴')
            await message.add_reaction('ℹ️')
            await message.add_reaction('🇦')
            await message.add_reaction('🇺')
            await message.add_reaction('🇸')
            await message.add_reaction('🇮')

        if message.content.startswith('!pierrefeuilleciseaux') or message.content.startswith('!chifoumi'): #partie de pierre feuille ciseaux contre le bot

            emojiRock = '🪨'
            emojiScissors = '✂️'
            emojiPaper = '🧻'
            choix = random.choice([emojiRock, emojiScissors, emojiPaper])

            texte = message.content

            if texte.startswith('!pierrefeuilleciseaux') :
                texte = texte[22:len(texte)]
            elif texte.startswith('!chifoumi') :
                texte = texte[10:len(texte)]
            
            if texte == '' :
                await message.channel.send('Pour jouer, envoie \'!pierrefeuilleciseaux\' ou \'chifoumi\' suivi de 🪨 , ✂️ ou 🧻')
            
            elif texte == '🪨' or texte == '✂️' or texte == '🧻' :


                username = '{0.author.id}'.format(message)
                file = 'users/' + username + '.json'

                listFile = os.listdir('users')

                if (username + ('.json')) in listFile :
                    print('joueur ',username,'deja present')
                else :
                    print('nouveau joueur : ',username)
                    with open(file, 'w') as jsonFile:
                        json.dump({"games":0,"wins": 0, "money": 100, "daily":0}, jsonFile)
                        jsonFile.close()

                with open(file) as jsonFile:
                    userData = json.load(jsonFile)
                    jsonFile.close()


                if texte == choix :
                    resultat = ('Dommage, égalité !')
            
                else : 
                    if (texte == emojiRock and choix == emojiScissors) or (texte == emojiScissors and choix == emojiPaper) or (texte == emojiPaper and choix == emojiRock) :
                        resultat = ('Bien joué tu m\'as battu (crois pas t\'es fort c\'est aléatoire ^^).')
                        userData['wins'] += 1
                
                    else :
                        resultat = ('Enfait t\'es eclatax')


                with open(file, 'w') as jsonFile:
                    userData['games'] += 1
                    json.dump(userData, jsonFile)
                    jsonFile.close()
                    if userData['games'] == 0 :
                        score = 'pas de parties'
                    else :
                        score = userData['wins']/userData['games']*100
                    print (score)


                await message.delete()

                arguments = 'Contre {0.author}'.format(message)

                score = str(score)
                score = score[0:4]

                embed=discord.Embed(title=arguments, description=texte + ' vs ' + choix, color=0xababab)
                embed.set_author(name="Pierre, feuilles, ciseaux !")
                embed.set_footer(text=resultat + '\nTon ratio de victoire est de ' + score + '%')
                await message.channel.send(embed=embed)

            else :

                await message.channel.send('Je... suis pas sûr que tu ai bien compris les règles')
               
        if message.content.startswith('!ascii'): #tranforme du texte en ascii
            
            texte = message.content
            texte = texte[7:len(texte)]

            fontList = ['cybermedium','bubble','block','small','block','white_bubble','random-small','random-medium','random-large','random-xlarge','random','magic']
            fontNum = 0
            arguments = 0

            while fontNum != len(fontList) :
                if texte.startswith(fontList[fontNum]) :
                    texte = texte[len(fontList[fontNum]) + 1:len(texte)]
                    arguments = '```' + text2art(texte, font=fontList[fontNum]) + '```'
                fontNum += 1
            if arguments == 0 :
                arguments = '```' + text2art(texte) + '```'


            if len(arguments) <= 2000 :
                if texte == '' :
                    await message.channel.send('Rajoue du texte après le \'!ascii\' pour que j\'affiche un résultat. \nTu peux aussi écrire avec différentes polices. Pour ce faire, rajoute \'cybermedium\', \'bubble\', \'block\', \'small\', \'block\', \'white_bubble\', \'random\', \'random-small\', \'random-medium\', \'random-large\', \'random-xlarge\' ou \'magic\' après le \'!ascii\'.')
                else :
                    await message.channel.send(arguments)
            else :
                await message.channel.send('Désolé, la phrase est trop grande')
        
        if message.content.startswith('!issou'): #issou

            await message.delete() 
            await message.channel.send('https://tenor.com/view/risitas-main-dent-issou-laugh-gif-9505807')

        if message.content.startswith('!casino'): #permet de jouer au casino

            texte = message.content
            texte = texte[8:len(texte)]

            if texte == '' :
                await message.channel.send('Pour jouer, mise une somme après le \'!casino\'.Tu commence avec la modique somme de 100 d$ !')
            elif texte == 'reset' :
                
                username = '{0.author.id}'.format(message)
                file = 'users/' + username + '.json'
                listFile = os.listdir('users')

                if (username + ('.json')) in listFile :
                    print('joueur ',username,'deja present')
                else :
                    print('nouveau joueur : ',username)
                    with open(file, 'w') as jsonFile:
                        json.dump({"games":0,"wins": 0, "money":100, "daily":0}, jsonFile)
                        jsonFile.close()

                with open(file) as jsonFile:
                    userData = json.load(jsonFile)
                    jsonFile.close()

                userData['money'] = 100
                
                with open(file, 'w') as jsonFile:
                        json.dump(userData, jsonFile)
                        jsonFile.close()

                await message.channel.send('Ton compte à été remis à zero, tu possède maintenant 100 d$ !')

            elif '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9' or '0' in texte :

                money = int(''.join(list(filter(str.isdigit, texte))))

                username = '{0.author.id}'.format(message)
                file = 'users/' + username + '.json'
                listFile = os.listdir('users')

                resultat = random.choice(['gagné','perdu'])

                if (username + ('.json')) in listFile :
                    print('joueur ',username,'deja present')
                else :
                    print('nouveau joueur : ',username)
                    with open(file, 'w') as jsonFile:
                        json.dump({"games":0,"wins": 0, "money":100, "daily":0}, jsonFile)
                        jsonFile.close()

                with open(file) as jsonFile:
                    userData = json.load(jsonFile)
                    jsonFile.close()

                
                if (money <= 0) or (money > userData['money']) :
                    arguments = 'Désolé tu n\'a pas assez d\'argent pour jouer cette somme. Tu ne possède actuellement que ' + str(userData['money']) + ' d$.'
                    await message.channel.send(arguments)
                elif money <= 0 :
                    await message.channel.send('Désolé tu est maintenant trop pauvre pour jouer...')
                else :

                    if resultat == 'gagné' :
                        userData['money'] += money
                    elif resultat == 'perdu' :
                        userData['money'] -= money

                    with open(file, 'w') as jsonFile:
                        json.dump(userData, jsonFile)
                        jsonFile.close()

                    arguments = 'Tu as ' + resultat + ' ! Tu possède actuellement ' + str(userData['money']) + ' d$ !'

                    await message.delete()

                    embed=discord.Embed(title='{0.author}'.format(message) , description='Tu as ' + resultat + ' !', color=0xababab)
                    embed.set_author(name="Casino 🎲 💸")
                    embed.set_footer(text='Tu possède actuellement ' + str(userData['money']) + ' d$ ! Tu avais misé ' + str(money))
                    await message.channel.send(embed=embed)


                    username =  '{0.author.id}'.format(message)

            
                    file = 'users/' + username + '.json'
                    listFile = os.listdir('users')

                    
                    with open(file) as jsonFile:
                        userData = json.load(jsonFile)
                        jsonFile.close()

                    userMoney = userData['money']


                    file = 'classement.json'
                    listFile = os.listdir('.')

                    classement = 1

                    if (file) not in listFile :
                        print ('ce fichier n\'existe pas')
                    else : 
                        with open(file) as jsonFile:
                            classementData = json.load(jsonFile)
                            jsonFile.close()

                while classement != 10 :
                    if classementData[str(classement)] == username :
                        classement = 10
    
                    else :

                        concurrent = classementData[str(classement)]
                        if concurrent != 0 :
                            with open('users/' + str(concurrent) + '.json') as jsonFile:
                                userData = json.load(jsonFile)
                                jsonFile.close()

                            print(userData['money'] , userMoney)

                            if userData['money'] < userMoney :
                                classementData[str(classement)] = username
                                print('le joueur ' + str(username) + 'est maintenant ' + str(classement) + 'ième')
                                if username == '{0.author.id}'.format(message) :
                                    await message.channel.send('Vous êtes maintenant numéro ' + str(classement) + ' dans le classement')
                                username = concurrent

                            classement += 1
                
                        else :
                            classementData[str(classement)] = username
                            print('le joueur ' + str(username) + ' est maintenant ' + str(classement) + 'ième')
                            classement = 10

                        with open(file, 'w') as jsonFile:
                            json.dump(classementData, jsonFile)
                            jsonFile.close()

            else :
                await message.channel.send('Pour jouer, mise une somme après le \'!casino\'.Tu commence avec la modique somme de 100 d$ !')

        if message.content.startswith('!score'): #affiche le score d'un joueur

            username = message.content
            username = username[10:28]

            if username == '' :
                username = '{0.author.id}'.format(message)
            
            file = 'users/' + username + '.json'

            listFile = os.listdir('users')

            if (username + ('.json')) in listFile :
                with open(file) as jsonFile:
                    userData = json.load(jsonFile)
                    jsonFile.close()
      
                score = str(userData['wins']/userData['games']*100)
                score = score[0:4]
                arguments = 'Au chifoumi, ce joueur à un score de ' + score + '% ! Sur ' + str(userData['games']) + ' parties jouées, il en a gagné ' + str(userData['wins']) + ' !\nEt au casino, ce joueur à un score de ' + str(userData['money']) + ' d$ !'
                await message.channel.send(arguments)
            else :
                await message.channel.send('Je ne connais pas ce joueur')

        if message.content.startswith('!daily') : #récupère les récompenses journalières

            username = '{0.author.id}'.format(message)
            
            file = 'users/' + username + '.json'
            listFile = os.listdir('users')

            if (username + ('.json')) not in listFile :
                with open(file, 'w') as jsonFile:
                    json.dump({"games":0,"wins": 0, "money":100, "daily":0}, jsonFile)
                    jsonFile.close()

            with open(file) as jsonFile:
                userData = json.load(jsonFile)
                jsonFile.close()

            if userData['daily'] == str(datetime.now())[0:10] :
                arguments = 'Désolé, tu as déjà récupéré ton argent quotidient. Tu es à ' + str(userData['money']) + ' d$ !'
                await message.channel.send(arguments)
            else :
                userData['money'] += 100
                userData['daily'] = str(datetime.now())[0:10]
                arguments = 'Tu as bien récupéré ton argent quotidient. Tu es à ' + str(userData['money']) + ' d$ !'
                await message.channel.send(arguments)

            with open(file, 'w') as jsonFile:
                json.dump(userData, jsonFile)
                jsonFile.close()

            username =  '{0.author.id}'.format(message)

            
            file = 'users/' + username + '.json'
            listFile = os.listdir('users')

                    
            with open(file) as jsonFile:
                userData = json.load(jsonFile)
                jsonFile.close()

            userMoney = userData['money']


            file = 'classement.json'
            listFile = os.listdir('.')

            classement = 1

            if (file) not in listFile :
                print ('ce fichier n\'existe pas')
            else : 
                with open(file) as jsonFile:
                    classementData = json.load(jsonFile)
                    jsonFile.close()

            while classement != 10 :
                if classementData[str(classement)] == username :
                    classement = 10
    
                else :

                    concurrent = classementData[str(classement)]
                    if concurrent != 0 :
                        with open('users/' + str(concurrent) + '.json') as jsonFile:
                            userData = json.load(jsonFile)
                            jsonFile.close()

                        print(userData['money'] , userMoney)

                        if userData['money'] < userMoney :
                            classementData[str(classement)] = username
                            print('le joueur ' + str(username) + 'est maintenant ' + str(classement) + 'ième')
                            if username == '{0.author.id}'.format(message) :
                                await message.channel.send('Vous êtes maintenant numéro ' + str(classement) + ' dans le classement')
                            username = concurrent

                        classement += 1
                
                    else :
                        classementData[str(classement)] = username
                        print('le joueur ' + str(username) + ' est maintenant ' + str(classement) + 'ième')
                        classement = 10

                    with open(file, 'w') as jsonFile:
                        json.dump(classementData, jsonFile)
                        jsonFile.close()
      
        if message.content.startswith('!classement') : #affiche les plus grosses fortunes

            listFile = os.listdir('.')
            if 'classement.json' in listFile :
                with open('classement.json') as jsonFile:
                    classementData = json.load(jsonFile)
                    jsonFile.close()

            userData = ''
            listUsers = os.listdir('./users')
            classement = 1
            arguments = ''
            while classement != 10 :
                if classementData[str(classement)] != 0 :
                    if 'classement.json' in listFile :
                        with open('users/'+classementData[str(classement)] +'.json') as jsonFile:
                            userData = json.load(jsonFile)
                            jsonFile.close()
                    arguments += '\nNuméro ' + str(classement) + ' : <@!' + classementData[str(classement)] + '> avec ' + str(userData['money']) + ' $d'
                    classement += 1
                else : 
                    classement = 10
            embed = discord.Embed(title="Classement du casino", description=arguments)
            await message.channel.send(embed=embed)


        date = str(datetime.now())[0:19]
        logsFile = open('logs.txt','a')
        arguments = ('\n' + date + ' : Message de {0.author} ({0.author.id}) : {0.content}').format(message)
        logsFile.write(arguments) 
        logsFile.close()

        

client = MyClient()
client.run(token)