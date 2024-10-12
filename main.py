import numpy as np
import sounddevice as sd

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=1.0):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return sine_wave

def play_wave(f, frequency, duration, sample_rate=44100, amplitude=1.0):
    wave = f(frequency, duration, sample_rate, amplitude)
    sd.play(wave, sample_rate)
    sd.wait()

def generate_scale(start_freq=440, steps=7):
    factor = 2**(1/steps)
    return [start_freq * (factor**i) for i in range(steps + 1)]

def generate_keyboard(initial_frequency):
    row_1 = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']
    row_2 = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']
    row_3 = ['z', 'x', 'c', 'v', 'b', 'n', 'm']
    octaves = generate_scale(initial_frequency, len(row_2))
    return dict(zip(row_2, octaves))

def main(keyboard, duration):
    while True:
        key = input('Play')
        play_wave(generate_sine_wave, frequency=keyboard[key], duration=duration)

    return 0

if __name__ == '__main__':
    frequency = input('Select the frequency of the base note: ')
    frequency = float(frequency)
    keyboard = generate_keyboard(frequency)
    duration = input('Select the duration: ')
    duration = float(duration)

    exit(main(keyboard=keyboard, duration=duration))