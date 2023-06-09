import argparse

class TLB:
    def __init__(self, algo, physMem):
        self.table = [None] * 256
        self.queue = []
        self.physMem = min(16, physMem)
        self.algo = algo
        self.size = 0

    def getFrame(self, address, history):
        pageNum = address // 256
        if self.table[pageNum] is not None:
            return True
        if self.algo == "FIFO":
            if self.size < self.physMem:
                self.table[pageNum] = 1
                self.size += 1
            else:
                evictNum = self.queue.pop(0)
                self.table[pageNum] = evictNum
                self.table[evictNum] = None
            self.queue.append(pageNum)
            return False

        if self.algo == "OPT" or self.algo == "LRU":
            if self.size < self.physMem:
                self.table[pageNum] = self.size
                memLoc = self.size
                self.size += 1
            else:
                pageList = []
                for i in range(len(self.table)):
                    if self.table[i] is not None:
                        pageList.append(i)
                for address in history:
                    if len(pageList) == 1:
                        break
                    if address // 256 in pageList:
                        pageList.remove(address // 256)
                evictNum = pageList.pop(0)
                memLoc = self.table[evictNum]
                self.table[pageNum] = memLoc
                self.table[evictNum] = None
            return False


class PageTable:
    def __init__(self, algo, physMem):
        self.table = [None] * 256
        self.queue = []
        self.algo = algo
        self.physMem = physMem
        self.size = 0

    def getFrameTlbHit(self, address):
        return self.table[address // 256]

    def getFrame(self, address, history):
        pageNum = address // 256
        if self.table[pageNum] is not None:
            return True, self.table[pageNum]

        if self.algo == "FIFO":
            memLoc = 0
            if self.size < self.physMem:
                self.table[pageNum] = self.size
                memLoc = self.size
                self.size += 1
            else:
                evictNum = self.queue.pop(0)
                memLoc = self.table[evictNum]
                self.table[pageNum] = memLoc
                self.table[evictNum] = None
            self.queue.append(pageNum)
            return False, memLoc

        if self.algo == "OPT" or self.algo == "LRU":
            if self.size < self.physMem:
                self.table[pageNum] = self.size
                memLoc = self.size
                self.size += 1
            else:
                pageList = []
                for i in range(len(self.table)):
                    if self.table[i] is not None:
                        pageList.append(i)
                for address in history:
                    if len(pageList) == 1:
                        break
                    if address // 256 in pageList:
                        pageList.remove(address // 256)
                evictNum = pageList.pop(0)
                memLoc = self.table[evictNum]
                self.table[pageNum] = memLoc
                self.table[evictNum] = None
            return False, memLoc


class BackingStore:
    def __init__(self):
        self.maxSize = 65536
        self.blockSize = 256
        self.data = []
        self.readfromfile()

    def readfromfile(self):
        # Read the binary file
        with open('BACKING_STORE.bin', 'rb') as file:
            for _ in range(self.blockSize):
                array_data = file.read(self.blockSize)
                self.data.append(array_data)

    def getData(self, address):
        block = self.data[address // self.blockSize]
        return block, block[address % self.blockSize]


def main():
    parser = argparse.ArgumentParser(description='Scheduler Simulator')

    # add arguments for the job file, algorithm, and quantum
    parser.add_argument('refFile', metavar='addresses.txt', type=str,
                        help='list of addresses')

    parser.add_argument('frames', metavar='FRAMES', type=int,
                        help='number of frames in physical memory', default=256)

    parser.add_argument('pra', metavar='PRA', type=str, default="FIFO",
                        help='algorithm for page table replacement')
    args = parser.parse_args()
    print(args.pra, args.frames, args.refFile)

    backingStore = BackingStore()
    pageTable = PageTable(args.pra, args.frames)
    tlb = TLB(args.pra, args.frames)

    addresses = []
    with open(args.refFile, 'r') as file:
        for line in file:
            integer = int(line.strip())
            addresses.append(integer)

    tlbMiss = 0
    pageFault = 0
    for i in range(len(addresses)):
        #if using OPT, use the substring from that element forward
        if pageTable.algo == "OPT":
            history = addresses[i+1:]
        #if using least recently used, use the substring form that element backwards in reversed order
        elif pageTable.algo == "LRU":
            history = addresses[:i]
            history.reverse()
        else:
            history = None

        block, value = backingStore.getData(addresses[i])
        if not tlb.getFrame(addresses[i], history):
            tlbMiss += 1
            result, memloc = pageTable.getFrame(addresses[i], history)
            if not result:
                pageFault += 1
        else:
            memloc = pageTable.getFrameTlbHit(addresses[i])
        integers = [str(addresses[i]), str(value) if value < 127 else str(value-256), str(memloc), "\n" + str("".join([hex(byte)[2:].zfill(2) for byte in block]).upper())]
        formatedstr = ', '.join(integers)
        print(formatedstr)
    print("Number of Translated Addresses =", len(addresses))
    print("Page Faults =", pageFault)
    print("Page Fault Rate = %3.3f" % (pageFault/len(addresses)))
    print("TLB Hits =", len(addresses) - tlbMiss)
    print("TLB Misses =", tlbMiss)
    print("TLB Hit Rate = %3.3f" % ((len(addresses) - tlbMiss) / len(addresses)))


if __name__ == '__main__':
    main()

