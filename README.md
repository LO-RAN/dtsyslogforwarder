# dtsyslogd

Dynatrace Syslog forwarder

will listen on port 514 (syslogd default port) for remote syslog connections
and forward any incoming log event to Dynatrace through log ingestion API

## deployment
Install on any Linux host, why not an ActiveGate.
Unzip "dtsyslogd.zip" in "/opt/dynatrace/batch"

## To start the script as a Linux service:

```bash
sudo cp dtsyslogd.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start dtsyslogd.service
sudo systemctl enable dtsyslogd.service
```


## to test the feature, just type a shell comamand like the following : 

```bash
nc -w0 -u <theHostWhereThedtsyslogdscriptIsRunning> 514 <<< "some message to send to syslog"
```


## inspired by

https://gist.github.com/marcelom/4218010 
https://github.com/choeffer/py3syslog