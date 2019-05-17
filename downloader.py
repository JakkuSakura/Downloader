#coding: utf-8
import requests
import threading
import time
import os
def download(url, path):
    requests.adapters.DEFAULT_RETRIES = 5
    response = requests.get(url, stream=True)
    status = response.status_code
    if status == 200:
        total_size = int(response.headers['content-length']) if 'content-length' in response.headers else -1

        with open(path, 'wb') as of:
            for chunk in response.iter_content(chunk_size=102400):
                if chunk:
                    of.write(chunk)
    
    return response
class Mission:
    def __init__(self, url, path, info=None, callback=None):
        self.url = url
        self.path = path
        self.info = info
        self.respond = None
        self.callback = callback

class DownloadThread(threading.Thread):
    def __init__(self, daemon):
        threading.Thread.__init__(self)
        self.daemon = daemon
        self.running = False
        self.downloading = False
        self.callingback = False
    def run(self):
        while self.running:
            ms = self.daemon.pop()
            if not ms:
                time.sleep(.1)
                continue
            self.downloading = True
            r = download(ms.url, ms.path)
            self.callingback = True
            # it must be like this
            self.downloading = False
            ms.respond = r
            if ms.callback:
                ms.callback(ms)
            self.callingback = False

class Daemon:
    def __init__(self, thread_number=1):
        self.pool = []
        self.mutex = threading.Lock()
        self.threads = [DownloadThread(self) for x in range(thread_number)]

    
    def add(self, url, filepath, info=None, callback=None):
        '''
            Add now download item into the waiting pool
        '''
        with self.mutex:
            self.pool.append(Mission(url, filepath, info=info, callback=callback))
        

    def pop(self):
        with self.mutex:
            if not self.pool:
                return None
            r = self.pool[0]
            del self.pool[0]
            return r

    def start(self):
        '''
            Start all the download threads
        '''
        for e in self.threads:
            e.running = True
            e.start()
    def stop(self):
        '''
            Make sure every download thread stops before next round.
        '''
        for e in self.threads:
            e.running = False


    def join(self):
        '''
            Wait until all the missions you allocated finish.
        '''
        while self.pool:
            time.sleep(.1)
        for e in self.threads:
            while e.callingback or e.downloading:
                time.sleep(.1)
    def clear(self):
        '''
            Clear download waiting pool, except downloading items.
        '''
        self.pool.clear()

    
def downloaded(mission):
    print(mission.url, 'downloaded')
if __name__ == "__main__":
    dm = Daemon()
    dm.start()
    dm.add('http://www.cnblogs.com/holbrook/archive/2012/03/04/2378947.html', 'test.html', callback=downloaded)
    dm.join()