import os
import sys
import time
import queue
import subprocess
import collections
from threading import Thread, currentThread


currentDir = os.path.dirname(__file__)

SHORTEXT = (".7z", ".xz", ".gz", ".rar", ".zip",  ".tar", ".bz2")
LONGEXT =  (".tar.gz", ".tar.bz2", ".tar.xz", ".tar.7z", ".zip.asc")


class ThreadPoll(object):
    def __init__(self, size=5):
        self.size = 5
        self.taskqueue = queue.Queue(size)
        # store thread function returned value
        self.resqueue = queue.Queue(2*size)
        # initial threads
        for _ in range(size):
            t = MyThread(self.taskqueue, self.resqueue)
            t.start()

    # submit task to task queue
    def submit(self, func, args):
        self.taskqueue.put((func, args))

    # get result from result queue
    def getres(self):
        return self.resqueue.get()


class MyThread(Thread):
    def __init__(self, taskqueue, resqueue):
        Thread.__init__(self)
        self.taskqueue = taskqueue
        self.resqueue = resqueue
        # enable daemon thread
        self.daemon = True

    # overide run method
    def run(self):
        while True:
            target, args = self.taskqueue.get()
            res = target(*args)
            self.taskqueue.task_done()
            self.resqueue.put(res)
    

class ExtractAll():
    def __init__(self, srcPath, dstPath):
        self.dst = dstPath
        self.file = srcPath
        self.longext = False

    def _check(self):
        """
        检查
        self.file 是文件
        self.dst 是文件夹
        """
        if os.path.exists(self.file):
            if os.path.isfile(self.file):
                if os.path.exists(self.dst):
                    if os.path.isdir(self.dst):
                        return True
                    else:
                        sys.stderr.write("path:'%s' isn't a folder.\n" % (self.dst))
                else:
                    sys.stderr.write("path:'%s' dosen't exist.\n" % (self.dst))
            else:
                sys.stderr.write("file:'%s' isn't a file.\n" % (self.file))
        else:
            sys.stderr.write("file:'%s' isn't a exist.\n" % (self.file))
        return False

    @staticmethod
    def is_extract(file):
        """
        如果文件是指定扩展名的压缩文件，返回解压的文件夹
        否则返回False
        """
        iszip = False
        if not os.path.exists(file):
            print("FileNotExist: %s" % (file))
            return False
        else:
            _, fileName = os.path.split(file)
            dstFolder, ext = os.path.splitext(fileName)
            if ext in SHORTEXT or ext in LONGEXT:
                for e in LONGEXT:
                    if e in fileName:
                        # 长扩展压缩文件的目标文件夹名
                        dstFolder, _ = os.path.splitext(dstFolder)
                        iszip = True
                        break
                for e in SHORTEXT:
                    if e in fileName:
                        iszip = True
                        break
            result = subprocess.run(["7z.exe", "t", file], capture_output=True)
            if result.stderr == b"" and iszip:
                return dstFolder
            return False

    def extract(self, src, dst):
        """
        解压压缩包并删除原来的压缩包
        """ 
        folder = self.is_extract(src)
        _, oldFolder = os.path.split(dst)    
        if folder:
            if folder != oldFolder:
                dst = os.path.join(dst, folder)
            res = subprocess.run(["7z.exe", "x", src, "-o%s" % (dst)])#, capture_output=True)
            try:
                if os.path.abspath(src) != os.path.abspath(self.file):
                    os.remove(src)
            except PermissionError as e:
                print(e+"\ncan't delete %s" % (src))
            return dst       

    def extractall(self):
        if not self._check():
            return False

        dst = self.extract(self.file, self.dst)
        queue = collections.deque()
        queue.append(dst)
        pool = ThreadPoll()

        # 广度优先遍历目录
        while len(queue) != 0:
            current_path = queue.popleft()
            fileslist = os.listdir(current_path)
            for file in fileslist:
                fileabspath = os.path.join(current_path, file)
                if os.path.isdir(fileabspath):
                    queue.append(fileabspath)
                else:
                    pool.submit(self.extract, (fileabspath, current_path, ))
                    dst = pool.getres()
                    if dst and os.path.isdir(dst):
                        queue.append(dst)


def shell():
    helpmsg = """usage: extractall <src> <dst>
                        <src>: zip file path
                        <dst>: destination folder

                        -h  --help: for help
                """
    if len(sys.argv) != 3 or sys.arg[1] == "-h" or sys.argv[1] == "--help":
        print(helpmsg)
        os._exit(0)   


def main(): 
    shell()
    print("running...")
    inst =  ExtractAll(sys.argv[1], sys.argv[2])
    inst.extractall()
    print("Finished!")


def f(n):
    return n**2

def t():
    pool = ThreadPoll()
    for i in range(100):
        pool.submit(f, (i, ))
        print(pool.getres())


if __name__ == "__main__":
    main()

