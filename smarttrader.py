import robin_stocks.robinhood as robin
import numpy as np
import pandas as pd
import pyotp
import json
import time
from datetime import datetime

class SmartTrader:
    def __init__(self):
        with open(r'C:\Users\kris2\OneDrive - ENDYNA, INC\Desktop\Final Project R\config.json') as f:
            config = json.load(f)
            self.username = config['ROBINHOOD_USERNAME']
            self.password = config['ROBINHOOD_PASSWORD']
            self.totp_key = config['TOTP_KEY']
        self.logged_in = False
        self.stop_loss = 0.02
        self.take_profit = 0.05

    def login(self):
        totp = pyotp.TOTP(self.totp_key)
        self.login = robin.login(
            username=self.username,
            password=self.password,
            mfa_code=totp.now()
        )
        self.logged_in = True
        print("Login successful!")
        return True

    def get_historical_data(self, symbol, span='day', interval='5minute'):
        try:
            historical = robin.get_stock_historicals(
                [symbol],
                interval=interval,
                span=span,
                bounds='regular'
            )[0]
            
            df = pd.DataFrame(historical)
            df['close_price'] = pd.to_numeric(df['close_price'])
            df['volume'] = pd.to_numeric(df['volume'])
            return df
        except Exception as e:
            print(f"Getting data for {symbol}...")
            time.sleep(1)
            return pd.DataFrame()

    def get_current_price(self, symbol):
        quote = robin.get_latest_price(symbol)
        return float(quote[0])

    def get_buying_power(self):
        account = robin.load_account_profile()
        return float(account['buying_power'])

    def calculate_indicators(self, df):
        if df.empty:
            return None
        
        # Calculate RSI
        delta = df['close_price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # Calculate Volume Average
        volume_avg = df['volume'].mean()
        current_volume = df['volume'].iloc[-1] if not df.empty else 0
        
        # Calculate Price Moving Averages
        sma_20 = df['close_price'].rolling(window=20).mean()
        sma_50 = df['close_price'].rolling(window=50).mean()
        
        return {
            'rsi': rsi.iloc[-1] if not df.empty else 0,
            'volume_ratio': current_volume/volume_avg if volume_avg != 0 else 0,
            'trend': sma_20.iloc[-1] > sma_50.iloc[-1] if not df.empty else False
        }

    def analyze_stock(self, symbol):
        df = self.get_historical_data(symbol)
        current_price = self.get_current_price(symbol)
        indicators = self.calculate_indicators(df)
        
        if indicators:
            signal_strength = 0
            
            # Trend following
            if indicators['trend']:
                signal_strength += 1
                
            # RSI Strategy
            if 30 <= indicators['rsi'] <= 70:
                signal_strength += 1
                
            # Volume confirmation
            if indicators['volume_ratio'] > 1.5:
                signal_strength += 1
            
            return {
                'symbol': symbol,
                'price': current_price,
                'rsi': indicators['rsi'],
                'volume_ratio': indicators['volume_ratio'],
                'signals': signal_strength,
                'recommendation': 'BUY' if signal_strength >= 2 else 'HOLD'
            }
        return None

    def execute_trade(self, symbol, action, quantity=1):
        if action == 'BUY':
            order = robin.order_buy_market(symbol, quantity)
            print(f"Bought {quantity} shares of {symbol}")
            return order
        elif action == 'SELL':
            order = robin.order_sell_market(symbol, quantity)
            print(f"Sold {quantity} shares of {symbol}")
            return order

    def run_strategy(self, watchlist=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']):
        print("\n=== Smart Trading Analysis ===")
        print(f"{'Symbol':<10} {'Price':<10} {'RSI':<10} {'Volume Ratio':<15} {'Signals':<10} {'Action':<10}")
        print("-" * 65)
        
        opportunities = []
        for symbol in watchlist:
            analysis = self.analyze_stock(symbol)
            if analysis:
                print(f"{symbol:<10} ${analysis['price']:<9.2f} {analysis['rsi']:<9.2f} "
                      f"{analysis['volume_ratio']:<14.2f} {analysis['signals']:<10} "
                      f"{analysis['recommendation']:<10}")
                
                if analysis['recommendation'] == 'BUY':
                    opportunities.append(analysis)
            
            time.sleep(1)  # Prevent rate limiting
        
        return opportunities

def main():
    trader = SmartTrader()
    if trader.login():
        while True:
            try:
                opportunities = trader.run_strategy()
                buying_power = trader.get_buying_power()
                
                for op in opportunities:
                    if op['recommendation'] == 'BUY' and buying_power > op['price']:
                        trader.execute_trade(op['symbol'], 'BUY')
                        buying_power -= op['price']
                
                print("\nWaiting for next analysis cycle...")
                time.sleep(300)  # 5 minute delay between cycles
                
            except Exception as e:
                print(f"Error in trading cycle: {str(e)}")
                time.sleep(60)
                continue

if __name__ == "__main__":
    main()
