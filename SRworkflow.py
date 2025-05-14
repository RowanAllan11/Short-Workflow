import subprocess
import os
print("[*] Script started")

# Define file paths 
short_reads = "/Users/rowanallan11/Desktop/SRworkflow/Sequences/duckTyphi.fastq.gz"
trimmed_reads = "/Users/rowanallan11/Desktop/SRworkflow/trimmedSR.fastq"
assembly_dir = "/Users/rowanallan11/Desktop/SRworkflow/Output"
trimmomatic_path = "/Users/rowanallan11/Desktop/SRworkflow/Trimmomatic/trimmomatic.jar"
adapter_path = "/Users/rowanallan11/Desktop/SRworkflow/Trimmomatic/adapters/TruSeq3-SE.fa"



# Run Trimmomatic
def run_trimmomatic():
    print("[*] Running Trimmomatic...")
    cmd = ["java", "-jar", trimmomatic_path, "SE", "-phred33",
        short_reads, trimmed_reads,
        f"ILLUMINACLIP:{adapter_path}:2:30:10",
        "LEADING:3",
        "TRAILING:3",
        "SLIDINGWINDOW:4:20",
        "MINLEN:36"]
    subprocess.run(cmd, check=True)
    print("[✓] Trimming complete.")

run_trimmomatic()


def run_unicycler():
    print("[*] Running Unicycler...")
    cmd = [
        "unicycler",
        "-s", trimmed_reads,
        "-o", assembly_dir
    ]
    subprocess.run(cmd, check=True)
    print("[✓] Assembly complete.")

run_unicycler()

