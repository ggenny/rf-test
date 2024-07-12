import numpy as np
from scipy.signal import gausspulse, lfilter, butter, decimate
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
import threading
import queue
import asyncio

# Parametri del segnale
sample_rate = 250000  # Frequenza di campionamento in Hz
bit_duration = 0.001  # Durata di ogni bit in secondi
bt = 0.3  # Bandwidth-time product per GMSK
power_threshold = 0.000032  # Soglia di potenza per la decodifica
decimation_factor = 100  # Fattore di decimazione

# Coda per la comunicazione tra i thread
sample_queue = queue.Queue()


# Funzione per la demodulazione GMSK
def gmsk_demodulate(iq_samples, sample_rate, bit_duration, bt, decimation_factor):
    # Decimazione del segnale
    iq_samples = decimate(iq_samples, decimation_factor)
    sample_rate //= decimation_factor
    samples_per_bit = int(sample_rate * bit_duration)

    # Creazione di un filtro gaussiano
    t = np.arange(-3 * samples_per_bit, 3 * samples_per_bit) / sample_rate
    pulse = gausspulse(t, fc=1 / bit_duration, bw=bt, retquad=False)

    # Filtraggio del segnale
    filtered_iq = lfilter(pulse, 1.0, iq_samples)

    # Demodulazione di fase
    phase = np.angle(filtered_iq)
    demodulated = np.diff(phase)

    # Applicazione di un filtro passa-basso per rimuovere il rumore ad alta frequenza
    b, a = butter(5, 0.2)
    demodulated = lfilter(b, a, demodulated)

    # Campionamento e decisione
    bit_samples = demodulated[::samples_per_bit]
    bits = (bit_samples > 0).astype(int)

    return bits


# Funzione per calcolare la potenza del segnale IQ
def calculate_power(iq_samples):
    return np.mean(np.abs(iq_samples) ** 2)


# Funzione per l'acquisizione dei campioni in tempo reale
def acquire_samples():
    async def stream_samples():
        sdr = RtlSdr()

        sdr.sample_rate = sample_rate
        sdr.center_freq = 433.944e6  # Frequenza centrale di esempio
        sdr.gain = 10

        try:
            async for samples in sdr.stream():
                sample_queue.put(samples)
        finally:
            await sdr.close()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(stream_samples())


# Funzione per l'elaborazione in tempo reale
def process_samples():
    while True:
        if not sample_queue.empty():
            iq_samples = sample_queue.get()
            power = calculate_power(iq_samples)

            if power > power_threshold:
                decoded_bits = gmsk_demodulate(iq_samples, sample_rate, bit_duration, bt, decimation_factor)
                print(decoded_bits)
            #else:
            #    print("Potenza troppo bassa, segnale ignorato.")


# Creazione e avvio dei thread per l'acquisizione e l'elaborazione
acquire_thread = threading.Thread(target=acquire_samples)
process_thread = threading.Thread(target=process_samples)

acquire_thread.start()
process_thread.start()

# Attesa della terminazione dei thread (in un'applicazione reale, gestisci l'arresto dei thread in modo sicuro)
acquire_thread.join()
process_thread.join()
