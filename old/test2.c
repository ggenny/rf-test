#include <pigpio.h>
#include <math.h>

#define PIN 17 // Sostituisci con il tuo GPIO

int main() {
    if (gpioInitialise() < 0) return 1; // Inizializzazione fallita

    // Assicurati che il PIN sia impostato come output o PWM
    // gpioSetMode(PIN, PI_OUTPUT); // Per output digitale

    const int samples = 100; // Numero di campioni per l'onda
    gpioPulse_t pulse[samples];

    for (int i = 0; i < samples; i++) {
        double rad = 2 * M_PI * i / samples; // Calcola l'angolo in radianti
        unsigned onTime = (sin(rad) + 1) * 500; // Calcola la durata dell'impulso (esempio)
        
        pulse[i].gpioOn = (1 << PIN); // Imposta il PIN ad alto
        pulse[i].gpioOff = 0; // Nessun PIN impostato a basso
        pulse[i].usDelay = onTime; // Imposta la durata dell'impulso
    }

    gpioWaveAddNew();
    gpioWaveAddGeneric(samples, pulse);
    int wave_id = gpioWaveCreate();

    if (wave_id >= 0) {
	while(1) {
        	gpioWaveTxSend(wave_id, PI_WAVE_MODE_REPEAT);
        }
    }

    // Aggiungi qui il codice per terminare la trasmissione e pulire
    gpioTerminate();
    return 0;
}
