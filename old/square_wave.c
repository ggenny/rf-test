#include <pigpio.h>

#define PIN 17 // Sostituisci con il numero del GPIO che intendi utilizzare

int main() {
    if (gpioInitialise() < 0) {
        // Inizializzazione fallita
        return 1;
    }

    // Imposta la frequenza PWM sul pin desiderato
    gpioSetPWMfrequency(PIN, 1000); // Imposta la frequenza a 10 kHz

    // Imposta il duty cycle del PWM al 50% per ottenere un'onda quadra
    // 255/2 = ~50% di duty cycle in una scala da 0 a 255
    gpioPWM(PIN, 128);

    // Lascia il segnale attivo per un po' (ad esempio, 10 secondi)
    // In una applicazione reale, gestiresti la durata e la terminazione in modo diverso
    time_sleep(6000);

    gpioTerminate(); // Termina pigpio e pulisce
    return 0;
}
