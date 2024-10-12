import numpy as np
import sounddevice as sd
import sys
import threading
import time

if sys.platform == 'win32':
    import msvcrt
else:
    import tty
    import termios

def get_key():
    if sys.platform == 'win32':
        return msvcrt.getch().decode('utf-8')
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=1.0):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return sine_wave

def play_wave(f, frequency, sample_rate=44100, amplitude=1.0):
    stream = sd.OutputStream(samplerate=sample_rate, channels=1)
    stream.start()
    
    chunk_duration = 0.1  # 100ms chunks
    while True:
        chunk = f(frequency, chunk_duration, sample_rate, amplitude)
        stream.write(chunk.astype(np.float32))
        if not threading.current_thread().is_alive():
            break
    
    stream.stop()
    stream.close()

def generate_scale(start_freq=440, steps=7):
    factor = 2**(1/steps)
    return [start_freq * (factor**i) for i in range(steps + 1)]

def generate_keyboard(initial_frequency):
    row_1 = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']
    row_2 = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']
    row_3 = ['z', 'x', 'c', 'v', 'b', 'n', 'm']
    octaves = generate_scale(initial_frequency, len(row_2))
    return dict(zip(row_2, octaves))

def main(keyboard):
    active_threads = {}
    while True:
        if sys.platform == 'win32':
            if msvcrt.kbhit():
                key = get_key()
                if key in keyboard:
                    if key not in active_threads or not active_threads[key].is_alive():
                        active_threads[key] = threading.Thread(target=play_wave, args=(generate_sine_wave, keyboard[key]))
                        active_threads[key].start()
                else:
                    for thread_key in list(active_threads.keys()):
                        active_threads[thread_key].join(timeout=0.1)
                        if not active_threads[thread_key].is_alive():
                            del active_threads[thread_key]
        else:
            key = get_key()
            if key in keyboard:
                if key not in active_threads or not active_threads[key].is_alive():
                    active_threads[key] = threading.Thread(target=play_wave, args=(generate_sine_wave, keyboard[key]))
                    active_threads[key].start()
            else:
                for thread_key in list(active_threads.keys()):
                    active_threads[thread_key].join(timeout=0.1)
                    if not active_threads[thread_key].is_alive():
                        del active_threads[thread_key]
    return 0

if __name__ == '__main__':
    frequency = input('Select the frequency of the base note: ')
    frequency = float(frequency)
    keyboard = generate_keyboard(frequency)

    exit(main(keyboard=keyboard))