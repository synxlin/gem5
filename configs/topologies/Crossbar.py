# Copyright (c) 2010 Advanced Micro Devices, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Steve Reinhardt

from m5.params import *
from m5.objects import *

from BaseTopology import BaseTopology

class Crossbar(BaseTopology):
    description='Crossbar'

    def __init__(self, controllers):
        self.nodes = controllers

    def makeTopology(self, options, IntLink, ExtLink, Router):
        # Create an individual router for each controller plus one more for the
        # centralized crossbar.  The large numbers of routers are needed because
        # external links do not model outgoing bandwidth in the simple network, but
        # internal links do.

        routers = [Router(router_id=i) for i in range(len(self.nodes)+1)]
        ext_links = [ExtLink(link_id=i, ext_node=n, int_node=routers[i])
                        for (i, n) in enumerate(self.nodes)]
        link_count = len(self.nodes)
        xbar = routers[len(self.nodes)] # the crossbar router is the last router created
        int_links = [IntLink(link_id=(link_count+i),
                             node_a=routers[i], node_b=xbar)
                        for i in range(len(self.nodes))]

        return routers, int_links, ext_links
