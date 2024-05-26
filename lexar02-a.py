import struct

# Define constants for partition table offsets and sizes
SECTOR_SIZE = 512
MBR_TABLE_OFFSET = 446

# Structure representing an MBR partition entry
class PartitionEntry(object):
    """
    Class representing an MBR partition entry.
    """
    def __init__(self):
        self.boot_indicator = 0  # 0=inactive, 0x80=bootable
        self.starting_chs = (0, 0, 0)  # CHS (Cylinder, Head, Sector)
        self.partition_type = 0  # Partition type code
        self.ending_chs = (0, 0, 0)  # CHS (Cylinder, Head, Sector)
        self.logical_sector_offset = 0  # Relative sector offset of partition
        self.sectors_in_partition = 0  # Total sectors in the partition

# Function to create a raw MBR table with sample partition entries
def create_sample_mbr_table():
  """
  Creates a raw MBR table with sample partition entries (replace with your logic)
  """
  # Create a partition entry objects
  partition1 = PartitionEntry()
  partition1.boot_indicator = 0x80  # Set bootable flag
  partition1.partition_type = 0x0B  # Set partition type (e.g., FAT32)
  partition1.logical_sector_offset = 1000  # Set starting sector for partition 1
  partition1.sectors_in_partition = 10000  # Set partition size in sectors

  partition2 = PartitionEntry()  # Add more entries as needed...

  # Pack partition entries into a binary string using struct
  partition_data = b"".join([struct.pack("<BBBxHHLL", p.boot_indicator, *p.starting_chs, 
                             p.partition_type, *p.ending_chs, p.logical_sector_offset, 
                             p.sectors_in_partition) for p in [partition1, partition2]])

  # Create a full MBR sector with padding
  mbr_sector = partition_data + b"\0" * (SECTOR_SIZE - len(partition_data))
  return mbr_sector

if __name__ == "__main__":
  # Create a sample MBR table in memory
  mbr_table = create_sample_mbr_table()
  print("Created a sample MBR table in memory (not written to disk)")
