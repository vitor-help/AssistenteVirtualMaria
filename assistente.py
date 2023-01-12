from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import os
import sys
from datetime import datetime
import wikipedia
from requests import get
import spotipy
import webbrowser

def criar_audio(audio, mensagem):
    tts = gTTS(mensagem, lang="pt-br")
    tts.save(audio)
    playsound(audio)
    os.remove(audio)

def reconhecer_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga algo!")
        audio = r.listen(source)
        try:
            mensagem = r.recognize_google(audio, language = "pt-br")
            mensagem = mensagem.lower()
            print("Você disse " + mensagem)
            return mensagem
        except sr.UnknownValueError:
            print("Maria não entendeu o áudio")
            return ""
        except sr.RequestError as e:
            print("Não foi possível obter uma resposta da Maria {0}".format(e))
            return ""

def chamar_comando(mensagem):
    mensagem = mensagem.replace("maria", "")
    if "qual o seu nome" in mensagem: criar_audio("audios/nome.mp3", "Meu nome é Maria")
    if "adeus" in mensagem: fechar_assistente()
    if "horas" in mensagem: horas()
    if "pesquise" in mensagem: pesquisar_wikipedia(mensagem)
    if "dólar" in mensagem: cotacao("USD")
    if "euro" in mensagem: cotacao("EUR")
    if "tocar" in mensagem: spotify(mensagem)

def fechar_assistente():
    criar_audio("audios/fechar_assitente.mp3", "Até logo!")
    sys.exit()

def horas():
    horas = datetime.now().strftime("%H:%M")
    criar_audio("audios/horas.mp3", "Agora são {}".format(horas))

def pesquisar_wikipedia(mensagem):
    mensagem = mensagem.replace("pesquise", "")
    wikipedia.set_lang("pt")
    resultado = wikipedia.summary(mensagem, sentences=2)
    criar_audio("audios/pesquisa.mp3", "De acordo com a Wikipedia, {}".format(resultado))

def cotacao(moeda):
    requisicao = get("https://economia.awesomeapi.com.br/all/{}-BRL".format(moeda))
    resultado = requisicao.json()
    nome = resultado[moeda]["name"]
    data = resultado[moeda]["create_date"]
    valor = resultado[moeda]["bid"]
    criar_audio("audios/cotacao.mp3", "Cotação do {} em {} é {}".format(nome, data, valor))

def spotify(mensagem):

    #credinciais
    spotify_details = {
        "client_id": "583ab1b26749429cb32bb856a2357a67",
        "client_secret": "e6b11df42bee4a7d82b1323b3a46efa5",
        "redirect_uri": "https://beacons.ai/rafaballerini"}

    try:
        sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(client_id=spotify_details['client_id'], client_secret=spotify_details['client_secret'], redirect_uri=spotify_details['redirect_uri'], open_browser=False))        
    except:
        print("token sem acesso")

    mensagem = mensagem.replace("tocar", "")
    resultado = sp.search(mensagem, 1, 0, "track")
    musica_dict = resultado["tracks"]
    musica_items = musica_dict["items"]
    musica_url = musica_items[0]["external_urls"]["spotify"]
    webbrowser.open(musica_url)

def main():
    criar_audio("audios/iniciar_assistente.mp3", "Olá eu sou a Maria, em que posso ajudar?")
    while True:
        mensagem = reconhecer_audio()
        if mensagem != "" and "maria" in mensagem: chamar_comando(mensagem)

main()