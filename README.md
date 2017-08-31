# Use Amazon Dash with IFTTT to trigger almost anything!

Hack an Amazon Dash Button and use it with a Raspberry Pi to trigger almost anything via webhook with IFTTT.com.

## Required pre-requisites

You will need to have an account on [IFTTT.com](https://ifttt.com) in order to use this app. They are free! Once you have an account, you'll need to activate the [Webhooks service](https://ifttt.com/maker_webhooks) as you'll need to create the webhook here to use in your code.

Please run the following command on your Raspberry Pi to install the relevant modules for this app to work:

````
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python-scapy tcpdump -y
````

## Capturing the Amazon Dash Button's MAC address

Setup the Amazon Dash Button using the iOS or Android app, but stop before you add a product. Force close the app on your device to be safe.

There are various methods to obtaining the MAC address of the Dash Button, but I simply used [Fing](https://www.fing.io/) to scan my network and then copied the MAC address from the button.

## Clone this repository

Unless you want to manually create the Python script yourself, simply clone this by running:

````git clone https://github.com/raspberrycoulis/iftttdash.git````

## Create a Webhook trigger on IFTTT.com

Without going into too much detail here, you need to create a webhook trigger using the [Webhooks service](https://ifttt.com/maker_webhooks) on IFTTT. Set a trigger word and choose your "action" accordingly - this action is triggered by the webhook sent by your Raspberry Pi when you press the Amazon Dash Button.

To get the full URL required (which will include your trigger and your unique key), you can click on the **Documentation** link on the [Webhooks service](https://ifttt.com/maker_webhooks) channel and follow the simple instructions provided there. Your URL will look something like `https://maker.ifttt.com/trigger/TRIGGER/with/key/YOUR_UNIQUE_KEY`

## Replace the necessary parts in the iftttdash.py script

Once you have created your webhook, edit the `iftttdash.py` file and replace the `TRIGGER` and `YOUR_UNIQUE_KEY` segments of the URL and save. This assumes you are in the folder where the `iftttdash.py` script is located on your Raspberry Pi:

````
nano iftttdash.py
"REPLACE THE SEGMENTS IN YOUR URL"
ctrl+x
y
````

## Running on boot

I prefer to use systemd to run Python scripts on boot as you can run them as a service, start, stop, restart them and check the status of them easily. To do so, you need to do the following:

````sudo nano /lib/systemd/system/iftttdash.service````

Then add the following:

````
[Unit]
Description=Amazon Dash IFTTT Webhook Service
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python /home/pi/github/iftttdash/iftttdash.py > /home/pi/github/iftttdash/iftttdash.log 2>&1

[Install]
WantedBy=multi-user.target
````

The parts to check are the `ExecStart` command as this assumes the `iftttdash.py` script is located in `/home/pi/github/iftttdash` so please update accordingly if you have installed the script in a different location.

Once you have done this, `Ctrl+X` to exit and `Y` to save then run:

````
sudo chmod 644 /lib/systemd/system/iftttdash.service
sudo systemctl daemon-reload
sudo systemctl enable iftttdash.service
````

You can `sudo reboot` or simply run `sudo systemctl start iftttdash.service` to start the script. Check the status by running `sudo systemctl status iftttdash.service`.