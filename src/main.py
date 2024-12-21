from pydub import AudioSegment
import speech_recognition as sr
import webvtt
import os
from googletrans import Translator


input_mov_path = "input.mov"  #เปลี่ยนชื่อไฟล์ให้ตรงกับ Video .mp .mov


def extract_audio_from_mov(input_mov, output_wav):
    from moviepy.editor import AudioFileClip
    audio = AudioFileClip(input_mov)
    audio.write_audiofile(output_wav)
    print(f"Audio extracted to {output_wav}")

def convert_wav_to_vtt(input_wav, output_vtt, segment_duration=5):
    audio = AudioSegment.from_wav(input_wav)
    duration = len(audio)  

    recognizer = sr.Recognizer()
    vtt = webvtt.WebVTT()

    segment_start = 0
    segment_id = 1

    while segment_start < duration:
        segment_end = min(segment_start + segment_duration * 1000, duration)
        audio_segment = audio[segment_start:segment_end]

        segment_file = "temp_segment.wav"
        audio_segment.export(segment_file, format="wav")

        with sr.AudioFile(segment_file) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language="th-TH")
            except sr.UnknownValueError:
                text = "[Unrecognized Speech]"
            except sr.RequestError as e:
                print(f"Error recognizing speech: {e}")
                text = "[Error]"

        start_time = format_time(segment_start)
        end_time = format_time(segment_end)
        vtt_caption = webvtt.Caption(start_time, end_time, text)
        vtt.captions.append(vtt_caption)

        segment_start = segment_end
        segment_id += 1

        os.remove(segment_file)

    vtt.save(output_vtt)
    print(f"VTT file saved as {output_vtt}")

def translate_vtt(input_vtt, output_vtt_en):
    translator = Translator()
    vtt = webvtt.read(input_vtt)

    for caption in vtt.captions:
        translated_text = translator.translate(caption.text, src='th', dest='en').text
        caption.text = translated_text

    vtt.save(output_vtt_en)
    print(f"English VTT file saved as {output_vtt_en}")

def format_time(milliseconds):
    total_seconds = milliseconds // 1000
    milliseconds = milliseconds % 1000
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

output_wav_path = "output.wav"
output_vtt_path = "output.vtt"
output_vtt_en_path = "output_en.vtt"

extract_audio_from_mov(input_mov_path, output_wav_path)

convert_wav_to_vtt(output_wav_path, output_vtt_path, segment_duration=10)

translate_vtt(output_vtt_path, output_vtt_en_path)
