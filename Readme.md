# Ratebeer Shopping Helper

This little script will help you buy beers for you and other <b>Ratebeerians</b>.

### Purpose
This script will allow you to search the ratings of you and your friends, and will show you who already rated the wanted beer.
### Usage
1) Download all your ratings (click on <i>My Account → My Beer Rantings → Compile My Ratings</i>; leave the standard delimiter "|")
2) Get your friend(s) to send you  their ratings
3) Run <b>prepare_data.py</b> once for each user (prepare_data.py is only tested on a Linuxmachine)
4) Install <i>QPython3</i> or a similar app on your mobile device
5) Copy the <b>compare.py</b> and all needed <b>*.ratings</b> files to the same folder on the mobile device
6) Start <b>compare.py</b> and have fun

If you run the program only on a computer item <b>4)</b> and <b>5)</b> are unnecessary.

### License
This and all versions is/will be licensed under the GPLv3.

### Disclaimer
This is just a little fun project I do, so I can buy some beers for <i>jfb</i>'s next visit. There will be most likely no maintaining. If you find a bug in this project, you can contact me on www.github.com/neur0nic or on www.ratebeer.com/user/133619/.
<br>This script is only tested on an Linux machine with Python 3.6 and an Android 4.2 with QPython3.
### Error
####- File not found
If the program on your mobile device returns something like <i>file *.ratings not found</i>, you probably need to change <b>compare.py</b> line <b>53</b> to your actual working directory.
####- no module named termcolor
I had to manually install the <i>termcolor</i> package to my Android app