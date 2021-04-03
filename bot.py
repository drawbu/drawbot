import discord, urllib.request, bs4, json, random, os, logging, subprocess, platform, operator, time, pronotepy
from discord.ext import commands, tasks
from art import *
from datetime import datetime

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)

mainFiles = './'

#Configuation des fichiers morpion.json et config.json par défault
morpionJson = {'player': '', 'tours': 0, 'joueur': 'O', 'entree': 0, 'victoire': False, 'plateau': ' 123456789', 'bot': '', 'dernier': ''}
configJson = {'token': '0', 'prefix': ';'}

# Fonctions principales (fonctions très utiles)
def openFile(repertory,file,action,fileData = None) :
    """Permet de créer ou ouvrir des fichier json. Dans action il faut mettre 'r' pour lire et 'w' pour remplacer le contenu du fichier par fileData. Si le fichier n'existe pas, il faut faire 'w'."""
    with open(repertory + file + '.json',action) as jsonFile:
        if action == 'r' :
            fileData = json.load(jsonFile)
        elif action == 'w' :
            json.dump(fileData, jsonFile)
        jsonFile.close()
        return fileData

def verifyFile(repertory,file,fileJson) :
    """Nécessite openFile(). Permet de créer un fichier si il n'existe pas et sinon de vérifier si le contenu du fichier correspond bien à au modèle (fileJson)."""
    if (file + '.json') not in os.listdir(repertory) :
        openFile(repertory, file, 'w', fileJson)
    fileData = openFile(repertory, file, 'r', 0)
    for cle,valeur in fileJson.items():
        if cle not in fileData.keys() :
            fileData[cle] = fileJson[cle]
    openFile(repertory, file, 'w', fileData)
    return fileData

def createDir(repertory):
    """Créé un dossier, et si n'existe pas ne fait rien"""
    try:
        os.mkdir(repertory)
    except:
        pass

# Fonctions secondaires (pour des utilisations précises)
def affichageMorpion(plateau) :
    curseur = 1
    affichage = ''
    while curseur != 10 :
        if plateau[curseur] == 'O' :
            affichage += ':o:'
        elif plateau[curseur] == 'X' :
            affichage += ':x:'
        elif plateau[curseur] == '1' :
            affichage += ':one:'
        elif plateau[curseur] == '2' :
            affichage += ':two:'
        elif plateau[curseur] == '3' :
            affichage += ':three:'
        elif plateau[curseur] == '4' :
            affichage += ':four:'
        elif plateau[curseur] == '5' :
            affichage += ':five:'
        elif plateau[curseur] == '6' :
            affichage += ':six:'
        elif plateau[curseur] == '7' :
            affichage += ':seven:'
        elif plateau[curseur] == '8' :
            affichage += ':eight:'
        elif plateau[curseur] == '9' :
            affichage += ':nine:'
        if curseur == 3 or curseur == 6:
            affichage += '\n'
        curseur += 1
    return affichage

def ping(host):
    
    #Returns True if host responds to a ping request
    #author : https://stackoverflow.com/a/35625078
    # ping.py  2016-02-25 Rudolf
    # Ping parameters as function of OS
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
    args = "ping " + " " + ping_str + " " + host
    need_sh = False if  platform.system().lower()=="windows" else True

    # Ping
    return subprocess.call(args, shell=need_sh) == 0

def mois(mois):
    mois = 0
    if mois == 2 :
        mois = 31
    elif mois == 3 :
        mois = 59
    elif mois == 4 :
        mois = 90
    elif mois == 5 :
        mois = 120
    elif mois == 6 :
        mois = 151
    elif mois == 7 :
        mois = 181
    elif mois == 8 :
        mois = 212
    elif mois == 9 :
        mois = 243
    elif mois == 10 :
        mois = 273
    elif mois == 11 :
        mois = 304
    elif mois == 12 :
        mois = 334
    return mois

openFile(mainFiles,'morpion','w',morpionJson)

#Création/vérifcation du fichier config
config = verifyFile(mainFiles, 'config', configJson)
token = config['token']


@client.event
async def on_ready():
    devoirs_pronote.start()
    print('Connecté en temps que {0.user.name} !'.format(client))


@client.event
async def on_member_join(member):
    serverFiles = './servers/' + str(member.guild.id) + '/'
    server = openFile(serverFiles,'server','r',0)
    channelWelcome = client.get_channel(server['welcome']) 
    print('[{0.guild}] Le membre {0.name} viens de rejoindre le serveur'.format(member))   
    for channel in member.guild.channels :
        if server['welcome'] == channel.id :
            embed = discord.Embed(title='Un nouveau membre viens de nous rejoindre !', description='Bienvenue <@!' + str(member.id) + '> !', color=0x009dff)
            await channelWelcome.send(embed=embed)


@client.event
async def on_message(message):

    def commande(commande):
        if message.content.startswith(commande):
            return True
        else :
            return False

    date = str(datetime.now())[0:19]

    # l'emplacement des différents dossiers
    mainFiles = './'
    if message.channel.type is not discord.ChannelType.private:
        serversBaseFiles = mainFiles + 'servers/'
        serverFiles = serversBaseFiles + '{0.guild.id}/'.format(message)
        usersFiles = serverFiles + 'users/'
    
    # variables utiles
    owner = client.get_user(352125871617736704)

    # configuation des fichiers morpion.json et config.json par défault
    config_idle = {'startIdleMaxTime': 3,}
    userJson = {'games':0, 'wins': 0, 'money':100, 'daily':0, 'derniereconnexion':str(datetime.now()), 'patates':0, 'mais':0, 'carrotes':0, 'poulailler':0, 'idleMaxTime': 3}
    serverJson = {'welcome':None}
    idleJson = {'afklesstime':3,'afkmaxtime':72,'patates':{'prix':5,'revenus':1,'unlock':0,'max':50},'mais':{'prix':15,'revenus':2,'unlock':200,'max':50},'carrotes':{'prix':40,'revenus':4,'unlock':600,'max':50},'poulailler':{'prix':100,'revenus':8,'unlock':1500,'max':50}}


    #Logs
    messageLogs = message.content.replace('\n', ' ')
    if message.channel.type is discord.ChannelType.private:
        print(f'[{(message.created_at.isoformat(sep="T", timespec="seconds")).replace("T"," ")}] [{message.created_at}] [{message.channel}] : {messageLogs}')
    else :
        print(f'[{(message.created_at.isoformat(sep="T", timespec="seconds")).replace("T"," ")}] [{message.guild}] [#{message.channel}] {message.author.name} : {messageLogs}')


    # récupération des fichier config
    commandes = verifyFile(mainFiles,'commandes',{})

    if message.channel.type is not discord.ChannelType.private:
        # création du dossier pour les serveurs
        createDir(serversBaseFiles)

        # création/vérification du dossier et du fichier serveur
        createDir(serverFiles)
        server = verifyFile(serverFiles, 'server', serverJson)

        # création/vérification du dossier et du fichier utilisateur
        createDir(usersFiles)
        userData = verifyFile(usersFiles,str(message.author.id),userJson)


    if message.content.startswith(config['prefix'] + 'pierrefeuilleciseaux') or message.content.startswith(config['prefix'] + 'chifoumi'): #partie de pierre feuille ciseaux contre le bot

        emojiRock = '🪨'
        emojiScissors = '✂️'
        emojiPaper = '🧻'
        choix = random.choice([emojiRock, emojiScissors, emojiPaper])

        texte = message.content

        if texte.startswith(config['prefix'] + 'pierrefeuilleciseaux') :
            texte = message.content[len(config['prefix']) + 21 :len(message.content)]
        elif texte.startswith(config['prefix'] + 'chifoumi') :
            texte = message.content[len(config['prefix']) + 9 :len(message.content)]
        
        print(texte)
        
        if texte == '' :
            await message.channel.send('Pour jouer, envoie \'!pierrefeuilleciseaux\' ou \'chifoumi\' suivi de 🪨 , ✂️ ou 🧻')
        
        elif texte == '🪨' or texte == '✂️' or texte == '🧻' :

            username = '{0.author.id}'.format(message)

            if (username + ('.json')) not in os.listdir(usersFiles) :
                print('Nouveau joueur : ',username)
                openFile(usersFiles,username,'w',{"games":0, "wins": 0, "money":100, "daily":0, "derniereconnexion":0, "champsdepatate":1, "ferme": 0})

            userData = openFile(usersFiles,username,'r',0)

            if texte == choix :
                resultat = ('Dommage, égalité !')
        
            else : 
                if (texte == emojiRock and choix == emojiScissors) or (texte == emojiScissors and choix == emojiPaper) or (texte == emojiPaper and choix == emojiRock) :
                    resultat = ('Bien joué tu m\'as battu (crois pas t\'es fort c\'est aléatoire ^^).')
                    userData['wins'] += 1
            
                else :
                    resultat = ('Enfait t\'es eclatax')

            userData['games'] += 1
            
            openFile(usersFiles,username,'w',userData)    
            score =  (str(userData['wins']/userData['games']*100))[0:4]
            arguments = 'Contre {0.author}'.format(message)

            await message.delete()

            embed=discord.Embed(title=arguments, description=texte + ' vs ' + choix, color=0xababab)
            embed.set_author(name="Pierre, feuilles, ciseaux !")
            embed.set_footer(text=resultat + '\nTon ratio de victoire est de ' + score + '%')
            await message.channel.send(embed=embed)

        else :

            await message.channel.send('Je... suis pas sûr que tu ai bien compris les règles')

    if message.content.startswith(config['prefix'] + 'help'): #affiche toutes les commandes du bot

        arguments = 'Aujourd\'hui, je suis assez limité comme bot, mais avec le temps, je deviendrais extremement puissant haha\n\n**' + config['prefix'] + 'help :** affiche ce message \n**' + config['prefix'] + 'counter :** compte le nombre de caractères de votre message \n**' + config['prefix'] + 'pierrefeuilleciseaux** ou **' + config['prefix'] + 'chifoumi :** partie de pierre feuille ciseaux contre moi \n**' + config['prefix'] + 'ascii :** tranforme du texte en ascii \n**' + config['prefix'] + 'issou :** issou \n**' + config['prefix'] + 'score :** affiche le score du joueur demandé \n**' + config['prefix'] + 'casino :** permet de jouer au casino \n**' + config['prefix'] + 'daily :** récupère les récompenses journalières \n** ' + config['prefix'] + 'bug :** Sert a prévenir drawbu d\'un bug \n**' + config['prefix'] + 'prefix :** Sert a changer le prefix des commandes \n**!prefix reset :** Sert à reset le prefix quel qu\'il soit \n' + config['prefix'] + 'commande : Permet de faire de nouvelles commandes' + config['prefix'] + 'morpion : Permet de jouer au morpion \n**' + config['prefix'] + 'ping :** Permet de marquer de vérifier qu\'un site est en ligne \n**' + config['prefix'] + 'bye :** Le bot de déconnecte \n**' + config['prefix'] + 'idle :** Permet de jouer à un idle (trop bien)'
        embed=discord.Embed(title='Commande disponibles par {0.user.name} :'.format(client) , description=arguments, color=0x11a4d4)

        arguments = 'Message invoqué par {0.author}'.format(message)
        embed.add_field(name=arguments, value= 'Pour apprendre comment utiliser les commandes, il suffit de taper la commande', inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith(config['prefix'] + 'casino'): #permet de jouer au casino

        texte = message.content[len(config['prefix']) + 7 :len(message.content)]

        if texte == '' :
            await message.channel.send('Pour jouer, mise une somme après le \'!casino\'.Tu commence avec la modique somme de 100 d$ !')

        elif '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9' or '0' in texte :

            money = int(''.join(list(filter(str.isdigit, texte))))

            username = '{0.author.id}'.format(message)

            resultat = random.choice(['gagné','perdu'])

            if (username + ('.json')) not in os.listdir(usersFiles) :
                print('nouveau joueur dans la base de donnée : ',username)
                openFile(usersFiles,username,'w',{"games":0, "wins": 0, "money":100, "daily":0, "derniereconnexion":0, "champsdepatate":1, "ferme": 0})

            userData = openFile(usersFiles,username,'r',0)

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

                openFile(usersFiles,username,'w',userData)

                arguments = 'Tu as ' + resultat + ' ! Tu possède actuellement ' + str(userData['money']) + ' d$ !'

                await message.delete()

                embed=discord.Embed(title='{0.author}'.format(message) , description='Tu as ' + resultat + ' !', color=0xababab)
                embed.set_author(name="Casino 🎲 💸")
                embed.set_footer(text='Tu possède actuellement ' + str(userData['money']) + ' d$ ! Tu avais misé ' + str(money))
                await message.channel.send(embed=embed)

        else :
            await message.channel.send('Pour jouer, mise une somme après le \'!casino\'.Tu commence avec la modique somme de 100 d$ !')

    if message.content.startswith(config['prefix'] + 'daily') : #récupère les récompenses journalières

        username = '{0.author.id}'.format(message)

        if (username + ('.json')) not in os.listdir(usersFiles) :
            openFile(usersFiles,username,'w',{"games":0, "wins": 0, "money":100, "daily":0, "derniereconnexion":0, "champsdepatate":1, "ferme": 0})

        userData = openFile(usersFiles,username,'r',0)

        if userData['daily'] == str(datetime.now())[0:10] :
            arguments = 'Désolé, tu as déjà récupéré ton argent quotidient. Tu es à ' + str(userData['money']) + ' d$ !'
            await message.channel.send(arguments)
        else :
            userData['money'] += 100
            userData['daily'] = str(datetime.now())[0:10]
            arguments = 'Tu as bien récupéré ton argent quotidient. Tu es à ' + str(userData['money']) + ' d$ !'
            await message.channel.send(arguments)

        openFile(usersFiles,username,'w',userData)

    if message.content.startswith(config['prefix'] + 'hourly') : #récupère les récompenses journalières

        username = '{0.author.id}'.format(message)

        if (username + ('.json')) not in os.listdir(usersFiles) :
            openFile(usersFiles,username,'w',{"games":0, "wins": 0, "money":100, "daily":0, "hourly": 0, "derniereconnexion":0, "champsdepatate":1, "ferme": 0})

        userData = openFile(usersFiles,username,'r',0)

        if userData['daily'] == str(datetime.now())[0:13] :
            arguments = 'Désolé, tu as déjà récupéré ton argent cette heure. Tu es à `' + str(userData['money']) + '` d$ !'
            await message.channel.send(arguments)
        else :
            userData['money'] += 20
            userData['daily'] = str(datetime.now())[0:13]
            arguments = 'Tu as bien récupéré ton argent de cette heure. Tu es à `' + str(userData['money']) + '` d$ !'
            await message.channel.send(arguments)

        openFile(usersFiles,username,'w',userData)

    if message.content.startswith(config['prefix'] + 'morpion') : #Permet de jouer au morpion

        victoire = False
        morpion = openFile(mainFiles,'morpion','r',0)

        if morpion['player'] == "" :

            morpion['player'] = '{0.author.id}'.format(message)

            await message.channel.send('BIENVENUE DANS LE MORPION ! Toutes les cases sont égales aux touches du clavier.')

            morpion['joueur'] = random.choice(['X','O'])

            if morpion['joueur'] == 'X' :
                morpion['bot'] = 'O'
            elif morpion['joueur'] == 'O' :
                morpion['bot'] = 'X'

            if random.choice([0,1]) == 0 :
                arguments = 'Je commence ! Tu joues les ":' + morpion['joueur'].lower() + ':" !'
                await message.channel.send(arguments)
                morpion['tours'] += 1
                entree = random.choice([1,2,3,4,5,6,7,8,9])
                plateau = morpion['plateau'][0:entree] + morpion['bot'] +  morpion['plateau'][entree+1:10]

                embed=discord.Embed(title='Partie de morpion avec {0.author.name}'.format(message), color=0x009dff)
                embed.add_field(name='Plateau :', value=affichageMorpion(plateau), inline=True)
                embed.add_field(name='A ton tour ( ' + morpion['joueur'] + ' )', value=str(morpion['tours']) + ' coups', inline=True)
                await message.channel.send(embed=embed)

                morpion['plateau'] = plateau
                openFile(mainFiles,'morpion','w',morpion)

            else : 
                arguments = 'Tu commences avec les "' + morpion['joueur'] + '" !'
                await message.channel.send(arguments)


            openFile(mainFiles,'morpion','w',morpion)

        elif morpion['player'] == '{0.author.id}'.format(message) :
            await message.delete()
            entree = message.content[len(config['prefix']) + 8 :len(message.content)]
            if (entree == '1') or (entree == '2') or (entree == '3') or (entree == '4') or (entree == '5') or (entree == '6') or (entree == '7') or (entree == '8') or (entree == '9') :
                entree = int(entree)
                if (morpion['plateau'][entree] == 'X') or (morpion['plateau'][entree] == 'O'):
                    await message.channel.send('Quelqu\'un à déjà joué sur cette case !')
                else :
                    morpion['tours'] += 1
                    plateau = morpion['plateau'][0:entree] + morpion['joueur'] +  morpion['plateau'][entree+1:10]

                    embed=discord.Embed(title='Partie de morpion avec {0.author.name}'.format(message), color=0x009dff)
                    embed.add_field(name='Plateau :', value=affichageMorpion(plateau), inline=True)
                    embed.add_field(name='Au tour du bot', value=str(morpion['tours']) + ' coups', inline=True)
                    await message.channel.send(embed=embed)

                    morpion['plateau'] = plateau
                    morpion['dernier'] = morpion['joueur']
                    openFile(mainFiles,'morpion','w',morpion)

                    if plateau[1]==plateau[2]==plateau[3] or plateau[4]==plateau[5]==plateau[6] or plateau[7]==plateau[8]==plateau[9] or plateau[1]==plateau[4]==plateau[7] or plateau[2]==plateau[5]==plateau[8] or plateau[3]==plateau[6]==plateau[9] or plateau[1]==plateau[5]==plateau[9] or plateau[3]==plateau[5]==plateau[7] :
                        victoire = True
                        morpion['tours'] = 9 
            
                    if morpion['tours'] < 9 :
                        morpion['tours'] += 1
                        entree = random.choice([1,2,3,4,5,6,7,8,9])
                        while (morpion['plateau'][entree] == 'X') or (morpion['plateau'][entree] == 'O'):
                            entree = random.choice([1,2,3,4,5,6,7,8,9])
                        plateau = morpion['plateau'][0:entree] + morpion['bot'] +  morpion['plateau'][entree+1:10]

                        embed=discord.Embed(title='Partie de morpion avec {0.author.name}'.format(message), color=0x009dff)
                        embed.add_field(name='Plateau :', value=affichageMorpion(plateau), inline=True)
                        embed.add_field(name='A ton tour ( ' + morpion['joueur'] + ' )', value=str(morpion['tours']) + ' coups', inline=True)
                        await message.channel.send(embed=embed)

                        morpion['plateau'] = plateau
                        morpion['dernier'] = morpion['bot']
                        openFile(mainFiles,'morpion','w',morpion)

                        if plateau[1]==plateau[2]==plateau[3] or plateau[4]==plateau[5]==plateau[6] or plateau[7]==plateau[8]==plateau[9] or plateau[1]==plateau[4]==plateau[7] or plateau[2]==plateau[5]==plateau[8] or plateau[3]==plateau[6]==plateau[9] or plateau[1]==plateau[5]==plateau[9] or plateau[3]==plateau[5]==plateau[7] :
                            victoire = True
                            morpion['tours'] = 9 

                if morpion['tours'] == 9:
                    if victoire == True:
                        if morpion['dernier'] == morpion['bot'] :
                            await message.channel.send('T\'as perdu nullos')
                        else :
                            await message.channel.send('Bien joué... t\'as gagné...')
                    else:
                        await message.channel.send("Egalite, dommage !")
                    
                    
                    morpion['player'] = ""
                    morpion['tours'] = 0
                    morpion['joueur'] = "O"
                    morpion['entree'] = 0
                    morpion['victoire'] = False
                    morpion['plateau'] = " 123456789"
                    morpion['bot'] = ""
                    morpion['dernier'] = ""
                    openFile(mainFiles,'morpion','w',morpion)

            elif entree == 'stop' :
                
                morpion['player'] = ""
                morpion['tours'] = 0
                morpion['joueur'] = "O"
                morpion['entree'] = 0
                morpion['victoire'] = False
                morpion['plateau'] = " 123456789"
                morpion['bot'] = ""
                morpion['dernier'] = ""
                openFile(mainFiles,'morpion','w',morpion)
                await message.channel.send('Fin de la partie pour cause d\'abandon')
                
                

            else :
                arguments = 'Pour jouer, il faut envoyer ' + config['prefix'] + 'morpion suivi d\'un chiffre'
                await message.channel.send(arguments)
                await message.channel.send(message.content[len(config['prefix']) + 8 :len(message.content)])
               
            
            openFile(mainFiles,'morpion','w',morpion)

        else :
            arguments = 'Désolé, une partie est déja en cours avec <@!' + morpion['player'] + '> !'.format(message)
            await message.channel.send(arguments)

    if message.content.startswith(config['prefix'] + 'idle') : #permet de jouer au jeu idle
        
        texte = message.content[len(config['prefix']) + 5:len(message.content)]

        if texte.startswith('help') :
            embed = discord.Embed(title='Tutoriel :', description= f'Vous pouvez acheter des propriétés à l\'aide de la commande `{config["prefix"]}idle buy` suivi de l\'émoji de la propriété et finalement du nombre de propriétés que vous voulez acheter.\nVous commencez cette aventure avec rien. Seuls vos revenus journaliers (`{config["prefix"]}daily`) comme source de revenus. Mais il est temps d\'étendre votre empire et faire du revenus ! Achetez dès maintenant des propriétés !\nEssayez la commande `{config["prefix"]}idle`.\n\n**Règles :**\n - Au début du jeu, seuls les champs de patate sont achetable. Mais avec vos revenus, vous pourrez débloquer de nouvelles possibilités.\n - Au début, vous ne pouvez récupérer les revenus des {idleJson["afklesstime"]} dernières heures seulements.\n\n**Listes des commandes :**\n- `;idle` : affiche vos propriétés\n- `;idle help` : affiche cette fenêtre\n- `;idle buy` : permet d\'acheter une ou plusieurs propriétés\n- `;idle unlock` : permet de débloquer une catégorie\n - `{config["prefix"]}idle upmaxtime` : permet d\'acheter du temps d\'AFK supplémentaire.\n\n**Exemple :** pour acheter 3 champs de patates, je dois faire "**{config["prefix"]}idle buy :potato: 3**". \n\n**Liste des propriétés achetables :** \n- :potato: Champ de patate (prix : `{idleJson["patates"]["prix"]} d$`, revenus : `{idleJson["patates"]["revenus"]} d$/h`)\n- :corn: Champ de maïs (prix : `{idleJson["mais"]["prix"]} d$`, revenus : `{idleJson["mais"]["revenus"]} d$/h`, débloquage : `{idleJson["mais"]["unlock"]} d$`)\n- :carrot: Champ de carrotes (prix : `{idleJson["carrotes"]["prix"]} d$`, revenus : `{idleJson["carrotes"]["revenus"]} d$/h`, débloquage : `{idleJson["carrotes"]["unlock"]} d$`\n- :hatching_chick: Poulailler (prix : `{idleJson["poulailler"]["prix"]} d$`, revenus : `{idleJson["poulailler"]["revenus"]} d$/h`, débloquage : `{idleJson["poulailler"]["unlock"]} d$`)', color=0xababab)
            embed.set_author(name='Bienvenue dans le IDLE, ' + message.author.name + ' !')
            embed.set_footer(text= f'Pour jouer, vous devez avoir de l\'argent ! Vous pouvez dans ce jeu acheter des propriétées afin de faire du revenu ! Pour afficher cette fenêtre, faites {config["prefix"]}idle help')
            await message.channel.send(embed=embed)

        else :
            if texte.startswith('buy') :
                texte = texte[4:len(texte)]
                if texte.startswith('🥔') or texte.startswith('🌽') or texte.startswith('🥕') or texte.startswith('🐣'):
                    for emoji,item in {'🥔':'patates','🌽':'mais','🥕':'carrotes','🐣':'poulailler'}.items() :
                        if texte.startswith(emoji) :
                            choix = item
                    texte = texte[2:len(texte)]
                    try :
                        texte = int(texte)
                    except :
                        await message.channel.send('Veuillez inclure un chiffre entier pour procéder à l\'achat. Plus d\'infos avec **' + config['prefix'] + 'idle help**.')
                    else :
                        if (userData[choix] + texte) > 50:
                            if userData[choix] >= 50 :
                                await message.channel.send(f'Désolé, vous avez déja atteints la limite de {choix}.')
                            else :
                                texte = 50 - userData[choix]
                                await message.channel.send(f'On ne peut acheter que 50 fois une propriété, ducoup vous ne pouvez en acheter que {texte}.')
                        else :
                            if userData['money'] >= texte * idleJson[choix]['prix'] :
                                if (userData[choix] != 0) or (idleJson[choix]['unlock'] == 0) :
                                    userData['money'] -= texte * idleJson[choix]['prix']
                                    userData[choix] += texte
                                    await message.channel.send('Achat effectué de **' + str(texte) + ' ' + choix + '**.')
                                else :
                                    await message.channel.send('Désolé, vous devez d\'abord débloquer cette catégorie. Faites **' + config['prefix'] + 'idle help** pour plus d\'infos.')
                            else :
                                await message.channel.send('Vous n\'avez pas assez pour acheter **' + str(texte) + ' ' + choix + '**. Vous possedez actuellement **' + str(userData['money']) + ' d$**. Il vous manque donc **' + str((texte * idleJson[choix]['prix'])-userData['money']) + ' d$**')
                else :
                    await message.channel.send('La commande d\'achat est invalide. Plus d\'infos avec **' + config['prefix'] + 'idle help**.')
            
            elif texte.startswith('unlock') :
                texte = texte[7:len(texte)]
                if texte.startswith('🥔') or texte.startswith('🌽') or texte.startswith('🥕') or texte.startswith('🐣'):
                    for emoji,item in {'🥔':'patates','🌽':'mais','🥕':'carrotes','🐣':'poulailler'}.items() :
                        if texte.startswith(emoji) :
                            choix = item
                    texte = texte[2:len(texte)]
                    if userData['money'] >= idleJson[choix]['unlock'] :
                        if userData[choix] == 0:
                            userData['money'] -= idleJson[choix]['unlock']
                            userData[choix] += 1
                            await message.channel.send('Vous avez débloqué **' + choix + '** !')
                        else :
                            await message.channel.send('Désolé, vous avez déjà débloqué cette catégorie. Faites **' + config['prefix'] + 'idle help** pour plus d\'infos.')
                    else :
                        await message.channel.send('Vous n\'avez pas assez pour débloquer **' + choix + '**. Vous possedez actuellement **' + str(userData['money']) + ' d$**. Il vous manque donc **' + str(idleJson[choix]['unlock'] - userData['money']) + ' d$**')
                else :
                    await message.channel.send('La commande de débloquage est invalide. Plus d\'infos avec **' + config['prefix'] + 'idle help**.')
            
            elif texte.startswith('upmaxtime'):
                if texte.startswith('upmaxtime buy') :
                    if userData['money'] >= (2**(userData["idleMaxTime"]-idleJson["afklesstime"])*100):
                        userData['money'] -= 2**(userData["idleMaxTime"]-idleJson["afklesstime"])*100
                        userData['idleMaxTime'] += 1
                        await message.channel.send(f'Achat d\'une heure d\'absence en plus réussie : `{2**(userData["idleMaxTime"]-idleJson["afklesstime"])*100} d$`. Vous pouvez maintenant vous absenter `{userData["idleMaxTime"]}h`. La prochaine coûtera : `{2**(userData["idleMaxTime"]-idleJson["afklesstime"]+1)*100} d$`.')
                    else :
                        await message.channel.send(f'Vous n\'avez pas assez d\'argent pour acheter une heure supplémentaire. Vous avez besoin de `{2**(userData["idleMaxTime"]-idleJson["afklesstime"])*100} d$`.')
                else :
                    await message.channel.send(f'Prix d\'une heure d\'absence en plus : `{2**(userData["idleMaxTime"]-idleJson["afklesstime"])*100} d$`.\nPour acheter, faites `{config["prefix"]}upmaxtime buy`.')

            openFile(usersFiles,str(message.author.id),'w',userData)

            arguments = '- :potato: Champ de patate : `' + str(userData['patates']) + '` , revenus : `' + str(idleJson['patates']['revenus'] * userData['patates']) + ' d$/h`'
            revenus = idleJson['patates']['revenus'] * userData['patates']
            for item,emoji in {'mais':'\n- :corn: ','carrotes':'\n- :carrot: ','poulailler':'\n- :hatching_chick: '}.items() :
                if userData[item] > 0 :
                    if item == 'poulailler' :
                        arguments += emoji + ' Poulailler : `' + str(userData[item]) + '` , revenus : `' + str(idleJson[item]['revenus'] * userData[item]) + ' d$/h`'
                    else :
                        arguments += emoji + 'Champ de ' + item + ' : `' + str(userData[item]) + '` , revenus : `' + str(idleJson[item]['revenus'] * userData[item]) + ' d$/h`'
                    revenus += idleJson[item]['revenus'] * userData[item]
                else :
                    arguments += '\n- :no_entry_sign: **Bloqué** - débloquage : **' + str(idleJson[item]['unlock']) + ' d$**'

            derniereconnexion = userData['derniereconnexion']
            derniereconnexion = datetime(int(derniereconnexion[0:4]), int(derniereconnexion[5:7]), int(derniereconnexion[8:10]), int(derniereconnexion[11:13]), 0, 0)
            derniereconnexion = ((derniereconnexion.year-1)*365 + mois(derniereconnexion.month) + (derniereconnexion.day-1))*24 + derniereconnexion.hour
            mtn = datetime.now()
            mtn = ((mtn.year-1)*365 + mois(mtn.month) + (mtn.day-1))*24 + mtn.hour
            absence = mtn-derniereconnexion
            if str(absence) != '0' :
                if absence > userData['idleMaxTime']:
                    absence = userData['idleMaxTime']
                    await message.channel.send(f'Vous avez été absent pendant `{mtn-derniereconnexion}h` ! Malheuresement, vous ne pouvez récupérer que les revenus des `{userData["idleMaxTime"]} dernières heures`.\nVous avez donc gagné `{revenus*absence} d$`')
                else :
                    await message.channel.send(f'Vous avez été absent pendant `{absence}h` !\nVous avez donc gagné `{revenus*absence} d$`')
                userData['money'] += revenus*absence
                userData['derniereconnexion'] = str(datetime.now())
            
            openFile(usersFiles,str(message.author.id),'w',userData)

            embed = discord.Embed(title='Liste des propriétées :', description=arguments + '\n\n**Argent :** `' + str(userData['money']) + ' d$`\n**Revenus :** `' + str(revenus) + ' d$/h`\n**Temps d\'absence max :** `' + str(userData['idleMaxTime']) + 'h`', color=0xababab)
            embed.set_author(name='IDLE - ' + message.author.name)
            embed.set_footer(text= 'Faites ' + config['prefix'] + 'idle help pour plus d\'infos')
            await message.channel.send(embed=embed)

    if commande(config['prefix']) :
        message.content = message.content[len(config['prefix'])::]

        for cle,valeur in commandes.items():
            if commande(cle):
                await message.channel.send(valeur)

        if commande('counter'): #compte le nombre de caractères du message
            alphabet="abcdefghijklmnopqrstuvwxyz0123456789éèêëàâäôöîïùûüç!\"#$%&'()*+,-./0123456789:;<=>?@[]^_`{|}~"
            texte = ''
            for i in range(len(alphabet)):
                if alphabet[i] in message.content[8::] :
                    texte += f'**{alphabet[i]}** est présent `{message.content[7::].count(alphabet[i])} fois` !\n'
            await message.channel.send(embed=discord.Embed(title=f'"{message.content[8::]}"', description=texte, color = 0x0088ff).set_author(name="Liste des caractères dans :"))

        if commande('issou'): #issou
            await message.delete() 
            await message.channel.send('https://tenor.com/view/risitas-main-dent-issou-laugh-gif-9505807')

        if commande('commande') : #Permet de faire de nouvelles commandes
            if message.content == 'commande' :
                await message.channel.send('Désolé, mais il faut un nom et un texte pour créer une commande.')
            elif message.content == 'commande del' :
                await message.channel.send('Désolé, mais il faut indiquer la commande à supprimer.')
            elif message.content.split()[1] == 'del' :
                try :
                    del commandes[message.content.split()[2]]
                except :
                    await message.channel.send(f'Désolé, la commande `{config["prefix"]}{message.content.split()[2]}` n\'existe pas...')
                else :
                    await message.channel.send(f'Commande `{config["prefix"]}{message.content.split()[2]}` enlevée avec succès !')
            elif len(message.content) > 300 : 
                await message.channel.send('Désolé, trop de caractères...')
            else :
                if message.content.split()[1] not in commandes.keys() :
                    commandes[message.content.split()[1]] = message.content[len(message.content.split()[0])+len(message.content.split()[1])+2::]
                    arguments = f'Commande `{config["prefix"]}{message.content.split()[1]}` bien ajoutée !'
                    await message.channel.send(arguments)
                else :
                    await message.channel.send(f'Désolé, la commande `{config["prefix"]}{message.content.split()[1]}` existe déjà...')
            openFile(mainFiles,'commandes','w',commandes)

        if commande('score'): #affiche le score d'un joueur
            username = message.content[9:-1]

            if username == '' :
                userData = openFile(usersFiles,str(message.author.id),'r',0)
                if userData['games'] == 0 :
                    await message.channel.send(f'Tu possède `{userData["money"]}` d$ !')
                else :
                    await message.channel.send(f'Au **chifoumi**, tu as un score de `{str(userData["wins"]/userData["games"]*100)[0:4]}`% ! Sur `{userData["games"]}` parties jouées, tu en as gagné `{userData["wins"]}` !\nEt tu possèdes `{userData["money"]}` d$ !')

            elif (username + ('.json')) in os.listdir(usersFiles) :
                userData = openFile(usersFiles,username,'r',0)
                if userData['games'] == 0 :
                    await message.channel.send(f'Le joueur possède `{userData["money"]}` d$ !')
                else :
                    await message.channel.send(f'Au **chifoumi**, le joueur **{client.get_user(int(username)).name}** à un score de `{str(userData["wins"]/userData["games"]*100)[0:4]}`% ! Sur `{userData["games"]}` parties jouées, il en a gagné `{userData["wins"]}` !\nEt il possède `{userData["money"]}` d$ !')
            else :
                await message.channel.send('Je ne connais pas ce joueur')

        if commande('ascii'): #tranforme du texte en ascii
        
            texte = message.content[6::]

            fontList = ['cybermedium','bubble','block','small','block','white_bubble','random-small','random-medium','random-large','random-xlarge','random','magic']
            arguments = 0

            for i in range(len(fontList)) :
                if texte.startswith(fontList[i]) :
                    texte = texte[len(fontList[i]) + 1::]
                    arguments = '```' + text2art(texte, font=fontList[i]) + '```'
            if arguments == 0 :
                arguments = '```' + text2art(texte) + '```'


            if len(arguments) <= 2000 :
                if texte == '' :
                    await message.channel.send('Rajoue du texte après le \'!ascii\' pour que j\'affiche un résultat. \nTu peux aussi écrire avec différentes polices. Pour ce faire, rajoute \'cybermedium\', \'bubble\', \'block\', \'small\', \'block\', \'white_bubble\', \'random\', \'random-small\', \'random-medium\', \'random-large\', \'random-xlarge\' ou \'magic\' après le \'!ascii\'.')
                else :
                    await message.channel.send(arguments)
            else :
                await message.channel.send('Désolé, la phrase est trop grande')
        
        if commande('prefix') : #Sert a changer le prefix des commandes
            if message.content[7::] == '' :
                await message.channel.send('Pour changer le prefix, veuillez le mettre à la suite de la commande.')
            else :
                config['prefix'] = message.content[7::]
                openFile(mainFiles,'config','w',config)
                await message.channel.send(f'Le prefix à bien été changé pour `{config["prefix"]}` !')

        if commande('bug') : #Sert a prévenir l'admin d'un bug
            if message.channel.type is discord.ChannelType.private:
                embed = discord.Embed(title =f'[MP] | id : `{message.author.id}`', description = f'message : `{message.content[4::]}`', color = 0xff0000)
            else :
                embed = discord.Embed(title =f'[{message.guild}] #{message.channel} | id : `{message.author.id}`', description = f'message : `{message.content[4::]}`', color = 0xff0000)

            embed.set_author(name='Bug signalé par ' + message.author.name)
            await owner.send(embed = embed)

            await message.channel.send('Message envoyé ! Merci de ton aide ^^')

        if commande('announceChannel') : #dis quel est le salon de bienvenue des nouveaux membres
            if message.content == (message.content).split()[0] :
                if server['welcome'] == message.channel.id :
                    await message.channel.send(f'Le salon <#{client.get_channel(server["welcome"]).id}> est déjà le salon d\'annonce')
                else :
                    server['welcome'] = message.channel.id
                    await message.channel.send(f'Le salon <#{client.get_channel(server["welcome"]).id}> est maintenant le salon d\'annonce')
                    openFile(serverFiles,'server','w',server)

            elif (message.content).split()[1] == 'del':
                if server['welcome'] == None :
                    await message.channel.send('Le salon d\'annonce à déjà été supprimé')
                else :
                    await message.channel.send('Salon d\'annonce bien supprimé')
                    server['welcome'] = None
                    openFile(serverFiles,'server','w',server)

            else :
                try :
                    if server['welcome'] == ((message.content).split()[1])[2:-1] :
                        await message.channel.send(f'Le salon <#{client.get_channel(server["welcome"]).id}> est déjà le salon d\'annonce')
                    else :
                        server['welcome'] = int(((message.content).split()[1])[2:-1])
                        await message.channel.send(f'Le salon <#{client.get_channel(server["welcome"]).id}> est maintenant le salon d\'annonce')
                        openFile(serverFiles,'server','w',server)
                except :
                    await message.channel.send('Veuillez entrer un salon valide')

        if commande('ping') : #Permet de recupérer le ping d'un site par exemple
            message.content = message.content[5::]

            if message.content == '' or  message.content == 'localhost' or  message.content ==  '127.0.0.1' or  message.content == '0.0.0.0':
                await message.channel.send(f'Ma latence est actuellement de {round(client.latency*1000)}ms !')
            elif ping(message.content) :
                if message.content[0] in '0123456789' :
                    message.channel.send(f'Le système {message.content} est bien connecté !')
                else :
                    message.channel.send(f'Le système https://{message.content} est bien connecté !')
            else :
                await message.channel.send(f'Le système {message.content} est déconnecté...')

        if commande('bye') : #bye les boi
            if message.author.id == owner.id :
                await message.channel.send(f'Je me déco à la demande de **{message.author.name}**')
                await client.close()
            else :
                await message.channel.send('Tu n\'as pas la permission')

        if commande('give') : #permet à un drawbu de give de l'argent
            if message.author.id == owner.id :
                texte = message.content[5::]
                try :
                    texte = int(texte)
                except :
                    await message.channel.send('Ce n\'est pas une valeur correcte')
                else :
                    userData['money'] += texte
                    openFile(usersFiles,str(message.author.id),'w',userData)
                    await message.channel.send(f'Don de `{texte} d$`') 
            else :
                await message.channel.send('Vous n\'avez pas la permission')

        if commande('serverInfos') : #infos sur le bot
            message.content = message.content[12::]

            if message.channel.type is discord.ChannelType.private:
                await message.channel.send('Désolé, pas en MP')

            else :
                print(f'"{message.content}"')
                if commande('memList') :
                    membres = ''
                    for i in message.guild.members :
                        membres += (f'{i.name}\n')
                    
                    await message.channel.send(embed=discord.Embed(title=message.guild.name, description=f'**Liste des membres ({message.guild.member_count}) :**\n{membres}').set_thumbnail(url=f'{message.guild.icon_url}'))
                

                elif commande('user') :
                    user = ''

                    if message.content == 'user' :
                        user = client.get_user(message.author.id)

                    else :
                        try :
                            user = int(message.content[8:26])
                            user = client.get_user(user)
                        except :
                            await message.channel.send('Je ne connais pas ce joueur')
                    
                    if user != '' :
                        if message.guild.owner.id == user.id :
                            attribut  = 'Propriétaire'
                        elif user.bot == True :
                            attribut  = 'Bot'
                        else :
                            attribut = 'Membre'

                        await message.channel.send(embed=discord.Embed(title=f'{user.name} - {attribut}', description=f'**id :** `{user.id}`').set_thumbnail(url=f'{user.avatar_url}'))

                else :
                    await message.channel.send(embed=discord.Embed(title=message.guild.name, description=f'Le serveur compte aujourd\'hui `{message.guild.member_count} membres`. \nLe propriétaire est `{message.guild.owner.name}`.\n\n**Commandes :**\n`{config["prefix"]}serverInfos memList` : Affiche la liste des membres d\'un serveur.\n`{config["prefix"]}user` : Affiche tes infos sur le serveur.\n`{config["prefix"]}serverInfos user <@membre>` : Affiche les infos d\'un membre du serveur').set_thumbnail(url=f'{message.guild.icon_url}'))

        if commande('classement') : #classement des joueurs
            users = os.listdir(usersFiles)
            usersDict = {}
            for i in range(len(users)) :
                usersDict[client.get_user(int(users[i][0:18])).name] = int(openFile(usersFiles, users[i][0:18], 'r', 0)["money"])
            texte = ''
            users = 0
            for r in sorted(usersDict, key=usersDict.get, reverse=True) : 
                users += 1
                if users != 11 :
                    texte += f'**{users} :** *{r}* : `{usersDict[r]} d$`\n'
                else :
                    break
            embed=discord.Embed(title="Classement des fortunes", description=texte, color=0x0088ff)
            await message.channel.send(embed=embed)

        if commande('cat') : #affiche une image de chat aléatoire
            if commande('cat help') :
                embed=discord.Embed(description=f'Image générée par le site https://thiscatdoesnotexist.com.\nFaites `{config["prefix"]}cat` pour affiche une image d\'un chat **qui n\'existe pas** et qui est generé grace à une Intelligence Artificielle.', color=0x009dff)
                embed.set_author(name=f'Aide pour la commande {config["prefix"]}cat :', icon_url='https://thiscatdoesnotexist.com/')
                await message.channel.send(embed=embed)
            else :
                await message.channel.send('Veuillez patienter, c\'est en cours !', delete_after=3.0)
                urllib.request.urlretrieve('https://thiscatdoesnotexist.com/','cat.png')
                with open('cat.png', 'rb') as picture: 
                    await message.channel.send(file=discord.File(picture))

        if commande('test') : #test 
            await client.change_presence(activity=discord.Activity(name='issou'))

    if commande('!prefix reset') : #Sert à reset le prefix quel qu'il soit
        config['prefix'] = '!'
        openFile(mainFiles,'config','w',config)
        await message.channel.send('Le prefix a bien été changé pour "!"')

@tasks.loop(seconds=300)
async def devoirs_pronote():

    if datetime.now().hour not in [22,23,0,1,2,3,4,5] :
        filesDir = './'
        configPronote = verifyFile(filesDir, 'pronote', {'username':None,'password':None,'folderName': None, 'channelID': None, 'url': None})
        if configPronote['username'] != None and configPronote['password'] != None and configPronote['url'] != None:
            pronote = pronotepy.Client(configPronote['url'], username=configPronote['username'], password=configPronote['password'])
            
            if configPronote['folderName'] != None :
                createDir(configPronote['folderName'])
                filesDir += f'{configPronote["folderName"]}/'

            if (pronote.logged_in and (configPronote['channelID'] != None)):
                devoirs = pronote.homework(pronote.start_day, pronote.start_day + pronotepy.datetime.timedelta(days=360))
                devoirsFile = verifyFile(filesDir, 'devoirs', {})
                devoirsList = []
                for i in devoirs :
                    description = i.description.replace('\n', ' ')
                    devoirsList.append(f'{i.date} : {i.subject.name} {description}')

                if len(devoirsList) > len(devoirsFile) :
                    devoirsNewNbr = len(devoirsList) - len(devoirsFile)
                    print(f'{devoirsNewNbr} nouveaux devoirs !')
                    pronoteChannel = client.get_channel(configPronote['channelID'])
                    for i in range(devoirsNewNbr) :
                        embed=discord.Embed(title=devoirs[len(devoirsFile)+i].subject.name, description=devoirs[len(devoirsFile)+i].description.replace('\n', ' '), color=0x1E744F)
                        embed.set_author(name=f'Pour le {devoirs[len(devoirsFile)+i].date}')
                        await pronoteChannel.send(embed=embed)
                    openFile('./', 'devoirs', 'w', devoirsList)

client.run(token)