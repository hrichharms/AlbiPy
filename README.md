## What is AlbiPy?
AlbiPy is a network sniffing tool that allows direct access to the Albion Online Client's market data through the Python programming language.

**Note: For the time being, AlbiPy has been tested on both Linux and Windows. It is not guaranteed to work on previous versions of Windows nor on Mac OS. If anyone wants to work together on testing it for other operating systems I'd be happy to collaborate to port it.**

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

etc.

## What are the limits of AlbiPy?
Since the market data is sent to the client through the UDP protocol, some of the data is scrambled or hard to read. AlbiPy does make some attempts to correct errors that are easy to fix, however there are still packets that AlbiPy cannot parse. These packets, however, are almost never the first packets received by the client and as a result, the most important orders are almost universaly understood. Should any user wish to build their own parser, manually review malformed logs, or simply meditate on the imperfect nature of reality, however, the packets that AlbiPy is unable to parse are kept along with the raw logs themselves.

The methods used to fix problematic strings can sometimes cause problems with accuracy of certain datapoints. As a result, the fix methods are entirely optional and can be switched off should the possibly affected attributes be particularly important for whatever task is at hand.

## How do I run the example scripts?
If you are somebody who doesn't have much experience with coding or are unsure about how AlbiPy works, you may be interested in running some of the provided example scripts. Current examples include:
- **record_to_csv.py** -> Records Albion Online market data until it is switched off, at which point it records that data to a csv file.
- **record_to_csv_live.py** -> While recording Albion Online market data, writes that data to a given csv file every three seconds until it is switched off.

In order to run these scripts, simply download them and put them in the same directory as AlbiPy.py then run the script with Python, which can be downloaded [here](https://www.python.org/downloads/).

## How do I install AlbiPy and use it in my project?
Simply download AlbiPy.py and import it as any other module. **It is importatnt to note that AlbiPy will throw an error and will not work if it is run without administrative privileges.** Below is an example of a script using AlbiPy that imports the module, records network traffic for ten seconds, then outputs the item prices, enchantment levels, and tiers, before exiting.
```Python
from AlbiPy import sniffing_thread
from time import sleep

thread = sniffing_thread()
thread.start()

sleep(10)

thread.stop()
orders = thread.get_data()
for order in orders:
    print(order.UnitPriceSilver, order.EnchantmentLevel, order.Tier)
```
Alternatively, the collected data, including unparsed versions of the logs and malformed orders can be written to json simply by typecasting the sniffer data object to a string then writing it to file.
```Python
from AlbiPy import sniffing_thread
from time import sleep

thread = sniffing_thread()
thread.start()

sleep(10)

thread.stop()
orders = thread.get_data()
output_file = open("output.json", "w")
output_file.write(str(orders))
output_file.close()
```

**Note: The above code and AlbiPy in general can only capture market data that is received by the client while the thread is recording (between thread.start() and thread.stop()).**

## List of datapoint attributes:
- Id -> A unique id for the specific order
- UnitPriceSilver -> The price buying or selling one item from the given market order
- TotalPriceSilver -> The total amount of silver involved in the order
- Amount -> The quantity of items being bought or sold in the order
- Tier -> The tier of the item being bought or sold if applicable
- IsFinished -> Seems more like a backend boolean for the developer's database but I'm not sure
- AuctionType -> Whether this is a buy order or a sell order
- HasBuyerFetched -> If the order is a buy order this is a boolean determining whether the buyer has fetched the order. This seems like a largely backend attribute
- HasSellerFetched -> If the order is a sell order this is a boolean determining whether the seller has fetched the order. This again, seems like a largely backend attribute
- SellerCharacterId -> If the order is a sell order, this is the unique id of the character that posted the sale
- SellerName -> If the order is a sell order, this is the in game name of the character that posted the sale
- BuyerCharacterId -> If the order is a buy order, this is the unique id of the character that posted the buy
- BuyerName -> If the order is a buy order, this is the in game name of the character that posted the buy
- ItemTypeId -> This is the item type identifier. Example: Adept's Longbow with 1 level of enchantment = T4_2H_LONGBOW@1
- ItemGroupTypeId -> Same as ItemTypeId without the enchantment difference
- EnchantmentLevel -> This is the enchantment level of the item being bought or sold if applicable
- QualityLevel -> This is the quality of the item being bought or sold expressed as an integer if applicable
- Expires -> The expiry date of the order
- ReferenceId -> To be totally honest, I have no idea what this is. Probably something for the backend but I really don't know.
