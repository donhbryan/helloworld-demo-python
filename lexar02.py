import ctypes

# Define constants for partition table size and sector size
SECTOR_SIZE = 512
MBR_SIZE = SECTOR_SIZE

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


def create_partition_table(partition_type, partition_start_sector, partition_sectors):
  """
  Creates a partition table structure in memory.

  Args:
      partition_type: Desired partition type (e.g., 0x0B for FAT32)
      partition_start_sector: Starting sector of the partition
      partition_sectors: Number of sectors in the partition

  Returns:
      A byte array representing the MBR partition table structure.
  """
  # Allocate memory for the MBR
  mbr_data = ctypes.create_string_buffer(MBR_SIZE)

  # Create a partition entry object
  partition_entry = PartitionEntry.from_buffer(mbr_data)

  # Set partition entry fields (replace with your logic)
  partition_entry.boot_indicator = 0x00  # Not bootable
  partition_entry.partition_type = partition_type
  # Set starting CHS (replace with appropriate values)
  partition_entry.starting_chs = (0, 1, 1)
  # Set ending CHS (replace with appropriate values)
  partition_entry.ending_chs = (0, 1, 1)
  partition_entry.logical_sector_offset = partition_start_sector
  partition_entry.sectors_in_partition = partition_sectors

  # Return the MBR data as a byte array
  return mbr_data.raw


# Example usage
partition_type = 0x0B  # FAT32
partition_start_sector = 1
partition_sectors = 10000

mbr_data = create_partition_table(partition_type, partition_start_sector, partition_sectors)

print("Created partition table in memory (not written to disk!)")
print(mbr_data)