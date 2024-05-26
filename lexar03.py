import fdisk

# Define constants (replace with actual values)
DEVICE_PATH = "/dev/sdb"  # Replace with your USB drive path
PARTITION_SIZE_MB = 1024  # Desired partition size in Megabytes
PARTITION_TYPE = "W95 FAT32"  # Desired partition type

def create_partition(device_path, size_mb, partition_type):
  """
  Creates a partition on the specified device using fdisk.

  Args:
      device_path: Path to the device (e.g., /dev/sdb)
      size_mb: Size of the partition in Megabytes
      partition_type: Desired partition type (e.g., W95 FAT32)
  """
  # Open the disk device with fdisk
  p = fdisk.open(device_path)

  try:
    # Create a new partition
    new_partition = p.new_partition(extended=False)

    # Set partition size
    new_partition.set_size_mbytes(size_mb)

    # Set partition type
    new_partition.set_type(partition_type)

    # Write changes to disk
    p.write()

    print(f"Partition created successfully on {device_path}")

  finally:
    # Close the fdisk connection
    p.close()


if __name__ == "__main__":
  # Get user confirmation
  print("**WARNING: This program can modify partitions on your drive!**")
  print(f"Make sure to use a test drive ({DEVICE_PATH}) and understand the risks before proceeding.")
  user_confirmation = input("Do you want to continue? (y/n): ")
  if user_confirmation.lower() == "y":
    create_partition(DEVICE_PATH, PARTITION_SIZE_MB, PARTITION_TYPE)
  else:
    print("Exiting program.")
