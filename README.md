# UChicago Trading Competition Bot - Team TexasTech

This project contains our custom trading bot implementation for the UChicago 2025 Trading Competition.  
It uses live market data, gRPC communication, and structured/unstructured news to make algorithmic trading decisions across five assets.

---

##  Overview

Our bot trades in a simulated market of five tickers:  
`APT`, `AKAV`, `DLR`, `MKJ`, and `AKIM`.

We implement a **multi-strategy trading system** where each team member contributed logic for:

- Smart limit/market order trading
- Risk-controlled stop-loss protection
- Swap utilization to maintain balance
- Trend/momentum-based allocations
- Dynamic short-covering and position exit strategies

All logic is contained within one bot and run from a **single virtual machine (VM)** using Python 3.

---

##  Folder Structure
utcxchangelib/ └── utcxchangelib/ ├── examples/ │ └── example_bot.py ← our custom bot ├── xchange_client.py ← base class for client ├── phoenixhood_api.py ← Flask interface (for dashboard) └── ...


---

##  Getting Started

> This assumes Python 3.9+ and `pip` are installed.

1. **Clone the Repository**

```bash
git clone https://github.com/YOUR_USERNAME/uchicago-trading-bot.git
cd uchicago-trading-bot
```
2. **Create and Activate Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows
```
3. **Install Dependencies**
```bash
pip install -e .
pip install flask flask_sse flask_cors requests pandas grpcio protobuf
```
4. **Run the Bot Locally**
```bash
cd utcxchangelib/utcxchangelib/examples
python example_bot.py
```
## Running on Competition VM
1. **SSH into Your Team's VM**
```bash
ssh utc@YOUR_VM_IP
```
2. **Navigate to Bot Folder**
```bash
cd utcxchangelib/utcxchangelib/examples
```
3. **Run the Bot with Phoenixhood (Dashboard)**:
```bash
python3 example_bot.py --phoenixhood True
```
4. **View Dashboard:**
```bash
http://YOUR_VM_IP:3000
```
---
##  Technologies Used
- Python 3
- gRPC
- Flask(Phoenixhood UI)
- Pandas, NumPy
- protobuf, grpcio
- SSE, CORS, Requests
---
## Goal

Maximize total portfolio value across rounds by combining multiple trading philosophies and strategies into a single intelligent system.

---
## Notes

- The bot reads real-time news events and reacts accordingly.
- Risk thresholds and swap logic and are customizable in `trade()` method.
- Phoenixhood provides live feedback on order book and positions.
 ---

## Acknowledgements

We would like to thank:

- The organizers of the **UChicago Trading Competition 2025** for the opportunity to participate.
- The tech team for maintaining the exchange infrastructure and Phoenixhood interface.
- Our mentors, classmates, and peers who helped us refine our strategy.
- The developers of the open-source `utcxchangelib` library that served as the foundation of this project.

Special thanks to the competition staff for rapid responses, debugging help, and clear documentation throughout the event.



