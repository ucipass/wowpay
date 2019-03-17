# wowpay
Automated Payment for WOW Cable TV provider
Basically automates several payments using different credit cards based on a YAML file.
# Installation
## Install chrome
    sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
    sudo echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
    sudo apt-get -y update
    sudo apt-get -y install google-chrome-stable
## Install chromedriver
    wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    sudo mv chromedriver /usr/bin/chromedriver
    sudo chown root:root /usr/bin/chromedriver
    sudo chmod +x /usr/bin/chromedriver
## Install selenium library
    sudo apt install python3-pip
    pip3 install selenium
## Install and run python program
    git clone https://github.com/ucipass/wowpay
    cd wowpay
    cp config_sample.yaml config.yaml
# Run the program
edit config.yaml

    python3 ./wowpay.py
# Options
    ubuntu@lubuntu4:~/wowpay$ python3 wowpay.py --help
    usage: wowpay.py [-h] [-u USERNAME] [-p PASSWORD] [-f] [-q]
    
    optional arguments:
      -h, --help            show this help message and exit
      -u USERNAME, --username USERNAME
      -p PASSWORD, --password PASSWORD
      -f, --force
      -q, --quiet
