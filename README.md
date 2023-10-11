# dtsyslogd

Dynatrace Syslog forwarder

will listen by default on port 8514 (configurable in config.properties) for remote syslog connections
and forward any incoming log event to Dynatrace through log ingestion API

## deployment
* Install on any Linux host, e.g. an ActiveGate.
* Unzip "dtsyslogd.zip" in "/opt/dynatrace/batch"
* Edit "config.properties" to set tenant URL and token for your Dynatrace environment.

## To start the script as a Linux service:

```bash
sudo cp dtsyslogd.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start dtsyslogd.service
sudo systemctl enable dtsyslogd.service
```


## to test the feature, just type a shell command like the following : 

```bash
nc -w0 -u <theHostWhereThedtsyslogdscriptIsRunning> 8514 <<< "some message to send to syslog"
```


## inspired by

https://gist.github.com/marcelom/4218010 
https://github.com/choeffer/py3syslog
