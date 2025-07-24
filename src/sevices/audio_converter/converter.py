import os
import subprocess

import speech_recognition as sr


class Converter:

    def __init__(self, path_to_file: str, language: str = "ru-RU"):
        self.language = language
        self.wav_file = path_to_file.replace(".ogg", ".wav")

    def audio_to_text(self) -> str:
        self._audio_to_wav()
        r = sr.Recognizer()
        with sr.AudioFile(self.wav_file) as source:
            audio = r.record(source)
            r.adjust_for_ambient_noise(source)

        return r.recognize_google(audio, language=self.language)

    def _audio_to_wav(self):
        """Конвертация аудио файла из ogg в wav"""
        subprocess.run(
            ["ffmpeg", "-v", "quiet", "-i", self.wav_file.replace(".wav", ".ogg"), self.wav_file]
        )
    # def _audio_to_wav(self):
    #     """Конвертация аудио файла из ogg в wav"""
    #     subprocess.run(
    #         ["/opt/homebrew/bin/ffmpeg", "-v", "quiet", "-i", self.wav_file.replace(".wav", ".ogg"), self.wav_file]
    #     )

    def __del__(self):
        os.remove(self.wav_file)
        os.remove(self.wav_file.replace(".wav", ".ogg"))
