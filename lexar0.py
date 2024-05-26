import ctypes

# Define constants
SECTOR_SIZE = 512  # Typical sector size for a USB drive
DEVICE_PATH = "\\\\.\\PHYSICALDRIVE2"  # Replace with your drive path (use with caution!)

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
    # Open the disk device with write access (use with caution!)
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

    # Write data to the specified sector (use with caution!)
    if not ctypes.windll.kernel32.WriteFile(handle, data, bytes_to_write, None, None):
        raise ctypes.WinError(ctypes.get_last_error())


def create_partition_table(drive_size, partition_size, partition_type):
    # This function outlines the logic for creating a partition table (replace with actual implementation)
    # 1. Calculate partition parameters (sectors, offset) based on drive size and partition size
    total_sectors = drive_size // SECTOR_SIZE
    partition_sectors = partition_size // SECTOR_SIZE
    partition_offset = SECTOR_SIZE  # Assuming first sector for primary partition

    # 2. Initialize an empty MBR data structure
    mbr_data = bytearray(SECTOR_SIZE)

    # 3. Create a PartitionEntry object for the desired partition
    partition_entry = PartitionEntry(
        boot_indicator=0x00,  # Not bootable
        starting_chs=(0, 0, 1),  # CHS values (often ignored in modern systems)
        partition_type=partition_type,  # Set partition type (e.g., 0x0B for FAT32)
        ending_chs=(0, 0, 0),  # CHS values (often ignored in modern systems)
        logical_sector_offset=partition_offset,
        sectors_in_partition=partition_sectors,
    )

    # 4. Copy PartitionEntry data into the MBR data structure at appropriate offsets
    # (Refer to MBR documentation for specific byte locations)

    return mbr_data


def main():
    # Open the disk device (use with caution!)
    handle = get_disk_handle(DEVICE_PATH)

    try:
        # Get drive size information (**WARNING: Not implemented here!**)
        # You'll need to implement a way to get the drive size in sectors.

        # Prompt user for partition details (size, type)
        partition_size = int(input("Enter desired partition size (in MB): ")) * 1024 * 1024
        partition_type = int(input("Enter partition type (
