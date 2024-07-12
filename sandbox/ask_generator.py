import numpy as np
import argparse
from scipy.signal import butter, filtfilt

def generate_ask_signal(sample_rate, bit_duration, frequency, sequence, repetitions, pause_duration_ms, output_file):
    # Calcola il numero di campioni per bit e per la pausa
    bit_samples = int(bit_duration * sample_rate)
    pause_samples = int(sample_rate * pause_duration_ms / 1000)

    # Genera il segnale della sinusoide per la durata totale di tutti i bit in tutte le ripetizioni
    total_sequence_samples = len(sequence) * bit_samples
    total_samples = repetitions * (total_sequence_samples + pause_samples)
    t = np.linspace(0, total_samples / sample_rate, total_samples, endpoint=False)
    I = np.sin(2 * np.pi * frequency * t)
    Q = np.cos(2 * np.pi * frequency * t)  # Q sfasata di 90 gradi rispetto a I

    # Azzerare le parti per i bit '0' e le pause
    current_sample = 0
    for _ in range(repetitions):
        for i, bit in enumerate(sequence):
            if bit == '0':
                I[current_sample + i * bit_samples: current_sample + (i + 1) * bit_samples] = 0
                Q[current_sample + i * bit_samples: current_sample + (i + 1) * bit_samples] = 0
        current_sample += total_sequence_samples
        # Azzerare la pausa dopo ogni ripetizione della sequenza
        I[current_sample: current_sample + pause_samples] = 0
        Q[current_sample: current_sample + pause_samples] = 0
        current_sample += pause_samples

    # # Converti i segnali in signed 8-bit format (range da -128 a 127)
    I_s8 = np.int8(I * 127)
    Q_s8 = np.int8(Q * 127) 

    # # Intercala I e Q per il formato I/Q in signed 8-bit
    iq_samples = np.empty(2 * len(I), dtype=np.int8)
    iq_samples[0::2] = I_s8 
    iq_samples[1::2] = Q_s8 

    # Intercala I e Q per il formato I/Q in float32
    #iq_samples = np.empty(2 * len(I), dtype=np.float32)
    #iq_samples[0::2] = I
    #iq_samples[1::2] = Q    

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

    args = parser.parse_args()

    generate_ask_signal(args.sample_rate, args.bit_duration, args.frequency, args.sequence, args.repetitions, args.pause_duration_ms, args.output)

if __name__ == '__main__':
    main()
