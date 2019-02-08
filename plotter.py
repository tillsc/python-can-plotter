#!/usr/bin/python3

import can
import matplotlib.pyplot as plt
import re

bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=125000)

class MyListener(can.Listener):

    seen = {}
    first_ts = 0

    def on_message_received(self, m):
        if self.first_ts == 0:
            self.first_ts = m.timestamp
        val = int.from_bytes(m.data, byteorder='big', signed=False)
        if m.dlc == 4:
            val = val >> 8
        if m.arbitration_id not in self.seen and val != 0 and val < 10000:
            self.seen[m.arbitration_id] = ([], [])
        if m.arbitration_id in self.seen:    
            self.seen[m.arbitration_id][0].append(m.timestamp - self.first_ts)
            self.seen[m.arbitration_id][1].append(val)

listener = MyListener()
can.Notifier(bus, [listener])

def plot(ids):
    for id in ids:
        plt.plot(listener.seen[id][0], listener.seen[id][1], label=hex(id))
    plt.legend()
    plt.show()

input_id = input("Enter an ID: ")
while input_id != 'quit':
    is_epression_matches = re.search('is: ?([1-9][0-9]*)', input_id)
    if is_epression_matches:
        val = int(is_epression_matches.group(1))
        ids = [id for id in listener.seen if listener.seen[id][1][-1] == val]
        plot(ids)
    elif input_id == 'list':
        print(list(map(lambda item: hex(item[0]) + ": " + str(len(item[1][0])) + ' [' + str(min(item[1][1])) + ':' + str(max(item[1][1])) + ']', listener.seen.items())))
    elif input_id == 'all' or input_id == 'changed':
        for id, data in dict(listener.seen).items():
            if input_id != 'changed' or min(data[1]) != max(data[1]):
                plt.plot(data[0], data[1], label=hex(id))
        plt.legend()    
        plt.show()  
    else:    
      try:
        id = int(input_id, 16)
      except ValueError:
        id = 0
      if id in listener.seen:
        plt.plot(listener.seen[id][0], listener.seen[id][1])
        plt.show()
      else:
        print('Could not find ID ' + input_id)  
    
    input_id = input("Enter an ID: ")
    

