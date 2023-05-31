import tkinter as tk
from tkinter import filedialog 
from gtts import gTTS 
import pygame.mixer 
import os 
import librosa
import random
import customtkinter as ctk
import numpy as np
from pydub import AudioSegment
from pydub.effects import normalize, high_pass_filter, low_pass_filter
import matplotlib.pyplot as plt
import soundfile as sf
import time
from scipy import signal

pygame.mixer.init()
ctk.set_appearance_mode("dark")

playlist = []
current_song_index = 0
current_volume = 0.5  


def play_music():
    global current_song_index
    if not playlist:
        return
    pygame.mixer.music.load(playlist[current_song_index])
    pygame.mixer.music.play()
    plot_waveform()


def update_listbox():
    playlist_box.delete("0.0",ctk.END)
    for song in playlist:
        playlist_box.insert(ctk.END, os.path.basename(song))
        playlist_box.insert(ctk.END, "\n")
       
def pause_music():
    pygame.mixer.music.pause()

def resume_music():
    pygame.mixer.music.unpause()

def set_volume(volume):
    global current_volume
    current_volume = float(volume)
    pygame.mixer.music.set_volume(current_volume)

def select_files():
    file_paths = filedialog.askopenfilenames()
    playlist.extend(file_paths)
    update_listbox()
    if len(playlist) == len(file_paths):
        play_music()


def next_song():
    global current_song_index
    if not playlist:
        return
    current_song_index += 1
    if current_song_index >= len(playlist):
        current_song_index = 0
    play_music()

def previous_song():
    global current_song_index
    if not playlist:
        return
    current_song_index -= 1
    if current_song_index < 0:
        current_song_index = len(playlist) - 1
    play_music()

def shuffle_playlist():
    global current_song_index
    if not playlist:
        return
    random.shuffle(playlist)
    current_song_index = 0
    play_music()

def update_listbox():
    playlist_box.delete('1.0', tk.END)
    for song in playlist:
        playlist_box.insert(tk.END, os.path.basename(song)+"\n")
       
        

def speed_up():
    global current_song_index
    global playlist
    
    if not playlist:
        return
    
    current_song = playlist[current_song_index]
    
    y, sr = librosa.load(current_song)

    stretch_factor = 1.75  

    
    D_stretch = librosa.phase_vocoder(rate= stretch_factor,D=librosa.stft(y))
    
    y_stretch = librosa.istft(D_stretch)
    y_stretch = y_stretch * 10**(6/20)

    temp_file = current_song.split(".")[0] + "_stretchedup.wav"
    sf.write(temp_file, y_stretch, sr)
    playlist[current_song_index] = temp_file
    
    play_music()

    playlist[current_song_index]= current_song


def speed_down():
    global current_song_index
    global playlist
    
    if not playlist:
        return
    
    current_song = playlist[current_song_index]
    
    y, sr = librosa.load(current_song)

    stretch_factor =0.5

    D_stretch = librosa.phase_vocoder(rate= stretch_factor,D=librosa.stft(y))
    
    y_stretch = librosa.istft(D_stretch)
    y_stretch = y_stretch * 10**(6/20)  

    temp_file = current_song.split(".")[0] + "_stretcheddown.wav"
    sf.write(temp_file, y_stretch, sr)
    playlist[current_song_index] = temp_file
    
    play_music()

    playlist[current_song_index]= current_song   
    
 
def pitch_up():
    global current_song_index
    global playlist
    
    if not playlist:
        return
    
    current_song = playlist[current_song_index]
    
    song = AudioSegment.from_file(current_song)
    
    semitones = 24 
    
    shifted_song = song._spawn(song.raw_data, overrides={'frame_rate': int(song.frame_rate + semitones*100)})
    
    temp_file = current_song.split(".")[0] + "_pitch_up.mp3"
    shifted_song.export(temp_file, format="mp3")
    
    playlist[current_song_index] = temp_file
    
    play_music()

    playlist[current_song_index]= current_song

def pitch_down():
    global current_song_index
    global playlist
    
    if not playlist:
        return
    
    current_song = playlist[current_song_index]
    
    song = AudioSegment.from_file(current_song)
    
    semitones = -24  
    
    shifted_song = song._spawn(song.raw_data, overrides={'frame_rate': int(song.frame_rate + semitones*100)})
    
    temp_file = current_song.split(".")[0] + "_pitch_down.mp3"
    shifted_song.export(temp_file, format="mp3")
    
    playlist[current_song_index] = temp_file
    
    play_music()

    playlist[current_song_index]= current_song
    
def increase_amplitude():
    global current_song_index
    global playlist
    
    if not playlist:
        return
    
    current_song = playlist[current_song_index]
    
    song = AudioSegment.from_file(current_song)
    
    gain_dB = 10
    
    amplified_song = song + gain_dB
    
    temp_file = current_song.split(".")[0] + "_amplified.mp3"
    amplified_song.export(temp_file, format="mp3")
    
    playlist[current_song_index] = temp_file
    
    play_music()

    playlist[current_song_index]= current_song


def decrease_amplitude():
    global current_song_index
    global playlist
    
    if not playlist:
        return
    
    current_song = playlist[current_song_index]
    
    song = AudioSegment.from_file(current_song)
    
    gain_dB = -10  
    
    attenuated_song = song + gain_dB
    
    temp_file = current_song.split(".")[0] + "_attenuated.mp3"
    attenuated_song.export(temp_file, format="mp3")
    
    playlist[current_song_index] = temp_file
    
    play_music()

    playlist[current_song_index]= current_song    
    
def white_noise(signal, noise_percentage_factor):
    noise = np.random.normal(0, signal.std(), signal.size)
    augmented_signal3 = signal + noise * noise_percentage_factor
    return augmented_signal3

def add_white_noise():
    global current_song_index
    global playlist

    if not playlist:
        return

    current_song = playlist[current_song_index]

    signal, sr = librosa.load(current_song)
    
    noise_signal = white_noise(signal, 0.2)

    temp_file = current_song.split(".")[0] + "_with_noise.mp3"

    sf.write(temp_file, noise_signal, sr)

    playlist[current_song_index] = temp_file

    play_music()

    playlist[current_song_index] = current_song

    
def noise_reduction():
    global current_song_index
    global playlist
    if not playlist:
        return
    
    current_song = playlist[current_song_index]
    song = AudioSegment.from_file(current_song)
    filtered_song = high_pass_filter(song, 100)

    filtered_song = low_pass_filter(filtered_song, 1000)
    normalized_song = normalize(filtered_song)
    temp_file = current_song.split(".")[0] + "_reduced.mp3"
    normalized_song.export(temp_file, format="mp3")
    
    playlist[current_song_index] = temp_file
    
    play_music()

    playlist[current_song_index]= current_song
           

def echo():
   
    global current_song_index
    global playlist
    if not playlist:
        return
    
    current_song = playlist[current_song_index]
    y, sr = librosa.load(current_song)

    
    fractional_delay = int(0.3 * sr)
    delayed_signal = np.zeros_like(y)
    delayed_signal[fractional_delay:]=y[:-fractional_delay]
    echoed_signal = y + 0.5 * delayed_signal

    temp_file = current_song.split(".")[0] + "_echoed.wav"
    sf.write(temp_file, echoed_signal, sr)

    playlist[current_song_index] = temp_file
    
    play_music()

    playlist[current_song_index]= current_song
   

def reverse(signal):

    return signal[::-1]

def reverse_audio():
    global current_song_index
    global playlist
    
    if not playlist:
        return
    
    current_song = playlist[current_song_index]
    
    song = AudioSegment.from_file(current_song)
    
    samples = np.array(song.get_array_of_samples())
    
    reversed_samples = reverse(samples)
    
    reversed_samples_contig = np.ascontiguousarray(reversed_samples, dtype=np.int16)
    
    reversed_song = song._spawn(reversed_samples_contig)
    
    temp_file = current_song.split(".")[0] + "_reversed.mp3"
    reversed_song.export(temp_file, format="mp3")
    
    playlist[current_song_index] = temp_file
    
    play_music()

    playlist[current_song_index] = current_song 
    
    
def plot_waveform():
    global current_song_index
    global playlist
    
    if not playlist:
        return
    
    audio_file = AudioSegment.from_file(playlist[current_song_index])
    samples = audio_file.get_array_of_samples()
    sample_rate = audio_file.frame_rate
    duration = len(samples) / sample_rate 
    num_samples = int(duration * sample_rate)
    samples = samples[:num_samples]  # truncate samples to match duration
    time = np.linspace(0, duration, num_samples, endpoint=False)
    plt.style.use(['bmh'])

    plt.clf() 
    plt.plot(time, samples, color="#8b72be")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.draw() 
    plt.pause(0.001)   


def delay():
    global current_song_index
    global playlist
    
    if not playlist:
        return
     
    time.sleep(10)
    play_music()
    
    
def text_to_speech():
    global current_song_index
    global playlist
    
    if not playlist:
        return
     
    text = playlist[current_song_index]
    text = text_entry.get()
    tts = gTTS(text=text, lang='en')
    file_path = os.path.join(os.getcwd(), f"{text[:5]}.mp3")
    tts.save(file_path)
    playlist.append(file_path)
    update_listbox()
    playlist[current_song_index] = file_path
    play_music()    

    
def add_sampling():
    global current_song_index
    global playlist
    
    if not playlist:
        return
    
    current_song = playlist[current_song_index]
    
    y, sr = librosa.load(current_song) 
    print(sr)

    
    new_sr = 8000
    
    ratio = sr / new_sr
   
    new_length = int(len(y) / ratio)
   
    y_resampled = signal.resample(y, new_length)
    
    temp_file = current_song.split(".")[0] + "_sampled.wav"
    sf.write(temp_file, y_resampled, new_sr)
    playlist[current_song_index] = temp_file
    
    play_music()

    playlist[current_song_index]= current_song
    
window = ctk.CTk()
window.title("TuneyTones")

frame = ctk.CTkFrame(window)
frame.grid(row=0,column=0)

plt.ion() 

select_files_button = ctk.CTkButton(frame, text="Select Files", command=select_files, bg_color="transparent",fg_color="#8b72be",text_color="white",hover_color="#b7b7b7")
select_files_button.grid(row=0,column=0)

text_label = ctk.CTkLabel(window, text="Enter a text:")
text_label.grid(row=0,column=2,pady=10)

text_entry = ctk.CTkEntry(window, width=250)
text_entry.grid(column=2,sticky="N")

convert_button = ctk.CTkButton(window, text="Convert to Audio", command=text_to_speech, height=30, width=30,fg_color="#8b72be",text_color="white",hover_color="#b7b7b7")
convert_button.grid(row=1,column=3,sticky="NW")

reduce_button=ctk.CTkButton(window,text="Reduce Noise",command=noise_reduction,fg_color="#8b72be",text_color="white",hover_color="#b7b7b7")
reduce_button.grid(row=1,column=1, pady=50,sticky="NW")

white_noise_button = ctk.CTkButton(window, text="White Noise", command=add_white_noise,fg_color="#8b72be",text_color="white",hover_color="#b7b7b7")
white_noise_button.grid(row=1,column=2,pady=50,padx=5,sticky="NW")

increase_amplitude_button = ctk.CTkButton(window, text="Increase Amplitude", command=increase_amplitude,fg_color="#8b72be",text_color="white",hover_color="#b7b7b7")
increase_amplitude_button.grid( row=1,column=2,sticky="NE",pady=50,padx=(150,0))

decrease_amplitude_button = ctk.CTkButton(window, text="Decrease Amplitude", command=decrease_amplitude,fg_color="#8b72be",text_color="white",hover_color="#b7b7b7")
decrease_amplitude_button.grid( row=1,column=3,sticky="NW",pady=50,padx=5)

pitch_up_button = ctk.CTkButton(window, text="Pitch Up", command=pitch_up,fg_color="#8b72be",text_color="white",hover_color="#b7b7b7")
pitch_up_button.grid(row=1,column=1,pady=50,sticky="E")

pitch_down_button = ctk.CTkButton(window, text="Pitch Down",text_color="white", command=pitch_down,fg_color="#8b72be",hover_color="#b7b7b7")
pitch_down_button.grid(row=1,column=2,sticky="W",padx=5, pady=40)

speedup_button = ctk.CTkButton(window, text="Speed Up", command=speed_up,text_color="white",fg_color="#8b72be",hover_color="#b7b7b7")
speedup_button.grid( row=1,column=2,padx=(150,0))

speeddown_button = ctk.CTkButton(window, text="Speed Down", command=speed_down,text_color="white",fg_color="#8b72be",hover_color="#b7b7b7")
speeddown_button.grid(row=1,column=3,pady=50,padx=5)

sample_button = ctk.CTkButton(window, text="Sampling", command=add_sampling,text_color="white",fg_color="#8b72be",hover_color="#b7b7b7")
sample_button.grid(row=1,column=2,padx=5,sticky="SW", pady=50)


delay_button=ctk.CTkButton(window, text="Delay", command=delay,text_color="white",fg_color="#8b72be",hover_color="#b7b7b7")
delay_button.grid(row=1,column=2,sticky="SE", pady=50)

echo_button=ctk.CTkButton(window, text="Echo", command=echo,text_color="white",fg_color="#8b72be",hover_color="#b7b7b7")
echo_button.grid(row=1,column=3,sticky="SW",padx=5, pady=50)

reverse_button=ctk.CTkButton(window, text="Reverse", command=reverse_audio,text_color="white",fg_color="#8b72be",hover_color="#b7b7b7")
reverse_button.grid(row=1,column=1,sticky="SW", pady=50)

playlist_frame = ctk.CTkFrame(window)
playlist_frame.grid(row=1,column=0)

playlist_label = ctk.CTkLabel(playlist_frame, text="  Playlist:  ")
playlist_label.grid(row=1,column=0,padx=1, pady=1)

playlist_box =ctk.CTkTextbox(playlist_frame, width=220, height=140,bg_color="transparent")
playlist_box.grid(padx=20, pady=20)

previous_song_button = ctk.CTkButton(window, text="⏮️", command=previous_song, font=("Retrcade", 14), height=30, width=30,fg_color="#8b72be",hover_color="#b7b7b7")
previous_song_button.grid( row=2,column=0,sticky="NW",padx=5)

play_music_button = ctk.CTkButton(window, text=" ▶ ", command=play_music, font=("Segoe UI Symbol",10),fg_color="#8b72be", height=30, width=30,hover_color="#b7b7b7")
play_music_button.grid(row=2,column=0,sticky="NW",padx=40)

next_song_button = ctk.CTkButton(window, text="⏭️", command=next_song, font=("Retrcade", 14), height=30, width=30,fg_color="#8b72be",hover_color="#b7b7b7")
next_song_button.grid( row=2,column=0,sticky="NW",padx=(75,0))

pause_music_button = ctk.CTkButton(window, text=" ■ ", command=pause_music, font=("Segoe UI Symbol", 10), height=30, width=30,fg_color="#8b72be",hover_color="#b7b7b7")
pause_music_button.grid(row=2,column=0,sticky="NW",padx=(110,0))

resume_music_button = ctk.CTkButton(window, text="⏸", command=resume_music, font=("Segoe UI Symbol", 14),fg_color="#8b72be" ,height=30, width=30,hover_color="#b7b7b7")
resume_music_button.grid(row=2,column=0,sticky="NW",padx=(145,0))

shuffle_button = ctk.CTkButton(window, text="🔀", command=shuffle_playlist, font=("Segoe UI Symbol", 12), height=30, width=30,fg_color="#8b72be",hover_color="#b7b7b7")
shuffle_button.grid(row=2,column=0,sticky="NW",padx=(180,0))

volume_label = ctk.CTkLabel(window, text=" 🎧",font=("Segoe UI Symbol",18))
volume_label.grid(row=2,column=0,sticky="W",padx=(315,0),pady=(0,10))

volume_scale = ctk.CTkSlider(window, from_=0.0, to=1.0, orientation="horizontal",width=100,button_hover_color="#b7b7b7",command=set_volume,state="normal",hover="True",button_color="#8b72be")
volume_scale.set(current_volume)
volume_scale.grid(row=2,column=0,sticky="NW",padx=(215,0),pady=10)

update_listbox()

window.mainloop()

