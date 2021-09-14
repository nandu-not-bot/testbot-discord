from googletrans import Translator

detector = Translator()

dec_lan = detector.translate('Hello World!', dest="ja")

print(dec_lan.text)