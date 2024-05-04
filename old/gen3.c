#include <stdio.h>
#include <stdint.h>

int main() {
    FILE *file = fopen("sequence.ft", "wb");
    if (!file) {
        perror("Failed to open file");
        return 1;
    }

    // Definisci la sequenza di bit da trasmettere
    char *bits = "100010001000111010001110100011101000111010001110100010001000111010001110100011101000111011101110100000000000000000000000000000000000000000000100010001000111010001110100011101000111010001110100010001000111010001110100011101000111010001000100000000000000000000000000000000000";
    double frequency = 434030000; // Frequenza per i bit '1'
    uint32_t duration = 350000;   // 350 microsecondi in nanosecondi
    uint32_t padding = 0;

    for (int i = 0; bits[i] != '\0'; i++) {
        double freq_to_write = bits[i] == '1' ? frequency : 0;  // Usa 0 Hz per '0'
        
        // Scrivi la frequenza
        fwrite(&freq_to_write, sizeof(double), 1, file);
        // Scrivi la durata
        fwrite(&duration, sizeof(uint32_t), 1, file);
        // Scrivi il padding
        fwrite(&padding, sizeof(uint32_t), 1, file);
    }

    fclose(file);
    printf("File written successfully.\n");
    return 0;
}
