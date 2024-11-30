import robin_stocks.robinhood as robin
import json
import pyotp
import time

class BTCBuyer:
    def __init__(self):
        with open(r'C:\Users\kris2\OneDrive - ENDYNA, INC\Desktop\Final Project R\config.json') as f:
            config = json.load(f)
            self.username = config['ROBINHOOD_USERNAME']
            self.password = config['ROBINHOOD_PASSWORD']
            self.totp_key = config['TOTP_KEY']
        self.logged_in = False
        self.usd_amount = 100.00  # $100 USD investment
        self.profit_target = 0.01  # 1% profit target
        self.stop_loss = -0.0002  # -0.02% stop loss
        self.purchase_price = 0

    def login(self):
        totp = pyotp.TOTP(self.totp_key)
        self.login = robin.login(
            username=self.username,
            password=self.password,
            mfa_code=totp.now()
        )
        self.logged_in = True
        print("Ready to trade BTC!")
        return True

    def get_btc_price(self):
        quote = robin.get_crypto_quote('BTC')
        current_price = float(quote['mark_price'])
        print(f"Current BTC Price: ${current_price:,.2f}")
        return current_price

    def execute_btc_buy(self):
        self.purchase_price = self.get_btc_price()
        btc_quantity = self.usd_amount / self.purchase_price
        
        print(f"\nExecuting purchase of ${self.usd_amount:.2f} worth of BTC")
        print(f"Purchase price: ${self.purchase_price:,.2f}")
        print(f"Estimated BTC amount: {btc_quantity:.8f} BTC")
        
        order = robin.order_buy_crypto_by_price('BTC', self.usd_amount)
        
        print("\nOrder Details:")
        print(f"Status: {order['state']}")
        print(f"Type: {order['type']}")
        print(f"Side: {order['side']}")
        
        return order

    def monitor_profit(self):
        while True:
            current_price = self.get_btc_price()
            profit_percentage = (current_price - self.purchase_price) / self.purchase_price
            
            print(f"Current Profit: {profit_percentage*100:.4f}%")
            
            if profit_percentage >= self.profit_target:
                print("🎯 Profit target reached! Selling BTC...")
                self.execute_btc_sell("PROFIT")
                break
            elif profit_percentage <= self.stop_loss:
                print("🛑 Stop loss triggered! Selling BTC...")
                self.execute_btc_sell("STOP LOSS")
                break
                
            time.sleep(60)  # Check every minute

    def execute_btc_sell(self, reason):
        holdings = robin.get_crypto_positions()
        for holding in holdings:
            if holding['currency']['code'] == 'BTC':
                quantity = float(holding['quantity'])
                order = robin.order_sell_crypto_by_quantity('BTC', quantity)
                print(f"Sold BTC position! Reason: {reason}")
                final_profit = (float(order['price']) - self.purchase_price) / self.purchase_price * 100
                print(f"Final Profit: {final_profit:.4f}%")
                return order

def main():
    buyer = BTCBuyer()
    buyer.login()
    buyer.execute_btc_buy()
    buyer.monitor_profit()

if __name__ == "__main__":
    main()
