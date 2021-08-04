#!/usr/bin/env python

# Tiny Syslog Server in Python.
##
# inspired by :
# https://gist.github.com/marcelom/4218010 
# https://github.com/choeffer/py3syslog

import os
import sys
import requests
import json
import configparser
import socketserver
import logging


class SyslogUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = bytes.decode(self.request[0].strip())
        socket = self.request[1]
        #print("%s : " % self.client_address[0], str(data))
        logging.info(str(data))
        self.sendtodynatrace(str(data),self.client_address[0], dtendpointurl,dttoken)

    # --------------------------------------------------------------------------------

    def sendtodynatrace(self, theresult, thesource, theurl, thetoken):

        thejson = [{"content": theresult,"log.source": thesource}]

        rdt = requests.post(
            theurl+'/api/v2/logs/ingest',
            data=json.dumps(thejson),
            headers={
                'Authorization': "Api-Token " + thetoken,
                'Content-Type': 'application/json; charset=utf-8',
                'Accept': 'application/json; charset=utf-8',

            },
            verify=False
        )

        # error ?
        if(rdt.status_code != 204):
            logging.error(rdt.status_code, rdt.reason, rdt.text)
        else:
            logging.info("Successfully pushed log data to Dynatrace ingestion endpoint from "+thesource+".")
            logging.debug(rdt.text)
# --------------------------------------------------------------------------------


if __name__ == "__main__":

    requests.packages.urllib3.disable_warnings()

    # open properties file
    config = configparser.ConfigParser()
    config.read(os.path.join(sys.path[0], "config.properties"))

    # get properties
    dttoken = config.get('dynatrace', 'dt_api_token')
    dtendpointurl = config.get('dynatrace', 'dt_endpoint_url')
    syslogip=config.get('syslog', 'syslog_ip')
    syslogport=int(config.get('syslog', 'syslog_port'))
    loggingpath=config.get('logging', 'logging_path')

    logging.basicConfig(filename=loggingpath,format='%(asctime)s %(message)s', level=logging.INFO)

    try:
        server = socketserver.UDPServer((syslogip, syslogport), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print("Crtl+C Pressed. Shutting down.")
