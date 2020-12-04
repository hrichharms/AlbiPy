## What is AlbiPy?
AlbiPy is a network sniffing tool that allows direct access to Albion Online's market data through the Python programming language.

## What can I access with AlbiPy?
The AlbiPy sniffing thread class allows quick and easy access to datapoint directly from the Albion Online client's network traffic. AlbiPy listens on the Albion Online client's UDP socket in order to record and parse information as it is passed to the game client. AlbiPy gives direct access to the following data on every market order sent to the client:
- Order Id
- Silver Per Unit
- Total Silver
- Item Amount
- Item Tier
- Order Type
- Buyer/Seller Name
- Item Enchantment
- Item Quality
- Order Expiry Date

and more...

## What are the limits of AlbiPy?
AlbiPy isn't perfect. Because the market data is sent to the client through the UDP protocol, some of the data is scrambled or hard to read. AlbiPy does make some attempts to correct errors that are easy to fix, however there are still packets that AlbiPy cannot parse. These packets, however, are almost never the first packets received by the client and as a result, the most important orders are almost universaly understood. Should any user wish to build there own parser, manually review malformed logs, or simply meditate on the imperfect nature of reality, however, the packets that AlbiPy is unable to parse are kept along with the raw logs themselves.
