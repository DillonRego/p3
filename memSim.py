import argparse


class TLB:
    def __init__(self):
        self.table = [None] * 256
        self.queue = []
        self.physMem = 16
        self.size = 0

    def getFrame(self, address):
        pageNum = address // 256
        if table[pageNum] == 1:
            return True
        if self.size < self.physMem:
            table[pageNum] = 1
            self.size += 1
        else:
            evictNum = self.queue.pop(0)
            table[evictNum] = 0
        self.queue.append(pageNum)
        return False


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

        if self.algo == "OPT" or self.algo == "LRU":
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
        self.readfromfile()

    def readfromfile(self):
        # Read the binary file
        with open('BACKING_STORE.bin', 'rb') as file:
            for _ in range(self.blockSize):
                array_data = file.read(self.blockSize)
                self.data.append([byte for byte in array_data])

    def getData(self, address):
        block = data[address // self.blockSize]
        return block, block[address % self.blockSize]




def main():
    parser = argparse.ArgumentParser(description='Scheduler Simulator')

    # add arguments for the job file, algorithm, and quantum
    parser.add_argument('refFile', metavar='job-file.txt', type=str,
                        help='list of addresses')

    parser.add_argument('frames', metavar='FRAMES', type=int,
                        help='number of frames in physical memory', default=256)

    parser.add_argument('pra', metavar='PRA', type=str, default="FIFO",
                        help='algorithm for page table replacement')
    args = parser.parse_args()
    print(args.pra, args.frames, args.refFile)

    backingStore = BackingStore()
    pageTable = PageTable(args.pra, args.frames)
    tlb = TLB()





if __name__ == '__main__':
    main()

