import subprocess
import os
from pathlib import Path
print("[*] Script started")

# Define file paths 
forward_read = "15.fastq.gz"
reverse_read = "25.fastq.gz"

input_reads = Path("/Users/rowanallan11/Desktop/SRworkflow/Sequences/D23580strain")
trim_dir = Path("/Users/rowanallan11/Desktop/SRworkflow/TrimmedSeq")
output_dir = Path("/Users/rowanallan11/Desktop/SRworkflow/Output")
trimmomatic_path = "/Users/rowanallan11/Desktop/SRworkflow/Trimmomatic/trimmomatic.jar"
adapter_path = "/Users/rowanallan11/Desktop/SRworkflow/Trimmomatic/adapters/TruSeq3-SE.fa"

f_read = input_reads / forward_read
r_read = input_reads / reverse_read
sample_name = "D2ref"

paired_f = trim_dir / f"{sample_name}_paired_f.fastq.gz"
unpaired_f = trim_dir / f"{sample_name}_unpaired_f.fastq.gz"
paired_r = trim_dir / f"{sample_name}_paired_r.fastq.gz"
unpaired_r = trim_dir / f"{sample_name}_unpaired_r.fastq.gz"
sample_output_dir = output_dir / sample_name

# Check inputs
if not f_read.exists() or not r_read.exists():
    raise FileNotFoundError("One or both input FASTQ files are missing.")

# Run Trimmomatic
def run_trimmomatic():
    print("[*] Running Trimmomatic...")
    cmd = ["java", "-jar", trimmomatic_path, "PE", "-phred33",
        str(f_read), str(r_read),
        str(paired_f), str(unpaired_f),
        str(paired_r), str(unpaired_r),
        f"ILLUMINACLIP:{adapter_path}:2:30:10",
        "LEADING:3",
        "TRAILING:3",
        "SLIDINGWINDOW:4:20",
        "MINLEN:36"]
    subprocess.run(cmd, check=True)
    print("[✓] Trimming complete.")



def run_unicycler():
    print("[*] Running Unicycler...")
    cmd = [
        "unicycler",
        "-1", str(paired_f),
        "-2", str(paired_r),
        "-o", str(sample_output_dir)
    ]
    subprocess.run(cmd, check=True)
    print("[✓] Assembly complete.")


def run_assembly_stats():
    print("[*] Running assembly-stats...")
    assembly_fasta = sample_output_dir / "assembly.fasta"
    stats_output_file = sample_output_dir / f"{sample_name}_assembly_stats.txt"

    result = subprocess.run(
        ["assembly-stats", str(assembly_fasta)],
        check =True,
        capture_output=True,
        text=True
    )

    with open(stats_output_file, "w") as f:
        f.write(result.stdout)

def run_abricate():
    print("[*] Running ABRicate...")
    assembly_fasta = sample_output_dir / "assembly.fasta"
    abricate_output_file = sample_output_dir / f"{sample_name}_abricate_output.txt"

    cmd = [
        "abricate",
        str(assembly_fasta)
    ]

    # Run abricate and capture output to a file
    with open(abricate_output_file, "w") as outfile:
        subprocess.run(cmd, check=True, stdout=outfile)

    print(f"[✓] ABRicate results saved to {abricate_output_file}")

def run_abricate_plasmidfinder():
    print("[*] Running ABRicate with PlasmidFinder...")
    assembly_fasta = sample_output_dir / "assembly.fasta"
    abricate_output_file = sample_output_dir / f"{sample_name}_abricate_plasmidfinder.tsv"

    result = subprocess.run(
        ["abricate", "--db", "plasmidfinder", str(assembly_fasta)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        print(f"[!] ABRicate error: {result.stderr}")
    else:
        with open(abricate_output_file, "w") as f:
            f.write(result.stdout)
        print(f"[✓] ABRicate results saved to {abricate_output_file}")

try:
    run_trimmomatic()
    run_unicycler()
    run_assembly_stats()
    run_abricate()
    run_abricate_plasmidfinder()
except subprocess.CalledProcessError as e:
    print(f"[!] Error during processing: {e}")

