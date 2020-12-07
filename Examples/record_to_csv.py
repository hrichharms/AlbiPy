from AlbiPy import sniffing_thread
from AlbiPy import HEADERS
from time import sleep

print("Starting sniffing thread...\nHit ctrl-c to stop recording and save results!")
thread = sniffing_thread()
thread.start()

running = True
try:
    sleep(72000000)
except KeyboardInterrupt:
    pass

thread.stop()
print("\nThread stopped!")
orders = thread.get_data()

output_filename = input("Output csv filename: ")
print("Writing data to csv...")
output_file = open(output_filename, "w")
output_file.write(",".join(HEADERS)+"\n")
for order in orders:
    output_file.write(",".join(list(map(str, order.data)))+"\n")
output_file.close()
print("Wrote", len(orders), "datapoints to", output_filename)
