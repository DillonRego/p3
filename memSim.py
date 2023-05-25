import argparse
    
class TLB:
    def __init__(self):
        self.maxSize = 16
        self.currentSize = 0
        self.queue = []

    def getAddress(self, virtualAddress):
        for i in self.queue:
            if i.virtual == virtualAddress:
                return i
    
    def insert(self):
        pass

class PageTable:
    def __init__(self, algo, physMem):
        self.table = [None] * 256
        self.queue = []
        self.algo = algo
        self.physMem = physMem
        self.size = 0

    def getFrame(self, address, history):
        pageNum = address // 256
        if table[pageNum] == 1:
            return True

        if self.algo == "FIFO":
            if self.size < self.physMem:
                table[pageNum] = 1
                self.size += 1
            else:
                evictNum = self.queue.pop(0)
                table[evictNum] = 0
            self.queue.append(pageNum)
            return False

        if self.algo == "LRU":
            if self.size < self.physMem:
                table[pageNum] = 1
                self.size += 1
            else:
                evictNum = self.queue.pop(0)
                table[evictNum] = 0
            self.queue.append(pageNum)
            return False

        if self.algo == "OPT":
            if self.size < self.physMem:
                table[pageNum] = 1
                self.size += 1
            else:
                pageList = []
                for i in range(len(table)):
                    if table[i] == 1:
                        pageList.append(i)
                for address in history:
                    if len(pageList) == 1:
                        break
                    if address // 256 in pageList:
                        pageList.remove(address // 256)
                evictNum = pageList.pop(0)
                table[evictNum] = 0
            return False







class BackingStore:
    def __init__(self):
        self.maxSize = 65536
        self.blockSize =256
        self.data = []

    def readfromfile(self):
        # Read the binary file
        with open('BACKING_STORE.bin', 'rb') as file:
            for _ in range(self.blockSize):
                array_data = file.read(self.blockSize)
                array = [byte for byte in array_data]
                self.data.append(array)

    def getBlock(self, address):
        return address // self.blockSize




def main():
    parser = argparse.ArgumentParser(description='Scheduler Simulator')

    # add arguments for the job file, algorithm, and quantum
    parser.add_argument('refFile', metavar='job-file.txt', type=str,
                        help='the file containing the list of jobs')

    parser.add_argument('frames', metavar='FRAMES', type=int,
                        help='the scheduling algorithm to use', default=256)

    parser.add_argument('pra', metavar='PRA', type=str, default="FIFO",
                        help='the quantum for the round-robin algorithm')
    args = parser.parse_args()
    print(args.pra, args.frames, args.refFile)


if __name__ == '__main__':
    main()

