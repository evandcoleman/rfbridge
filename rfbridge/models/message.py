#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class Message:
    messageType = dict(
        status = 'status',
        command = 'command'
    )

    def __init__(self, messageType, data):
        self.type = messageType
        self.data = data

    def as_json(self):
        return json.dumps({
            'type': self.type,
            'data': self.data
        })
