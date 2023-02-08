import mymodule as mod
from pprint import pprint

while True:
    location = input("Enter a location: ").strip()
    if location:
        pprint(mod.current_weather(location))
    else:
        break
