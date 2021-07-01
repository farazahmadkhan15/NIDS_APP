# Real Time Network Intrusion Detection System Using Machine Learning

## Setting Up Linux Dependencies:

### CICFLOWMETER:

CICFLOWMETER has been modified according to our application. NIDS only support
CICFLOWMETER installed from mentioned repository:
```sh
git clone https://github.com/farazahmadkhan15/cicflowmeter-NIDS.git 
cd cicflowmeter-NIDS.git 
sudo python3 setup.py install 
```

### net-tools

```sh
sudo apt install net-tools
```

### whois
```sh
sudo apt install whois
```

### Redis-server
```sh
sudo apt update
sudo apt install redis-server
```


## Installing Application: 



```sh
git clone https://github.com/farazahmadkhan15/NIDS_APP.git 
cd NIDS_APP 
python3 -m venv venv 
sudo su 
. venv/bin/activate 
 pip install -r requirements.txt 
```

## Running App
```sh
sudo su 
. venv/bin/activate 
flask run
```