const express = require('express');
const fs = require('fs');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;

app.use(bodyParser.raw({ type: 'application/octet-stream', limit: '50mb' }));

app.post('/sendiq', (req, res) => {
  const filePath = 'record.iq';
  const sampleRate = req.headers['sample-rate'] || '200000';
  const frequency = req.headers['frequency'] || '433.944e6';
  const harmonicNumber = req.headers['harmonic-number'];
  const sharedMemoryToken = req.headers['shared-memory-token'];
  const ddsMode = req.headers['dds-mode'] ? '-d' : '';
  const powerLevel = req.headers['power-level'];
  const loopMode = req.headers['loop-mode'] ? '-l' : '';  // Attiva se l'header loop-mode è true
  const iqType = req.headers['iq-type'] || 'u8';

  fs.writeFile(filePath, req.body, (err) => {
    if (err) {
      return res.status(500).send('Errore nella scrittura del file');
    }

    const cmd = `sudo`;
    const args = [`../rpitx/sendiq`, `-i`, filePath, `-s`, sampleRate, `-f`, frequency, `-t`, iqType, ddsMode, loopMode,
                  harmonicNumber ? `-h ${harmonicNumber}` : '',
                  sharedMemoryToken ? `-m ${sharedMemoryToken}` : '',
                  powerLevel ? `-p ${powerLevel}` : ''];

    const child = spawn(cmd, args.filter(arg => arg));

    if (req.headers['loop-mode']) {
      req.on('close', () => {
        child.kill(); // Termina il processo quando la connessione HTTP viene chiusa
        console.log('Connessione chiusa, processo terminato');
      });
      res.status(200).send('Comando eseguito, in modalità loop');
    } else {
      child.on('exit', (code) => {
        console.log(`Processo terminato con codice ${code}`);
      });
      res.status(200).send('Comando eseguito');
    }
  });
});

app.listen(PORT, () => {
  console.log(`Server in ascolto sulla porta ${PORT}`);
});
