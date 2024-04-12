from pydub import AudioSegment  
import speech_recognition as sr
import os

def convert(debug=False):
    input_file = "ogg_voice.ogg"
    output_file = "converted_voice.mp3"
    try:
        ogg_audio = AudioSegment.from_file(input_file, format="ogg")
        ogg_audio.export(output_file, format="WAV")
        if debug:
            print("SUCCESS Голосовое успешно переведено в mp3")
        return output_file 
    except Exception as e:
        if debug:
            print("ERROR", f"An error occurred during conversion: {e}")
        return None


def convert_mp3_to_text(mp3_file,debug=False):
    recognizer = sr.Recognizer()

    with sr.AudioFile(mp3_file) as source:
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data, language='ru-RU')
            if debug: print('SUCCESS Успешно mp3_to_text')
            print('try')
            return text
        except sr.UnknownValueError:
            if debug:
                print("ERROR Google Web Speech API не смог распознать аудио")
            return None
        except sr.RequestError as e:
            if debug:
                print("ERROR Ошибка при запросе к Google Web Speech API - {0}".format(e))
            return None
        except Exception as e:
            if debug:
                print(f'ERROR Ошибка в модулe mp3_to_text : {e}')
            return None


def from_ogg_to_text(debug=False):
    mp3_file_path = convert(debug)
    
    try:
        if  mp3_file_path is not None:
            print(mp3_file_path)
            text = convert_mp3_to_text(mp3_file_path, debug)
            os.remove(mp3_file_path)
            
            if text is not None: 
                if debug: print('SUCCESS Голосовое успешно переведено в текст и временный файл удален')
                return text
            else: 
                if debug:
                    print('ERROR Пустое сообщение или ошибка распознания')
                return "Пустое сообщение или ошибка распознания"
        else: return  'Ошибка конвертации звука в текст'
    except Exception as e:
        print('else')
        if debug:
            print(f'ERROR Ошибка функции from_ogg_to_text : {e}')


    


