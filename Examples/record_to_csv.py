from AlbiPy import sniffing_thread
from AlbiPy import HEADERS

# initialize and start sniffing thread
print("Starting sniffing thread...\nHit ctrl-c to stop recording and save results!")
thread = sniffing_thread()
thread.start()

# wait forever until keyboard interupt is detected
try:
    while True: pass
except KeyboardInterrupt:
    pass

# stop sniffing thread
thread.stop()
print("\nThread stopped!")

# fetch captured data and store in orders
orders = thread.get_data()

# get output filename from user
output_filename = input("Output csv filename: ")

print("Writing data to csv...")
# open file
output_file = open(output_filename, "w")

# write headers to file
output_file.write(",".join(HEADERS)+"\n")

# write parsed datapoints to file
for order in orders:
    output_file.write(",".join(list(map(str, order.data)))+"\n")

# close output file
output_file.close()
print("Wrote", len(orders), "datapoints to", output_filename)
