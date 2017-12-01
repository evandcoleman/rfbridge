#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class Command:
    def __init__(self, cmd):
        self.cmd = cmd

    def as_json(self):
        return json.dumps({
          'cmd': cmd
        })
