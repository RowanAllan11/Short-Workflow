# 🧬 Salmonella Assembly Workflow Notes

## 📅 Date: 2025-05-14

1. Designed short read workflow for initial assembly using tools like trimmomatic and unicycler. (BASE ENV)
2. Tested AMRFinder on hybrid dataset (required prokka installation)
3. Downsampling the short read data set using seqtk to test it on pipeline
4. Investigating the presence of replicons present on contigs/plasmids visible in the bandage assembly using plamidfinder. Perhaps hybrid assemblies have an advantage over short read assemblies because of their better spatial resolvement?? Need to investigate. Better resolved assemblies can detect whether AMR genes are present on the chromosome or plasmids.
