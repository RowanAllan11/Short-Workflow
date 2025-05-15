import subprocess
import os
from pathlib import Path
print("[*] Script started")

# Define file paths 
fastq_filename = "subsampled.1.fastq"
input_reads = Path("/Users/rowanallan11/Desktop/SRworkflow/Sequences")
trim_dir = Path("/Users/rowanallan11/Desktop/SRworkflow/TrimmedSeq")
output_dir = Path("/Users/rowanallan11/Desktop/SRworkflow/Output")
trimmomatic_path = "/Users/rowanallan11/Desktop/SRworkflow/Trimmomatic/trimmomatic.jar"
adapter_path = "/Users/rowanallan11/Desktop/SRworkflow/Trimmomatic/adapters/TruSeq3-SE.fa"

fastq_file = input_reads / fastq_filename
sample_name = fastq_file.stem
trimmed_file = trim_dir / f"{sample_name}_trimmed.fastq"
sample_output_dir = output_dir / sample_name

# Check Input Exists
if not fastq_file.exists():
    raise FileNotFoundError(f"{fastq_file} does not exist.")

# Run Trimmomatic
def run_trimmomatic():
    print("[*] Running Trimmomatic...")
    cmd = ["java", "-jar", trimmomatic_path, "SE", "-phred33",
        str(fastq_file), str(trimmed_file),
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
        "-s", str(trimmed_file),
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

