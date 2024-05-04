#include <pigpio.h>
#include <ncurses.h>

#define PIN 18 // Sostituisci con il numero del GPIO che intendi usare

int main() {
    int frequency = 10000; // Inizializza la frequenza a 10kHz
    double dutyCycle = 50.0; // Inizializza il duty cycle al 50%

    if (gpioInitialise() < 0) {
        return 1; // Inizializzazione fallita
    }

    gpioSetMode(PIN, PI_OUTPUT);

    // Calcola il valore del duty cycle per pigpio (range 0-1000000)
    unsigned int dutyCycleValue = (unsigned int)(dutyCycle * 10000);

    // Imposta PWM con duty cycle iniziale
    gpioHardwarePWM(PIN, frequency, dutyCycleValue);

    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE); // Permette l'input delle frecce

    printw("Usa le frecce su/giù per aumentare/diminuire la frequenza.\n");
    printw("Usa Pag Up/Pag Down per aumentare/diminuire il duty cycle.\n");
    printw("Premi 'q' per uscire.\n");
    refresh();

    int ch;
    while ((ch = getch()) != 'q') {
        switch (ch) {
            case KEY_RIGHT:
                frequency += 1000; // Incrementa di 1 kHz
                break;
            case KEY_LEFT:
                frequency -= 1000; // Decrementa di 1 kHz
                break;
            case KEY_UP:
                frequency += 100; // Incrementa di 100 Hz
                break;
            case KEY_DOWN:
                frequency -= 100; // Decrementa di 100 Hz
                break;
            case KEY_PPAGE: // Pag Up
                if(dutyCycle < 100.0) dutyCycle += 0.5;
                break;
            case KEY_NPAGE: // Pag Down
                if(dutyCycle > 0.5) dutyCycle -= 0.5; // Evita di andare sotto lo 0%
                break;
        }

        // Evita frequenze negative
        if (frequency < 0) frequency = 0;

        // Aggiorna il valore del duty cycle per pigpio
        dutyCycleValue = (unsigned int)(dutyCycle * 10000);

        // Aggiorna PWM con la nuova frequenza e il nuovo duty cycle
        gpioHardwarePWM(PIN, frequency, dutyCycleValue);

        // Pulisce lo schermo e stampa le nuove impostazioni
        clear();
        printw("Usa le frecce su/giù per aumentare/diminuire la frequenza.\n");
        printw("Usa Pag Up/Pag Down per aumentare/diminuire il duty cycle.\n");
        printw("Premi 'q' per uscire.\n");
        printw("Frequenza attuale: %d Hz\n", frequency);
        printw("Duty cycle attuale: %.1f%%\n", dutyCycle);
        refresh();
    }

    endwin(); // Termina ncurses
    gpioTerminate(); // Pulisce pigpio
    
    return 0;
}
