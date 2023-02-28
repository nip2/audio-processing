# Audio analysis programs

## Arduino FFT readback
This set of programs reads voltage data from a piezo transducer through a teensy 3.2 and prints the data to the serial port
### Files:

* record2PC.ino
* serialarduino.py
* analyzeData.py

### How to run:

Connect a 1Mohm resistor and zener diode from analog pin A2 to GND and connect the piezo red to pin A2. Set an active low button to pin 8. Upload record2PC.ino to arduino UNO or teensy board.

In serialarduino.py, change the serPort variable to the serial port connection to the arduino. Run serialarduino.py from the computer while arduino is connected and running. Press and hold the button on the arduino. The signal from the piezo will be recorded while the button is pressed.

Run analyzeData.py to plot the frequency response and fundamental tone.

## animate folder 
### Audio frequency spectrum animation:

animatewav.py takes an audio file and plots its animated frequency response while playing the audio. Two example wav files are included.
