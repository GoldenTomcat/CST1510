import threading


class Threading:
    """Class for the threads. This allows for the creation and starting of threads. Daemon specification
    is included."""

    def __init__(self, thread, flag):
        self.target_process = thread
        self.thread = threading.Thread(target=self.target_process)
        # Flag is Boolean value for if thread is daemon
        # Daemons will be need on client and server network processes to make sure threads terminate when -
        # main program exits.
        self.thread.daemon = flag

    def start_thread(self):
        self.thread.start()
        """Start thread method. Starts the thread on the Target process."""


# threading.Thread.daemon = True
