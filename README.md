# msStopWatch
Outputs a neat little stopwatch to a 2-line LCD, with physical start/stop button and reset button. The code assumes that (a) the start/stop button is latching (so it stays down when pressed, until pressed again), that (b) it has a built-in LED, which it turns on when the timer is running, and (c) that the LCD has a HD44780 controller.

Uses the newish libraries from Adafruit for interacting with the GPIO pins.

If you choose to build this project, you'll also want a variable pot connected to the LCD to control contrast. That is reflected in the accompanying schematics but plays no role in the included python code.
