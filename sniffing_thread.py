import socket
import json
import threading

PROBLEMS = ["'", "$", "QH", "?8", "H@", "ZP"]

class sniffing_thread(threading.Thread):

    # override the initialization method
    def __init__(self):
        # initialize thread
        threading.Thread.__init__(self)

        # set thread id
        self.threadID = 1

        # define thread attributes
        self.recording = False
        self.sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        # log list with placeholder entry
        self.logs = [""]


    # override the run method
    def run(self):

        # set recording to True
        self.recording = True

        # while the thread is set to recording, sniff and record data
        while self.recording:

            # wait for market data
            data = self.sniffer.recvfrom(1250)[0]

            # remove known problematic strings from data
            data = str(data)
            for p in PROBLEMS:
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
        
        # remove placeholder log entry
        self.logs = self.logs[1:]

        # parse logs, record malformed logs, and count total logs and malformed logs
        self.E = 0
        self.N = len(self.logs)
        self.malformed = []
        self.parsed = []
        for i, log in enumerate(self.logs):
            try:
                self.parsed.append(json.loads(log))
            except:
                self.malformed.append(self.logs.pop(i))
                self.E += 1


    # parse current data
    def parse_current_data(self):
        # if no logs have been recorded
        if self.logs == [""]:
            return (0, 0, [], [])
        
        # parse logs, record malformed logs, and count total logs and malformed logs
        self.E = 0
        self.N = 0
        self.malformed = []
        self.parsed = []
        for i, log in enumerate(self.logs):
            try:
                self.parsed.append(json.loads(log))
                self.N += 1
            except:
                self.malformed.append(self.logs.pop(i))
                self.E += 1
        
        # return parsed data
        return (self.N, self.E, self.parsed, self.malformed)


    # get recorded data method
    def get_recorded(self):
        return (self.N, self.E, self.parsed, self.malformed)


    # stop recording method
    def stop(self):
        self.recording = False
