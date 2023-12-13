import sys
import numpy as np
import cv2 as cv
import time
import NDIlib as ndi
import subprocess
import psutil

class NDIReceiver:
    def __init__(self, user_name):
        self.user_name = user_name
        self.ndi_find = None
        self.ndi_recv = None

    def initialize(self):
        if not ndi.initialize():
            return False

        self.ndi_find = ndi.find_create_v2()

        if self.ndi_find is None:
            return False

        sources = []
        desired_source = None
        t = time.time()
        while time.time() - t < 1.0 * 60:
            #print('Looking for sources ...')
            ndi.find_wait_for_sources(self.ndi_find, 10000)
            sources = ndi.find_get_current_sources(self.ndi_find)
            for source in sources:
                if str(self.user_name).lower() in source.ndi_name.lower() and not 'Remote' in source.ndi_name:
                    #desired_source = source
                    break
            else:
                continue
            break
        
        # Sort the sources based on ndi_name
        sources = sorted(sources, key=lambda s: s.ndi_name.lower())

        # Find the first source that contains the desired user_name
        desired_source = None
        for source in sources:
            if str(self.user_name).lower() in source.ndi_name.lower() and not 'Remote' in source.ndi_name:
                desired_source = source
                break
        
        if desired_source is None:
            print(f"No source containing '{self.user_name}' found.")
            return False

        ndi_recv_create = ndi.RecvCreateV3()
        ndi_recv_create.color_format = ndi.RECV_COLOR_FORMAT_BGRX_BGRA

        self.ndi_recv = ndi.recv_create_v3(ndi_recv_create)

        if self.ndi_recv is None:
            return False

        ndi.recv_connect(self.ndi_recv, desired_source)

        return True

    def receive_frames(self):
        t, v, _, _ = ndi.recv_capture_v2(self.ndi_recv, 5000)
        while t != ndi.FRAME_TYPE_VIDEO:
            t, v, _, _ = ndi.recv_capture_v2(self.ndi_recv, 5000)
            #if t == ndi.FRAME_TYPE_VIDEO:


        #frame = np.empty_like(v.data)  # Create an empty array with the same shape
        #frame[:] = v.data  # Copy the data into the frame array
        frame = np.copy(v.data)
        ndi.recv_free_video_v2(self.ndi_recv, v)
        return frame

        '''
        if t == ndi.FRAME_TYPE_VIDEO:
            print('Video data received (%dx%d).' % (v.xres, v.yres))
            frame = np.copy(v.data)
            ndi.recv_free_video_v2(self.ndi_recv, v)
            return frame
        '''

    def release(self):
        if self.ndi_recv is not None:
            ndi.recv_destroy(self.ndi_recv)

        ndi.destroy()
        cv.destroyAllWindows()
def start_capture():
    process_name = "captures.exe"
    # Check if the process is already running
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            # Kill the process
            proc.kill()
            break

    # Run the process
    subprocess.Popen([process_name], shell=False)

if __name__ == "__main__":
    user_name = 'main-pc'
    ndi_receiver = NDIReceiver(user_name)
    if ndi_receiver.initialize():
        while True:
            frame = ndi_receiver.receive_frames()
            if frame is not None:
                cv.imshow("frame", frame)
            if cv.waitKey(10) & 0xff == 27:
                break
    ndi_receiver.release()