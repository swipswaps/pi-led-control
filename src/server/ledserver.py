#!/usr/bin/python3
# Copyright (c) 2016 Sebastian Kanis
# This file is part of pi-led-control.

# pi-led-control is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pi-led-control is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pi-led-control.  If not, see <http://www.gnu.org/licenses/>.

from http.server import HTTPServer
import logging
import os

from server.piledhttprequesthandler import PiLEDHTTPRequestHandler


class LEDServer(HTTPServer):

    def __init__(self, connection, ledManager, configManager):
        super().__init__(connection, PiLEDHTTPRequestHandler)
        self.ledManager = ledManager
        self.config = configManager
                
    def serve_forever(self, poll_interval=0.5):
        logging.info("running %s from %s at %s:%s", __name__, os.path.dirname(os.path.realpath(__file__)), self.server_name, self.server_port)
        HTTPServer.serve_forever(self, poll_interval=poll_interval)
        
    def server_close(self):
        HTTPServer.server_close(self)
        logging.info("%s stopped, was running from %s at %s:%s", __name__, os.path.dirname(os.path.realpath(__file__)), self.server_name, self.server_port)
