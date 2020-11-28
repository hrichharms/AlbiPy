from datetime import datetime

# function to get the current time
def get_time():
    return str(datetime.now()).split()[1].split(".")[0]+" "