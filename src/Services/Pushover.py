#######################################################################
#
#    Push Service for Enigma-2
#    Coded by betonme (c) 2020 <DannyBoy(at)24h.de>
#    Support: 
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#######################################################################

# Config
from Components.config import config, NoSave, ConfigText, ConfigPassword

# Plugin internal
from Plugins.Extensions.PushService.ServiceBase import ServiceBase

# Plugin specific
import httplib, urllib


# Constants
PUSHOVER_TITLE_TEMPLATE = _("{name:s} - {plugin:s}")


class Pushover(ServiceBase):
    ForceSingleInstance = True

    def __init__(self):
        # Is called on instance creation
        ServiceBase.__init__(self)

        # Default configuration
        self.setOption('token', NoSave(ConfigPassword(default="<API Token>", fixed_size=False)), "")
        self.setOption('user', NoSave(ConfigPassword(default="<User Token>", fixed_size=False)), "")
        self.setOption('sound', NoSave(ConfigText(default="cashregister", fixed_size=False)), "cashregister")

    def push(self, callback, errback, pluginname, subject, body="", attachments=[]):
        from Plugins.Extensions.PushService.plugin import NAME

        poconf = {}
        poconf["token"] = self.getValue('token')
        poconf["user"] = self.getValue('user')
        poconf["sound"] = self.getValue('sound')

        # Send message
        print _("PushService Pushover: Sending message: %s") % subject
        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request("POST", "/1/messages.json",
                     urllib.urlencode({
                         "token": self.getValue('token'),
                         "user": self.getValue('user'),
                         "message": subject,
                         "title":  PUSHOVER_TITLE_TEMPLATE.format( **{'name': config.pushservice.boxname.value, 'plugin': NAME} ),
                         "sound": self.getValue('sound')
                     }), {"Content-type": "application/x-www-form-urlencoded"})
        response = conn.getresponse()

        if response.status == 200:
            callback(response.reason)
        else:
            errback(response.reason)

