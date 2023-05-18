import argparse


class TLB:
    def __init__(self):
        self.maxSize = 16
        self.currentSize = 0
        self.queue = []

    def getAddress(self, virtualAddress):



class Entry:

    def __init__(self, virtual=0, physical=0):
        self.virtual = virtual
        self.physical = physical

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

