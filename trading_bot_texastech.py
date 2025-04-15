from typing import Optional
import asyncio
import argparse
import logging
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utcxchangelib.xchange_client import XChangeClient, Side

logging.basicConfig(level=logging.INFO)
_LOGGER = logging.getLogger("team-texastech-bot")
_LOGGER.setLevel(logging.INFO)


class MyXchangeClient(XChangeClient):

    def __init__(self, host: str, username: str, password: str):
        super().__init__(host, username, password)

    async def bot_handle_cancel_response(self, order_id: str, success: bool, error: Optional[str]) -> None:
        order = self.open_orders[order_id]
        print(f"{'Market' if order[2] else 'Limit'} Order ID {order_id} cancelled, {order[1]} unfilled")

    async def bot_handle_order_fill(self, order_id: str, qty: int, price: int):
        print("Order fill:", self.positions)

    async def bot_handle_order_rejected(self, order_id: str, reason: str) -> None:
        print("Order rejected because of", reason)

    async def bot_handle_trade_msg(self, symbol: str, price: int, qty: int):
        pass

    async def bot_handle_book_update(self, symbol: str) -> None:
        pass

    async def bot_handle_swap_response(self, swap: str, qty: int, success: bool):
        pass

    async def bot_handle_news(self, news_release: dict):
        # Handles news with possible "type": Exchange Alert, News, or Tweet
        news_type = news_release["kind"]
        news_data = news_release["new_data"]
        print(f"Received {news_type}: {news_data.get('content', '')}")

    async def connect(self):
        while True:
            try:
                _LOGGER.info("Attempting to connect to server...")
                await super().connect()
            except Exception as e:
                _LOGGER.error(f"Connection lost: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)

    async def trade(self):
        await asyncio.sleep(0.5)
        print("Starting multi-strategy trading sequence...")

        book = self.order_books.get("APT")
        if not (book and book.asks and book.bids):
            print("APT book not ready.")
            return

        best_ask = min(book.asks.keys())
        best_bid = max(book.bids.keys())

        # ==========================
        # Strategy 1: Risk control (Peace)
        # ==========================
        if self.positions['cash'] < 1000:
            print("Low cash — skipping risky trades.")
            return
        if abs(self.positions['APT']) > 1000:
            print("Excessive APT position — pausing trades.")
            return

        # ==========================
        # Strategy 2: Smart orders (Joanna)
        # ==========================
        await self.place_order("APT", 3, Side.BUY, best_bid + 1)
        await asyncio.sleep(0.5)
        await self.place_order("APT", 3, Side.SELL, best_ask - 1)
        await asyncio.sleep(0.5)

        await self.place_swap_order('toAKAV', 1)
        await asyncio.sleep(0.5)
        await self.place_swap_order('fromAKAV', 1)
        await asyncio.sleep(0.5)

        # ==========================
        # Strategy 3: Momentum (Ohi)
        # ==========================
        recent_momentum = best_bid - best_ask
        if recent_momentum > 2:
            print("Uptrend detected — buying more.")
            await self.place_order("APT", 5, Side.BUY)
        elif recent_momentum < -2:
            print("Downtrend detected — selling more.")
            await self.place_order("APT", 5, Side.SELL)
        await asyncio.sleep(1)

        # ==========================
        # Strategy 4: Smart short cover (Joanna)
        # ==========================
        entry_price = best_bid
        cover_threshold = entry_price + 10

        while self.positions["APT"] < 0:
            await asyncio.sleep(3)
            book = self.order_books.get("APT")
            if book and book.asks:
                current_ask = min(book.asks.keys())
                if current_ask > cover_threshold:
                    print(f"Covering short at {current_ask}")
                    await self.place_order("APT", abs(self.positions["APT"]), Side.BUY)
                    break

        # ==========================
        # Strategy 5: Position balancing (Chioma)
        # ==========================
        if self.positions["APT"] > 50:
            print("Trimming long APT position...")
            await self.place_order("APT", 25, Side.SELL)
        elif self.positions["APT"] < -50:
            print("Covering excessive short...")
            await self.place_order("APT", 25, Side.BUY)

        print("Finished trade cycle.\n")

    async def view_books(self):
        while True:
            await asyncio.sleep(3)
            for symbol, book in self.order_books.items():
                print(f"{symbol} Bids:", sorted(book.bids.items(), reverse=True))
                print(f"{symbol} Asks:", sorted(book.asks.items()))

    async def start(self, user_interface):
        asyncio.create_task(self.trade())
        if user_interface:
            self.launch_user_interface()
            asyncio.create_task(self.handle_queued_messages())
        await self.connect()


async def main(user_interface: bool):
    # Use actual server values when running live
    SERVER = 'INSERT_SERVER_URL_HERE'
    my_client = MyXchangeClient(SERVER, "YOUR_USERNAME", "YOUR_PASSWORD")
    await my_client.start(user_interface)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run trading bot with optional Phoenixhood UI")
    parser.add_argument("--phoenixhood", required=False, default=False, type=bool, help="Starts Phoenixhood if True")
    args = parser.parse_args()

    user_interface = args.phoenixhood
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main(user_interface))

