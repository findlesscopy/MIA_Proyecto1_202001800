import struct

class Inodos:
    def __init__(self):
        self.i_uid = -1
        self.i_gid = -1
        self.i_size = -1
        self.i_atime = 0
        self.i_ctime = 0
        self.i_mtime = 0
        self.i_block = [-1] * 15
        self.i_type = 0
        self.i_perm = -1

    def __bytes__(self):
        return (struct.pack("<i", self.i_uid) +
                struct.pack("<i", self.i_gid) +
                struct.pack("<i", self.i_size) +
                struct.pack("<d", self.i_atime) +
                struct.pack("<d", self.i_ctime) +
                struct.pack("<d", self.i_mtime) +
                struct.pack("<15i", *self.i_block) +
                struct.pack("<B", self.i_type) +  # Use "<B" format for a single byte
                struct.pack("<i", self.i_perm))
    
    def __setstate__(self, data):
        self.i_uid = struct.unpack("<i", data[:4])[0]
        self.i_gid = struct.unpack("<i", data[4:8])[0]
        self.i_size = struct.unpack("<i", data[8:12])[0]
        self.i_atime = struct.unpack("<d", data[12:20])[0]
        self.i_ctime = struct.unpack("<d", data[20:28])[0]
        self.i_mtime = struct.unpack("<d", data[28:36])[0]
        self.i_block = list(struct.unpack("<15i", data[36:96]))
        self.i_type = struct.unpack("<B", data[96:97])[0]
        self.i_perm = struct.unpack("<i", data[97:101])[0]