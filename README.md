# word-hunt
Code behind getting the world record in word hunt. Note this was complicated as I had to workaround with a raspberry pi and a teensy for phone control

See a video explanation [here](https://www.tiktok.com/@spicypete/video/6821358058799779078)!


When this project was created, no easy way of controlling an iphone from a computer was available. A popular jailbreak project that allows one to VNC share their screen wasn't available.


What this means is I plugged a teensy: a arduino capable of acting as a mouse into my phone. I then plugged the teensy into a raspberry pi, and then airplayed my phones screen to the raspberry pi.


1) Initialize connection and wait for board to display
2) Parse board using image processing and calculate all words
3) Convert these words into relative mouse positions
4) Send the mouse positions to the teensy
5) Profit!!!!
