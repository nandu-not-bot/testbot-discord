from googletrans import Translator, LANGCODES

detector = Translator()

print(detector.translate("hello world", "ja"))