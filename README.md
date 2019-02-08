# python-can-plotter

This tool should help to refactor messages over CAN busses.

## Setup

You need a running python3 with pip3

    sudo apt-get install python3-pip
    
Install some 'matplotlib' via apt

    sudo apt-get install python3-matplotlib

Install 'python-can' via pip

    pip install python-can

There must be a working can device. Change the configuration in 'plotter.py' to match your setup. E.g.

    bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=5000)
    
## Running

    ./plotter.py
    
* Enter `0x123` to plot the ID `0x123`    
* Enter `list` to see all IDs with values > 0
* Enter `changed` to plot all IDs which values have changed since startup
* Enter `all` to plot all IDs
* Enter `is: 12345` to plot all IDs which current value is `12345`
* Enter `quit` to leave the program
