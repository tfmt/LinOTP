#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    LinOTP - the open source solution for two factor authentication
#    Copyright (C) 2010 - 2016 LSE Leading Security Experts GmbH
#
#    This file is part of LinOTP smsprovider.
#
#    This program is free software: you can redistribute it and/or
#    modify it under the terms of the GNU Affero General Public
#    License, version 3, as published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the
#               GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#    E-mail: linotp@lsexperts.de
#    Contact: www.linotp.org
#    Support: www.lsexperts.de
#
"""
This is a SMS Provide class that can send OTP values via SMS using a phone
that is connected to the LinOTP server

This module makes use of the command line programm gnokii. It gets configured
in a file .gnokiirc file like this:

[global]
model = AT
port = /dev/ttyACM1
connection = serial

"""

import SMSProvider
from SMSProvider import getSMSProviderClass
from SMSProvider import ISMSProvider

import subprocess
import string

import logging
log = logging.getLogger(__name__)


class DeviceSMSProvider(ISMSProvider):
    def __init__(self):
        self.config = {}

    def submitMessage(self, phone, message):
        '''
            submitMessage()
            - send out a message to a phone

        '''
        msisdn = 'true' in ("%r" % self.config.get('MSISDN', "false")).lower()
        if msisdn:
            phone = self._get_msisdn_phonenumber(phone)

        if (not self.config.has_key('CONFIGFILE')):
            log.error("[submitMessage] No config key CONFIGFILE found!")
            return
        else:
            configfile = self.config.get('CONFIGFILE')
            log.info("[submitMessage] setting configfile to %s" % configfile)

        if (self.config.has_key('SMSC')):
                smsc_number=self.config.get('SMSC')
                smsc_option="--setsmsc"

        # NOTE 1: The LinOTP service account need rw-access to /dev/ttyXXX
        # NOTE 2: we need gnokii 0.6.29, since 0.6.28 will crash with a bug

        # FIXME: Das blockiert hier noch!
        #args = ['gnokii', "--config", configfile, "--sendsms", phone]
        #log.info("[submitMessage] preparing to run : %s" % string.join(args) )
        #proc = subprocess.Popen(args,shell=False,stdin=subprocess.PIPE)
        #log.info("process run. Now sending message as input into pipe")
        #proc.communicate(message+"\n")

        command = ("echo %s | gnokii --config %s --sendsms %s %s %s"
                   % (message, configfile, phone, smsc_option, smsc_number))
        log.debug("[submitMessage] running command: %s" % command)
        proc = subprocess.Popen([command], shell=True)

    def loadConfig(self, configDict):
        self.config = configDict
        log.info("loading config for DeviceSMSProvider")



def main(phone, message):
    print "SMSProvider - class load test "

    # echo "text" | gnokii --config <filename> <ziel>

    config = {'CONFIGFILE':'/home/user/.gnokiirc',
              }


    sms = getSMSProviderClass("DeviceSMSProvider", "DeviceSMSProvider")()

    sms.loadConfig(config)
    ret = sms.submitMessage(phone, message)
    print sms


if __name__ == "__main__":
    phone = "+4901234567890"
    #phone      = "015154294800"
    message = "DeviceSMSProviderClass test. blocking. :-/"
    main(phone, message)
    print "... done!"

