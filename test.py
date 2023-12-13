from ctypes import *
 
# Define constants and types from C code
MOUSE_PRESS = 1
MOUSE_RELEASE = 2
MOUSE_MOVE = 3
MOUSE_CLICK = 4
 
class MOUSE_IO(Structure):
    _fields_ = [
        ('button', c_char),
        ('x', c_char),
        ('y', c_char),
        ('wheel', c_char),
        ('unk1', c_char),
    ]
 
IO_STATUS_BLOCK = c_ulonglong * 2
 
# Load ntdll library and define function prototypes
ntdll = WinDLL('ntdll')
NtDeviceIoControlFile = ntdll.NtDeviceIoControlFile
NtDeviceIoControlFile.argtypes = [HANDLE, HANDLE, LPVOID, LPVOID, LPVOID, DWORD, LPVOID, DWORD, LPVOID, DWORD]
NtDeviceIoControlFile.restype = NTSTATUS
 
# Set up global variables
g_input = HANDLE()
g_io = IO_STATUS_BLOCK()
g_found_mouse = False
 
# Define Python wrapper function
def callmouse(button, x, y, wheel, unk1):
    global g_input, g_io
    buffer = MOUSE_IO(button, x, y, wheel, unk1)
    return NtDeviceIoControlFile(g_input, None, None, None, byref(g_io), 0x2a2010, byref(buffer), sizeof(MOUSE_IO), None, 0) == 0
 
# Example usage
if __name__ == '__main__':
    g_input = CreateFile("\\\\.\\Mouse", GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, None)
    if g_input != INVALID_HANDLE_VALUE:
        g_found_mouse = True
 
    if g_found_mouse:
        # Move mouse to x=100, y=100
        callmouse(MOUSE_MOVE, 100, 100, 0, 0)
 
    CloseHandle(g_input)