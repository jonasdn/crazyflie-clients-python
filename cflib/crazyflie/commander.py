#!/usr/bin/env python
#
#     ||          ____  _ __                           
#  +------+      / __ )(_) /_______________ _____  ___ 
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2011-2013 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
Used for sending control setpoints to the Crazyflie
"""

__author__ = 'Bitcraze AB'
__all__ = ['Commander']

from cflib.crtp.crtpstack import CRTPPacket, CRTPPort
import struct

class Commander():
    """
    Used for sending control setpoints to the Crazyflie
    """

    def __init__(self, crazyflie = None):
        """
        Initialize the commander object. By default the commander is in +-mode (not x-mode).
        """
        self.cf = crazyflie
        self.xMode = False

        """
        Enable/disable the client side X-mode. When enabled this recalculates the setpoints before
        sending them to the Crazyflie.
        """
    def setClientSideXModeEnabled(self, enabled):
        self.xMode = enabled

    def sendControlSetpoint(self, roll, pitch, yaw, thrust):
        """
        Send a new control setpoint for roll/pitch/yaw/thust to the copter
        
        The arguments roll/pitch/yaw/trust is the new setpoints that should be sent to the copter
        """
        if self.xMode:
            roll = 0.707*(roll-pitch)
            pitch = 0.707*(roll+pitch)

        p = CRTPPacket()
        p.setPort(CRTPPort.COMMANDER);
        p.data = struct.pack('<fffH', -pitch, roll, yaw, thrust)
        self.cf.sendLinkPacket(p)