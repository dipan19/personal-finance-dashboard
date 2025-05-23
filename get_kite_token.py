from kiteconnect import KiteConnect

api_key = "mih4xn8w7ngeo4cn"

kite = KiteConnect(api_key=api_key)
print("Login URL:", kite.login_url())