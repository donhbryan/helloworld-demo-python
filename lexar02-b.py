from diskutils import Partition

# Define constants for the partition
partition_size_mb = 1024
partition_type = "FAT32"  # Or any valid MBR partition type code

# Create an empty MBR object
mbr = Partition(partition_type="mbr")

# Add a new partition to the MBR
partition = mbr.add_partition(start=2048, size=partition_size_mb * 2048, type=partition_type)

# Access and modify partition properties (optional)
partition.bootable = True  # Set the partition as bootable

# Get the raw bytes representing the MBR structure
mbr_bytes = mbr.get_bytes()

print("Created a sample MBR partition table in memory:")
# Print some information about the partition (optional)
print(f"Partition size: {partition_size_mb} MB")
print(f"Partition type: {partition_type}")
