from telegram.ext import CommandHandler, Updater
import requests
import json
import random
from urllib.request import urlopen
import urllib.parse
import datetime
from unidecode import unidecode
import USCrimes
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TOKEN")
SENT_1 = os.getenv("SENT_1")
SENT_2 = os.getenv("SENT_2")
N_MSGS_FWD = 150
URL_ANALISE = "https://api.gotit.ai/NLU/v1.4/Analyze"
HEADERS = {'Content-Type': 'application/json'}
PAYLOAD_ANT = "{ 'T': '"
PAYLOAD_DEP = "', 'SL': 'PtBr', 'EM': true }"

PAISES = urlopen("https://raw.githubusercontent.com/datasets/country-list/master/data.csv").read().decode('utf-8').split("\n")
PAISES_TAM = len(PAISES)
POPULACOES = urlopen("https://raw.githubusercontent.com/datasets/population/master/data/population.csv").read().decode('utf-8').split("\n")[2715:]
POPULACOES.reverse()
POPULACOES_TAM = len(POPULACOES)

def sendRedditImg(bot, update, sub, arq, msgError):
    try:
        arqAp = open("./Posts/{}.csv".format(arq), "a+")
        postsArq = open("./Posts/{}.csv".format(arq), "r")
        postsUsados = postsArq.read().splitlines()
        postsArq.close()
        urlReddit = "https://www.reddit.com/r/{}.json?sort=hot".format(sub)
        resp = requests.request(method="GET", url=urlReddit, headers={'User-agent': 'ocramoidev'})
        respPosts = json.loads(resp.text)["data"]["children"]
        flag = True
        for post in respPosts:
            if (not(str(hash("{}{}".format(post["data"]["id"], update.message.chat_id))) in postsUsados)) and ((".jpg" in post["data"]["url"]) or (".png" in post["data"]["url"])):
                bot.sendPhoto(
                    chat_id=update.message.chat_id,
                    photo=post["data"]["url"]
                )
                flag = False
                arqAp.write(str(hash("{}{}".format(post["data"]["id"], update.message.chat_id))) + "\n")
                break
        if flag:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=msgError
            )
    except Exception as e:
        print(str(e))
        bot.send_message(
            chat_id=update.message.chat_id,
            text=msgError
        )

def liberals(bot, update):
    sendRedditImg(bot, update, "ToiletPaperUSA", "tpusa", "female orgasm is a liberal hoax")

def surreal(bot, update):
    sendRedditImg(bot, update, "surrealmemes", "surreal", "S̶̢̭͎̣̠͎̬̩̣̬͚̤̤̣͌̓͋̄̊̾̉͋̃̚U̵͚̬͓̺̗̠̲̮̦̟͚̗̣͌̿̽͗̾̂͆̕̕͜͝͝ͅŖ̸͇̼̮̪̤̤͖̗̼̺̻́̄̐̍̚R̴̢̛̤̪̗̦̦͔̜̯̒̇́̆̍̏̚̚͝͠ͅͅE̶̡̡̦̠̮̘͌̓̇̋͑̈́̓̆͗̆̏̋́͒͠A̷̧̘̦̞͚̤̦͎͍̱͕̯͑̓̽͗̄̏̅̀̅͜L̴̩̫̥̜̈́͂̍̊̽̈́̿͘͠")

def ooer(bot, update):
    sendRedditImg(bot, update, "Ooer", "ooer", "OOER")

def insta(bot, update):
    try:
        if len(update.message.text.split(" ")) == 2:
            link = update.message.text.split(" ")[1]
            sopa = BeautifulSoup(urlopen(link).read().decode("utf-8"), features="html.parser")
            bot.sendPhoto(
                chat_id=update.message.chat_id,
                photo=sopa.find("meta", property="og:image")['content'],
                caption=sopa.find("title").get_text()
            )
        elif len(update.message.text.split(" ")) == 1:
            link = update.message.reply_to_message["text"].split(" ")[0]
            sopa = BeautifulSoup(urlopen(link).read().decode("utf-8"), features="html.parser")
            bot.sendPhoto(
                chat_id=update.message.chat_id,
                photo=sopa.find("meta", property="og:image")['content'],
                caption=sopa.find("title").get_text()
            )
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="manda respondendo link ou manda o link junto"
            )
    except Exception as e:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="eta tenta de novo"
        )
        print(len(update.message.text.split(" ")), e)


def farid(bot, update):
    pais, sigla = PAISES[random.randint(1, PAISES_TAM - 1)].split(',')
    populacao = 0
    for linha in POPULACOES:
        if linha.split(',')[0] == pais:
            populacao = linha.split(',')[-1]
            break

    if populacao != 0:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="o Farid nasceu em {} [{}], com {} habitantes".format(pais, sigla, populacao)
        )
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="o Farid nasceu em {} [{}]".format(pais, sigla)
        )


def crimeAmericano(bot, update):
    try:
        if len(update.message.text.split(" ")) <= 1:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=USCrimes.randomCrime()
            )
            return
        pesquisa = update.message.text.split(" ")[1:]
        pesquisa = " ".join(pesquisa)
        res = USCrimes.searchCrime(pesquisa)
        if res != 0:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=res
            )
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="o único crime que os eua não cometeram é o que ce tá pesquisando :("
            )
    except Exception as e:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="o único crime que os eua não cometeram é o que ce tá pesquisando :(",
            disable_web_page_preview=False
        )
        print(e)


def gordineo(bot, update):
    sendRedditImg(bot, update, "fatcats", "postsGordineo", "kd os catto gordo")

def catto(bot, update):
    sendRedditImg(bot, update, "CatsStandingUp", "postsCatto", "kd os catto")

def ranpom(bot, update):
    try:
        bot.sendPhoto(
            chat_id=update.message.chat_id,
            photo="https://cdn.dicionariopopular.com/imagens/rom-pom-pom-mate-um-homem-man-down-og.jpg"
        )
    except Exception as e:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="MATE UM HOME"
        )
        print(str(e))


def cuti(bot, update):
    sendRedditImg(bot, update, "wholesomememes", "postsCuti", "sem cuti hoje :(")

def doubt(bot, update):
    try:
        bot.sendPhoto(
            chat_id=update.message.chat_id,
            photo="https://i.kym-cdn.com/entries/icons/facebook/000/023/021/e02e5ffb5f980cd8262cf7f0ae00a4a9_press-x-to-doubt-memes-memesuper-la-noire-doubt-meme_419-238.jpg"
        )
    except Exception as e:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="X -> Doubt"
        )
        print(str(e))


def respects(bot, update):
    try:
        bot.sendPhoto(
            chat_id=update.message.chat_id,
            photo="https://wompampsupport.azureedge.net/fetchimage?siteId=7575&v=2&jpgQuality=100&width=700&url=https%3A%2F%2Fi.kym-cdn.com%2Fentries%2Ficons%2Ffacebook%2F000%2F017%2F039%2Fpressf.jpg"
        )
    except Exception as e:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Press F to pay respects"
        )
        print(str(e))


def anarcho(bot, update):
    sendRedditImg(bot, update, "AnarchoWave", "postsAnarcho", "death to america")

def quarta(bot, update):
    if datetime.datetime.today().weekday() == 2:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="https://www.youtube.com/watch?v=du-TY1GUFGk",
            disable_web_page_preview=False
        )
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="It isn't wednesday my dudes :("
        )


def grito(bot, update):
    sendRedditImg(bot, update, "AAAAAAAAAAAAAAAAA", "postsGrito", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="CHUPA FEDERAL"
    )


def comandos(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="start - Inicia o bot\n"
             "fwd - Forward do @fwdbcc020\n"
             "sentimento - Analisa o sentimento contido na mensagem marcada\n"
             "stack - Uso:  <tag1 tag2 ... tagn>. Manda o primeiro resultado em atividade do stack overflow "
             "com as tags enviadas\n"
             "comandos - Envia os comandos do bot\n"
             "aaaa - AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\n"
             "quarta - Is it wednesday my dudes??\n"
             "anarcho - Don't compete\n"
             "f - Press F to pay respects\n"
             "doubt - X doubt\n"
             "cuti - Coisinha fofa pra esquecer a quarentena\n"
             "ranpom - MATE UM HOME\n"
             "cattosdipe - Gatinhos de pé\n"
             "cattosgordineos - Gatinhos gordineos\n"
             "crime - Retorna um crime cometido pelo governo americano :) <dá pra pesquisar termos também só mandar depois do comando>\n"
             "faridao - Onde o Farid nasceu mesmo?\n"
             "insta - Retorna as informações do post enviado\n"
             "ooer - NOW WITH 200k% MORE WEP!\n"
             "suuuuuuuu - memes may be difficult to understand for mere mortals\n"
             "dearliberals - comando oficial do TPUSA"
    )


def stack(bot, update):
    try:
        if len(update.message.text.split(" ")) <= 1:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="manda as tag junto"
            )
            return
        pesquisa = update.message.text.split(" ")[1:]
        pesquisa = ";".join(pesquisa)
        urlPesquisa = "".join(["https://api.stackexchange.com/2.2/questions?order=desc&sort=activity&tagged=",
                               urllib.parse.quote(unidecode(pesquisa)).replace("%3B", ";"),
                               "&site=stackoverflow&filter=!BHMIbze0EPheMk572h0kxuj.q(NQC*"])
        resp = requests.request(method="GET", url=urlPesquisa)
        respObj = json.loads(resp.text)
        bot.send_message(
            chat_id=update.message.chat_id,
            text="\n".join(["primeiro resultado man", respObj["items"][0]["link"]])
        )
    except Exception as e:
        if str(e) == "list index out of range":
            bot.send_message(
                chat_id=update.message.chat_id,
                text="tem nada com essas tag",
                disable_web_page_preview=False
            )
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="o stack ta me fudeno não dá pra mandar agora",
                disable_web_page_preview=False
            )
        print(e)


def fwd(bot, update):
    msg_id = random.randint(0, N_MSGS_FWD)
    try:
        bot.forwardMessage(update.effective_chat.id, -1001437873025, msg_id)
        print("Mensagem n{} enviada".format(msg_id))
    except Exception as e:
        print("{}. Msg n{}".format(str(e), msg_id))
        fwd(bot, update)


def sentimento(bot, update):
    try:
        origMsg = str(update.message.reply_to_message["text"])
        origMsg = origMsg.replace('"', "").replace("'", "").replace("\n", " ").replace("\r", " ").replace("\t", " ")
        payload = "".join([PAYLOAD_ANT, unidecode(origMsg), PAYLOAD_DEP])
        response = requests.request(method="POST", url=URL_ANALISE, headers=HEADERS, data=payload,
                                    auth=(SENT_1, SENT_2))
        respJson = json.loads(response.text)['emotions']
        arReps = [float(respJson["sadness"]), float(respJson["joy"]), float(respJson["fear"]), float(respJson["disgust"]),
                  float(respJson["anger"])]
        if respJson["sadness"] == respJson["joy"] == respJson["fear"] == respJson["disgust"] == respJson["anger"]:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="menino neutro"
            )
        else:
            maior = max(arReps)
            msgSent = ""
            if arReps.index(maior) == 0:
                msgSent = "sad boi"
            elif arReps.index(maior) == 1:
                msgSent = "happi boi"
            elif arReps.index(maior) == 2:
                msgSent = "ta caganu de medo"
            elif arReps.index(maior) == 3:
                msgSent = "ta com nojinho"
            elif arReps.index(maior) == 4:
                msgSent = "ta brabo"
            bot.send_message(
                chat_id=update.message.chat_id,
                text=msgSent
            )
    except Exception as e:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="tem que marca uma mensagem irmão tá doido"
        )
        print(e)


def main():
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(
        CommandHandler('start', start)
    )
    dispatcher.add_handler(
        CommandHandler('fwd', fwd)
    )
    dispatcher.add_handler(
        CommandHandler('sentimento', sentimento)
    )
    dispatcher.add_handler(
        CommandHandler('stack', stack)
    )
    dispatcher.add_handler(
        CommandHandler('comandos', comandos)
    )
    dispatcher.add_handler(
        CommandHandler('aaaa', grito)
    )
    dispatcher.add_handler(
        CommandHandler('quarta', quarta)
    )
    dispatcher.add_handler(
        CommandHandler('anarcho', anarcho)
    )
    dispatcher.add_handler(
        CommandHandler('f', respects)
    )
    dispatcher.add_handler(
        CommandHandler('doubt', doubt)
    )
    dispatcher.add_handler(
        CommandHandler('cuti', cuti)
    )
    dispatcher.add_handler(
        CommandHandler('ranpom', ranpom)
    )
    dispatcher.add_handler(
        CommandHandler('cattosdipe', catto)
    )
    dispatcher.add_handler(
        CommandHandler('cattosgordineos', gordineo)
    )
    dispatcher.add_handler(
        CommandHandler('crime', crimeAmericano)
    )
    dispatcher.add_handler(
        CommandHandler('faridao', farid)
    )
    dispatcher.add_handler(
        CommandHandler('insta', insta)
    )
    dispatcher.add_handler(
        CommandHandler('ooer', ooer)
    )
    dispatcher.add_handler(
        CommandHandler('suuuuuuuu', surreal)
    )
    dispatcher.add_handler(
        CommandHandler('dearliberals', liberals)
    )
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    print("Cancela na marra memo irmão")
    main()
