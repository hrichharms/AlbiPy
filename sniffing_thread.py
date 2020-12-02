import socket
import json
import threading
from datetime import datetime

PROBLEMS = ["'", "$", "QH", "?8", "H@", "ZP"]

class datapoint:
    """ Single market datapoint including all available data from the game's api"""
    def __init__(self, data):
        self.Id = data[0]
        self.UnitPriceSilver = data[1]
        self.TotalPriceSilver = data[2]
        self.Amount = data[3]
        self.Tier = data[4]
        self.IsFinished = data[5]
        self.AuctionType = data[6]
        self.HasBuyerFetched = data[7]
        self.HasSellerFetched = data[8]
        self.SellerCharacterId = data[9]
        self.SellerName = data[10]
        self.BuyerCharacterId = data[11]
        self.BuyerName = data[12]
        self.ItemTypeId = data[13]
        self.ItemGroupTypeId = data[14]
        self.EnchantmentLevel = data[15]
        self.QualityLevel = data[16]
        self.Expires = data[17]
        self.ReferenceId = data[18]


class sniffer_data:
    """ Organized sniffed market data"""
    def __init__(self, N, E, parsed, malformed):
        self.N = N
        self.E = E
        self.parsed = parsed
        self.malformed = malformed

    def __getitem__(self, i):
        return self.parsed[i]

    def __len__(self):
        return len(self.parsed)


class sniffing_thread(threading.Thread):
    """ Sniffing thread class"""

    def __init__(self, problems=PROBLEMS):
        # initialize thread
        threading.Thread.__init__(self)

        # set thread id
        self.threadID = 1

        # set problems list
        self.problems = problems

        # define thread attributes
        self.E = 0
        self.N = 0
        self.parsed = []
        self.malformed = []
        self.recording = False
        self.last_parsed = True
        self.sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        # log list with placeholder entry
        self.logs = [""]


    def run(self):

        # set recording to True
        self.recording = True

        # while the thread is set to recording, sniff and record data
        while self.recording:

            # wait for market data
            data = self.sniffer.recvfrom(1250)[0]

            # remove known problematic strings from data
            data = str(data)
            for p in self.problems:
                data = data.replace(p, "")

            # partition received cleaned data into chunks
            chunks = [s[3:] for s in data.split("\\") if len(s) > 5 and ("Silver" in s or "ReferenceId" in s)]

            # processed chunks
            for chunk in chunks:
                # if this chunk is the start of a new piece of market information, add a new entry to the log
                if "{" in chunk[:4]:
                    self.logs.append(chunk[chunk.find("{"):])
                # otherwise, this chunk is assumed to be a continuation of the last chunk and is simply concatenated to the end
                elif self.logs:
                    self.logs[-1] += chunk
            
            # set last parsed to false
            self.last_parsed = False

        if self.last_parsed:
            # remove placeholder log entry
            self.logs = self.logs[1:]

            # parse logs, record malformed logs, and count total logs and malformed logs
            self.E = 0
            self.N = len(self.logs)
            self.parsed = []
            self.malformed = []
            for i, log in enumerate(self.logs):
                try:
                    self.parsed.append(datapoint(list(json.loads(log).values())))
                except:
                    self.malformed.append(self.logs.pop(i))
                    self.E += 1


    def parse_current_data(self):
        # if no logs have been recorded
        if self.logs == [""]:
            return sniffer_data(0, 0, [], [])

        # parse logs, record malformed logs, and count total logs and malformed logs
        if not last_parsed:
            self.E = 0
            self.N = 0
            self.malformed = []
            self.parsed = []
            for i, log in enumerate(self.logs):
                try:
                    self.parsed.append(datapoint(list(json.loads(log).values())))
                    self.N += 1
                except:
                    self.malformed.append(self.logs.pop(i))
                    self.E += 1
        
        # return parsed data
        return sniffer_data(self.N, self.E, self.parsed, self.malformed)


    def get_recorded(self):
        return sniffer_data(self.N, self.E, self.parsed, self.malformed)


    def stop(self):
        self.recording = False
