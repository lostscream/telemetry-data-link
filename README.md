# Real-Time Telemetry Data Link & Ground Control Station

A lightweight, low-bandwidth binary telemetry transmission framework designed for rocketry and UAV avionics.

## Features
- **Binary Struct Serialization:** Packs telemetry (packet counter, altitude, velocity, battery voltage, flight state) into compact 16-byte payloads using Python's `struct` module.
- **Data Integrity:** Real-time XOR checksum calculation and verification to detect packet corruption over lossy RF links.
- **Non-Blocking Architecture:** Multithreaded socket listener decoupled from the GUI rendering loop.
- **Real-Time Visualization:** Live graphical plotting and monitoring of telemetry data.

## Architecture
- `roket_sim.py`: Simulates onboard avionics, flight dynamics, and telemetry transmitter.
- `yer_istasyonu.py`: Asynchronous Ground Control Station (GCS) receiver and dashboard.

## Usage
1. Run the ground station:
   ```bash
   python yer_istasyonu.py
