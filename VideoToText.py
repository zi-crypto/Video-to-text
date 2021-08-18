import subprocess
import os
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from google_trans_new import google_translator

print("***************************************************************")
print("---------------- Welcome To Youtube Transcriber ---------------")
print("***************************************************************")

apikey = "b7A6O44nNbk-CYhWrK_Z8IUHAz5XAoDAChTuBPohTBT1"
url = "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/5ded1a17-8e04-43b5-b127-8375e8b52026"

video_url = str(input("Enter The Video URL (from YouTube): "))
transcribe_language = str(input("Enter The Transcribe Language 'with language fromats from https://cloud.ibm.com/docs/speech-to-text?topic=speech-to-text-models': "))
download_video = 'youtube-dl --extract-audio --audio-format mp3 -o "audio.%(ext)s" "{}"'.format(video_url)
subprocess.call(download_video, shell=True)

authenticator = IAMAuthenticator(apikey)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(url)

command = 'ffmpeg -i audio.mp3 -f segment -segment_time 360 -c copy %03d.mp3'
subprocess.call(command, shell=True)

files = []
for filename in os.listdir('.'):
    if filename.endswith(".mp3") and filename != 'audio.mp3':
        files.append(filename)
files.sort()

results = []
for filename in files:
    with open(filename, 'rb') as f:
        res = stt.recognize(audio=f, content_type='audio/mp3', model=transcribe_language, continuous=True,
                            inactivity_timeout=600).get_result()
        results.append(res)

text = []
for file in results:
    for result in file['results']:
        text.append(result['alternatives'][0]['transcript'].rstrip() + '.\n')

with open('output.txt', 'w') as out:
    out.writelines(text)

print("Done!!")
print("Your Transcription is in output.txt!!")

yorntranslate = str(input("Do you want to Translate The Transcription (y/n)?"))
if yorntranslate == "y":
    translator = google_translator()
    target_language = str(input("Which Language To Translate To '{'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu', 'fil': 'Filipino', 'he': 'Hebrew'}':"))
    with open("output.txt", "r") as t:
        file_text = t.readlines()
    result = translator.translate(
        file_text, lang_src=transcribe_language, lang_tgt=target_language)
    with open("output_translated.txt", "w") as to:
        to.write(result)
    print("Translated!")

elif yorntranslate == "n":
    print("OK!")

else:
    print("Abort.")

print("Good Bye!")
