import Queue

def init():     #defines queue objects so they can be used globally
    global commandQueue, outputQueue
    commandQueue = Queue.Queue()
    outputQueue = Queue.Queue()