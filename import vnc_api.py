import vnc_api

# Set the IP range to scan
ip_range = '192.168.1.'
start_ip = 1
end_ip = 100

# Loop through the IP range and check for open VNC servers
for i in range(start_ip, end_ip+1):
    ip = ip_range + str(i)
    try:
        vnc = vnc_api.connect(ip)
        print('VNC server found at', ip)
        
        # Open a window to view the VNC screen
        vnc_api.show(vnc)
    except:
        pass
