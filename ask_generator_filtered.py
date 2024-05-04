import numpy as np
import argparse
import scipy.signal as signal
from scipy.signal import butter, filtfilt

def apply_lowpass_filter(signal, sample_rate, cutoff_frequency=300, order=5):
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff_frequency / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal

def generate_ask_signal(sample_rate, bit_duration, frequency, sequence, repetitions, pause_duration_ms, output_file, enable_filter, cutoff_freq):
    # Calcola il numero di campioni per la pausa
    pause_samples = int(sample_rate * pause_duration_ms / 1000)

    # Crea un array per il segnale I e Q con spazio sufficiente per ripetizioni e pause
    total_samples = repetitions * (len(sequence) * int(bit_duration * sample_rate) + pause_samples)
    I = np.zeros(total_samples)
    Q = np.zeros_like(I)  # Q rimane zero per un segnale ASK

    # Compila il segnale con ripetizioni e pause
    current_sample = 0
    for _ in range(repetitions):
        for bit in sequence:
            num_samples = int(bit_duration * sample_rate)
            t = np.linspace(0, bit_duration, num_samples, endpoint=False)
            if bit == '1':
                I[current_sample:current_sample + num_samples] = np.sin(2 * np.pi * frequency * t)
            current_sample += num_samples
        current_sample += pause_samples  # Aggiungi pause dopo ogni ripetizione del segnale

    # Applica il filtro passa-basso se richiesto
    if enable_filter:
        I = apply_lowpass_filter(I, sample_rate, cutoff_freq)

    # Converti i segnali in unsigned 8-bit format (range da 0 a 255)
    I_u8 = np.uint8((I + 1) * 127.5)
    Q_u8 = np.uint8((Q + 1) * 127.5)

    # Intercala I e Q per il formato I/Q
    iq_samples = np.empty(2 * len(I), dtype=np.uint8)
    iq_samples[0::2] = I_u8
    iq_samples[1::2] = Q_u8

    # Salva il segnale I/Q in un file
    with open(output_file, 'wb') as f:
        f.write(iq_samples.tobytes())

    print(f"File .iq creato con successo: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Generate an ASK modulated signal and save to an IQ file.")
    parser.add_argument('--sample_rate', type=int, default=200000, help='Sample rate in Hz')
    parser.add_argument('--bit_duration', type=float, default=0.00035, help='Duration of each bit in seconds')
    parser.add_argument('--frequency', type=int, default=1000, help='Carrier frequency in Hz')
    parser.add_argument('--sequence', type=str, default="1000100010001110", help='Bit sequence for ASK modulation')
    parser.add_argument('--repetitions', type=int, default=10, help='Number of repetitions of the sequence')
    parser.add_argument('--pause_duration_ms', type=int, default=10, help='Duration of pause between repetitions in milliseconds')
    parser.add_argument('--output', type=str, default='repeated_ask_signal.iq', help='Output IQ file name')
    parser.add_argument('--enable_filter', action='store_true', help='Enable low pass filtering')
    parser.add_argument('--cutoff_freq', type=int, default=2000, help='Cutoff frequency for the low pass filter if enabled')

    args = parser.parse_args()

    generate_ask_signal(args.sample_rate, args.bit_duration, args.frequency, args.sequence, args.repetitions, args.pause_duration_ms, args.output, args.enable_filter, args.cutoff_freq)

if __name__ == '__main__':
    main()
