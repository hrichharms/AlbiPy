from AlbiPy import sniffing_thread
from AlbiPy import HEADERS
from time import sleep


def orders_to_csv(orders, filename):
    # open file
    output_file = open(output_filename, "w")

    # write headers to file
    output_file.write(",".join(HEADERS)+"\n")

    # write parsed datapoints to file
    for order in orders:
        output_file.write(",".join(list(map(str, order.data)))+"\n")

    # close output file
    output_file.close()


# get output filename from user
output_filename = input("Output csv filename: ")

# initialize and start sniffing thread
print("Starting sniffing thread...\nHit ctrl-c to stop recording and save results!")
thread = sniffing_thread()
thread.start()

# fetch recorded market orders and write them to file every three seconds
try:
    while True:
        print("Waiting three seconds...")
        sleep(3)

        print("Fetching recorded orders...")
        orders = thread.get_data()

        print("Writing recorded orders to", output_filename)
        orders_to_csv(orders, output_filename)
except KeyboardInterrupt:
    pass

# stop sniffing thread
thread.stop()
print("\nThread stopped!")

# fetch captured data
orders = thread.get_data()

# write any outstanding orders to csv
print("Writing remaining orders to", output_filename)
orders_to_csv(orders, output_filename)
