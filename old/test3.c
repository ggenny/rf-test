#include <pigpio.h>
#include <stdio.h>
#include <stdlib.h>

#define PIN 18 // Sostituisci con il numero del GPIO che intendi usare

void adjustFrequency(int *frequency, char input) {
    switch (input) {
        case 'u': // aumenta la frequenza
            *frequency += 5000;
            break;
        case 'd': // diminuisce la frequenza
            *frequency -= 5000;
            break;
    }

    // Assicura che la frequenza non vada sotto 0
    if (*frequency < 0) {
        *frequency = 0;
    }

    // Imposta la nuova frequenza
    gpioHardwarePWM(PIN, *frequency, 500000); // Duty cycle al 50%
    printf("Frequenza attuale: %d Hz\n", *frequency);
}

int main() {
    if (gpioInitialise() < 0) {
        fprintf(stderr, "Errore nell'inizializzazione di pigpio\n");
        return 1;
    }

    int frequency = 100000; // Frequenza iniziale di 500 kHz
    gpioSetMode(PIN, PI_OUTPUT);
    gpioHardwarePWM(PIN, frequency, 500000); // Duty cycle al 50%
    printf("Frequenza iniziale: %d Hz\n", frequency);

    printf("Premi 'u' per aumentare di 1 kHz, 'd' per diminuire di 1 kHz, 'q' per uscire.\n");

    char input;
    do {
        input = getchar();
        adjustFrequency(&frequency, input);
    } while (input != 'q');

    gpioTerminate();
    return 0;
}
