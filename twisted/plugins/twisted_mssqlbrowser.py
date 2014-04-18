#!/usr/bin/env python
import struct
import os
import signal
import json
import sys
try:
    from twisted.internet.protocol import DatagramProtocol
    from twisted.internet import reactor
    from twisted.application import internet
    from twisted.application.service import IServiceMaker
    from twisted.plugin import IPlugin
    from zope.interface import implements
    from twisted.python import usage
except ImportError:
    print "Please install twisted"
    sys.exit(1)


class Options(usage.Options):
    optParameters = [["settings", "f", "settings.json", "Path to settings file"]]

class MSUDPHandler(DatagramProtocol):
    def __init__(self, settings):
        if os.path.isfile(settings):
            self.instances = json.load(open(settings, 'r'))
        else:
            print "Unable to load instances list from %s\n" % settings
            sys.exit(1)
        self.tmpl = "ServerName;%s;InstanceName;%s;IsClustered;No;Version;11.0.3000.0;tcp;%s;;"


    def datagramReceived(self, data, (host, port)):
        action, client_msg = struct.unpack('B%ds' % len(data[1:]), data)
        client_msg = client_msg.lower().rstrip()[:-1]
        if action == 4:
            if client_msg in self.instances:
                msg = self.tmpl % (instances[client_msg]['host'].upper(), client_msg.upper(), instances[client_msg]['port'])
                msg = struct.pack('<Bh%ds' % len(msg), 5,len(msg), msg)
                self.transport.write(msg, (host, port))
        elif action == 3:
            msg = ''
            for k, v in self.instances.items():
                msg += str(self.tmpl % (v['host'], k, v['port']))
            msg = struct.pack('<Bh%ds' % len(msg), 5,len(msg), msg)
            self.transport.write(msg, (host, port))


class MSServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "mssqlnameservice"
    description = "Provide MSSQL browser fuctionality"
    options = Options

    def makeService(self, options):
        return internet.UDPServer(1434, MSUDPHandler(options["settings"]))


serviceMaker = MSServiceMaker()

