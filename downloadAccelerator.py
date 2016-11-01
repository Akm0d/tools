#!/usr/bin/env python
# Tyler Johnson
# Renato Scheuer
import sys
import os
import requests
import threading
import timeit

class partialDownload(threading.Thread):
    """Creates a thread that will download part of a file"""
    def __init__(self,url,b_start,b_end):
        self.url = url
        self.b_start = str(b_start)
        self.b_end = str(b_end)
        self.part = None
        self.done = False
        # Initialize the thread
        threading.Thread.__init__(self)
        # Se the thread as unlocked
        self._content_consumed = False

    # Method representing the thread's activity
    def run(self):
        # Each thread sends a GET request with a Range header that gives the range of bytes desired. 
        # Be sure the GET request also requests the identity encoding:
        # Accept-Encoding: identity so that it doesn't get a compressed response.
        self.part = requests.get(self.url, headers={"Accept-Encoding":"", "Range": "bytes="+self.b_start+"-"+self.b_end}).content
        self.done = True

class downloadAccelerator:
    """The Download Accelerator class"""
    def __init__(self,arguments):
        # Initialize all the variables that will be used with this class
        self.help_text = "downloadAccelerator.py [-n threads] url [-v]"
        self.debug = False
        self.url = None
        self.name = None
        # There will always be at least one thread
        self.threads = 1

        # Parse the command line arguments
        i = 1
        # A C++ like for loop
        while i < len(arguments):
            arg = arguments[i]
            # Verbose mode switch
            if "-d" in arg or "--debug" in arg:
                self.debug = True
            # If there is a -n, then the next argument is the number of threads
            elif "-n" in arg:
                if i + 1 < len(arguments):
                    self.threads = int(arguments[i+1])
                    i += 1
                else:
                    # If no number was passed with the -n argument then exit with the help text
                    print("ERROR! -n requires an argument")
                    print(self.help_text)
                    exit(1)
            elif not self.url:
                # Add The other argument as a url
                self.url = arguments[i]
            else:
                # If more arguments were given than expected
                print("ERROR! Too many arguments")
                print(self.help_text)
                exit(0)
            i += 1

        # If no url was provided then exit with the help text
        if not self.url:
            print("ERROR! a URL is required")
            print(self.help_text)
            exit(2)

        # The downloader saves the file in the current directory, using the same name as given in the URL. 
        # If the URL ends with "/", then the name "index.html" is implied.
        if self.url.endswith('/'):
            self.name = "index.html"
        else:
            self.name = self.url.split("/")[-1:][0]

        # print out the results of the command line options
        if self.debug:
            print("Verbose: ON")
            print("Threads: " + str(self.threads))
            print("URL: " + str(self.url))
            print("Name: " + str(self.name))

    # Performs all the download operations and returns the filepath of the fully downloaded file
    # This is the function that other python program should call
    def download(self):
        # Function variables
        # On starting, the downloader first sends a HEAD request to the web server specified in the URL to determine the size of the object. 
        request  = requests.head(self.url)
        # If the object has a valid Content-Length field, 
        if not "content-length" in request.headers:
            print("Error! Invalid content_length")
            exit(4)
        # then it downloads the object in parallel, using the specified number of threads. 
        num_bytes = int(request.headers.get('content-length'))
        cwd = os.getcwd()
        path = cwd + "/" + self.name
        t_start = timeit.default_timer()
        threads = []

        for t in range(0,self.threads):
            # The starting and ending bits for this thread
            b_start = 0
            # Except for the first thread, start one byte over
            if t > 0: b_start = (t*(num_bytes/self.threads))+t
            b_end = b_start + (num_bytes / self.threads)
            # The last thread will download the remaining bits
            if(t == self.threads - 1): b_end = num_bytes
            thread = partialDownload(self.url,b_start,b_end)
            threads.append(thread)

        # Start the run method of each thread
        for thread in threads: thread.start()

        # Wait for threads to finish
        all_done = False
        while not all_done:
            done = True
            for thread in threads:
                done &= thread.done 
            all_done |= done

        # Save the file
        with open(path,'wb') as output:
            i = 0
            for thread in threads: 
                # Wait until the output is printed before moving on to the next thread
                thread.join()
                if self.debug: output.write("|Thread " + str(i) + "|")
                output.write(thread.part)
                i+= 1
            output.close

        # Print the output in the correct format
        t_stop = timeit.default_timer()
        time = t_stop - t_start
        if self.debug: print("Downloaded to " + path)
        if self.debug: print("URL"+" "*(len(self.url)-3)+"       \tThreads"+" "*(len(str(self.threads))-7)+"    \tbytes"+" "*(len(str(num_bytes))-5)+"    \tSeconds")
        print(self.url + "     \t" + str(self.threads) + "    \t" + str(num_bytes) + "    \t" + str(time))
        return path

# Main function
if __name__ == '__main__':
    accelerator = downloadAccelerator(sys.argv)
    output_file = accelerator.download()
