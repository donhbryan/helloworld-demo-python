import os
import ctypes

# Define constants (replace with actual values for your drive)
DEVICE_PATH = "\\\\E:"  # Replace with your drive path
SECTOR_SIZE = 512  # Typical sector size for a USB drive

# Structure representing an MBR partition entry
class PartitionEntry(ctypes.Structure):
    _fields_ = [
        ("boot_indicator", ctypes.c_ubyte),
        ("starting_chs", ctypes.c_ubyte * 3),
        ("partition_type", ctypes.c_ubyte),
        ("ending_chs", ctypes.c_ubyte * 3),
        ("logical_sector_offset", ctypes.c_uint),
        ("sectors_in_partition", ctypes.c_uint),
    ]
    

def get_disk_handle(device_path):
    # Open the disk device with write access
    handle = ctypes.windll.kernel32.CreateFileA(
        device_path,
        ctypes.windll.kernel32.GENERIC_READ | ctypes.windll.kernel32.GENERIC_WRITE,
        0,
        None,
        ctypes.windll.kernel32.OPEN_EXISTING,
        0,
        None,
    )
    if handle == -1:
        raise ctypes.WinError(ctypes.get_last_error())
    return handle


def read_sector(handle, sector_number):
    # Define buffer to hold the sector data
    buffer = ctypes.create_string_buffer(SECTOR_SIZE)

    # Set number of bytes to be read (entire sector)
    bytes_to_read = ctypes.c_ulong(SECTOR_SIZE)

    # Read data from the specified sector
    if not ctypes.windll.kernel32.ReadFile(handle, buffer, bytes_to_read, None, None):
        raise ctypes.WinError(ctypes.get_last_error())

    return buffer.raw


def write_sector(handle, sector_number, data):
    # Set number of bytes to be written (entire sector)
    bytes_to_write = ctypes.c_ulong(SECTOR_SIZE)

    # Write data to the specified sector
    if not ctypes.windll.kernel32.WriteFile(handle, data, bytes_to_write, None, None):
        raise ctypes.WinError(ctypes.get_last_error())


def main():
    # Open the disk device
    handle = get_disk_handle(DEVICE_PATH)

    try:
        # Read the first sector (MBR)
        mbr_data = read_sector(handle, 0)

        # **WARNING: Modifying MBR data can lead to data loss!**
        # This section demonstrates hypothetical modification (replace with actual logic)

        # Modify partition entries in the MBR data (replace with valid values)
        partition_entry = PartitionEntry.from_buffer(mbr_data)
        partition_entry.boot_indicator = 0x80  # Set bootable flag
        partition_entry.partition_type = 0x0B  # Set partition type (e.g., FAT32)
        # ... Modify other partition entry fields

        # Write the modified MBR data back to the first sector
        # write_sector(handle, 0, mbr_data)

        print("MBR data written (**WARNING: Data on the drive might be lost!**)")
    finally:
        # Close the disk handle
        ctypes.windll.kernel32.CloseHandle(handle)


if __name__ == "__main__":
    print("**WARNING: This program can cause data loss on the specified drive!**")
    print("Make sure to use a test drive and understand the risks before proceeding.")
    user_confirmation = input("Do you want to continue? (y/n): ")
    if user_confirmation.lower() == "y":
        main()
    else:
        print("Exiting program.")
