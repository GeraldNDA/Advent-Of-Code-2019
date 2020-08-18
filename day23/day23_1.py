#!/usr/bin/env python3
# Imports
from collections import deque, defaultdict, namedtuple

from intcode_parser import IntComputer
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=23)
puzzle_input = puzzle.get_input()

# Actual Code
class NetworkComputer(object):
    def __init__(self, ip, nic, port):
        self.ip = ip
        self.port = port
        packet_getter = self.get_packets()
        self.nic = IntComputer(
            code=nic,
            inputs=lambda _: next(packet_getter)
        )
        self.idle = False
        self.idle_time = 0
    
    def get_packets(self):
        yield self.ip
        while True:
            self.is_recieving = True
            pkg = self.port()
            if pkg.ip != Network.INVALID_IP:
                yield pkg.x
                yield pkg.y
            else:
                self.idle_time += 1
                if self.idle_time >= Network.IDLE_TIMEOUT:
                    self.idle = True 
                yield -1

    def step_process(self):
        for _ in self.nic:
            if len(self.nic.outputs) == 3:
                self.idle = False
                self.idle_time = 0
                self.port(Network.Message(*self.nic.outputs))
                self.nic.outputs = []
            yield

    def __repr__(self):
        return f"NetworkComputer(ip={self.ip})"

class Network(object):
    Message = namedtuple("Message", ("ip", "x", "y"))
    Message.__new__.__defaults__ = (None, None, None)
    INVALID_IP = -1
    IDLE_TIMEOUT = 5
    NAT_ADDRESS = 255

    def __init__(self, num_computers, nic):
        self.computers = [
            NetworkComputer(ip, list(nic), self.get_port(ip))
            for ip in range(num_computers)
        ]
        self.packet_buffer = defaultdict(deque)
        self.packet_buffer[Network.NAT_ADDRESS] = deque([], 1)
        self.last_nat_packet = None
        self.done = False
    
    def get_port(self, ip):
        def port(msg=None):
            if msg:
                self.packet_buffer[msg.ip].append(msg)
                return
            try:
                return self.packet_buffer[ip].popleft()
            except IndexError:
                return Network.Message(ip=Network.INVALID_IP)
        return port
    
    def check_network(self):
        if self.packet_buffer[Network.NAT_ADDRESS]:
            print(self.packet_buffer[Network.NAT_ADDRESS].pop())
            self.done = True

    def run_network(self):
        handles = [comp.step_process() for comp in self.computers]
        while all(handles) and not self.done:
            for idx, handle in enumerate(handles):
                if not handle:
                    continue
                try:
                    next(handle)
                except StopIteration:
                    handles[idx] = None
            self.check_network()

network = Network(50, [int(i) for i in puzzle_input.split(",")])

# Result
print("Simulating ...")
network.run_network()