#!/usr/bin/env python3
"""AJAX Pattern Simulation - 非同步請求模擬"""

import json
import time
from typing import Callable, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class RequestState(Enum):
    UNSENT = 0
    OPENED = 1
    HEADERS_RECEIVED = 2
    LOADING = 3
    DONE = 4

@dataclass
class AJAXRequest:
    state: RequestState = RequestState.UNSENT
    status: int = 0
    response_text: str = ""
    onreadystatechange: Optional[Callable] = None
    method: str = ""
    url: str = ""

    def open(self, method: str, url: str, async: bool = True):
        self.state = RequestState.OPENED
        self.method = method
        self.url = url
        self._trigger()

    def send(self, data: Optional[str] = None):
        self.state = RequestState.HEADERS_RECEIVED
        self._trigger()
        self.state = RequestState.LOADING
        self._trigger()
        time.sleep(0.01)
        self.response_text = json.dumps({
            "user": {"id": 1, "name": "John", "email": "john@example.com"},
            "timestamp": datetime.now().isoformat(),
            "data": [1, 2, 3, 4, 5]
        })
        self.state = RequestState.DONE
        self.status = 200
        self._trigger()

    def _trigger(self):
        if self.onreadystatechange:
            self.onreadystatechange()

def demo():
    print("=== AJAX 模式模擬 ===")
    print()

    def make_request():
        req = AJAXRequest()
        req.onreadystatechange = lambda: (
            print(f"State: {req.state.name}, Status: {req.status}")
            if req.state == RequestState.DONE
            else None
        )
        req.open('GET', '/api/data')
        req.send()
        print(f"Response: {req.response_text[:50]}...")
        print()

    print("1. 模擬 GET 請求")
    make_request()

    print("=== 完成 ===")

if __name__ == "__main__": demo()