Yes — the `exploratory-data-analysis` skill is specifically designed to describe a comprehensive data analysis workflow. Here are its major steps:

---

### `exploratory-data-analysis` Workflow (5 Steps)

**Step 1: File Type Detection**
Extracts the file extension, looks it up in the appropriate reference file, and identifies the file category and format description. [1](#1-0) 

**Step 2: Load Format-Specific Information**
Reads the corresponding reference file to understand typical data content, use cases, Python libraries, and the appropriate EDA approach for that format. [2](#1-1) 

**Step 3: Perform Data Analysis**
Runs either the automated `scripts/eda_analyzer.py` script or custom in-conversation analysis (e.g., pandas for tabular data, BioPython for sequences, tifffile for images). [3](#1-2) 

**Step 4: Generate Comprehensive Report**
Produces a markdown report with six required sections: Title/Metadata, Basic Information, File Type Details, Data Analysis, Key Findings, and Recommendations. [4](#1-3) 

**Step 5: Save Report**
Saves the markdown report using the pattern `{original_filename}_eda_report.md`. [5](#1-4) 

---

The skill covers **200+ scientific file formats** across 6 categories (chemistry, bioinformatics, microscopy, spectroscopy, proteomics/metabolomics, and general scientific formats). [6](#1-5) 

---

There is also a complementary `statistical-analysis` skill that picks up where EDA leaves off, with its own workflow covering test selection, assumption checking, running statistical tests, effect size calculation, and APA-formatted reporting. [7](#1-6)

### Citations

**File:** scientific-skills/exploratory-data-analysis/SKILL.md (L34-78)
```markdown
## Supported File Categories

The skill has comprehensive coverage of scientific file formats organized into six major categories:

### 1. Chemistry and Molecular Formats (60+ extensions)
Structure files, computational chemistry outputs, molecular dynamics trajectories, and chemical databases.

**File types include:** `.pdb`, `.cif`, `.mol`, `.mol2`, `.sdf`, `.xyz`, `.smi`, `.gro`, `.log`, `.fchk`, `.cube`, `.dcd`, `.xtc`, `.trr`, `.prmtop`, `.psf`, and more.

**Reference file:** `references/chemistry_molecular_formats.md`

### 2. Bioinformatics and Genomics Formats (50+ extensions)
Sequence data, alignments, annotations, variants, and expression data.

**File types include:** `.fasta`, `.fastq`, `.sam`, `.bam`, `.vcf`, `.bed`, `.gff`, `.gtf`, `.bigwig`, `.h5ad`, `.loom`, `.counts`, `.mtx`, and more.

**Reference file:** `references/bioinformatics_genomics_formats.md`

### 3. Microscopy and Imaging Formats (45+ extensions)
Microscopy images, medical imaging, whole slide imaging, and electron microscopy.

**File types include:** `.tif`, `.nd2`, `.lif`, `.czi`, `.ims`, `.dcm`, `.nii`, `.mrc`, `.dm3`, `.vsi`, `.svs`, `.ome.tiff`, and more.

**Reference file:** `references/microscopy_imaging_formats.md`

### 4. Spectroscopy and Analytical Chemistry Formats (35+ extensions)
NMR, mass spectrometry, IR/Raman, UV-Vis, X-ray, chromatography, and other analytical techniques.

**File types include:** `.fid`, `.mzML`, `.mzXML`, `.raw`, `.mgf`, `.spc`, `.jdx`, `.xy`, `.cif` (crystallography), `.wdf`, and more.

**Reference file:** `references/spectroscopy_analytical_formats.md`

### 5. Proteomics and Metabolomics Formats (30+ extensions)
Mass spec proteomics, metabolomics, lipidomics, and multi-omics data.

**File types include:** `.mzML`, `.pepXML`, `.protXML`, `.mzid`, `.mzTab`, `.sky`, `.mgf`, `.msp`, `.h5ad`, and more.

**Reference file:** `references/proteomics_metabolomics_formats.md`

### 6. General Scientific Data Formats (30+ extensions)
Arrays, tables, hierarchical data, compressed archives, and common scientific formats.

**File types include:** `.npy`, `.npz`, `.csv`, `.xlsx`, `.json`, `.hdf5`, `.zarr`, `.parquet`, `.mat`, `.fits`, `.nc`, `.xml`, and more.

**Reference file:** `references/general_scientific_formats.md`
```

**File:** scientific-skills/exploratory-data-analysis/SKILL.md (L82-98)
```markdown
### Step 1: File Type Detection

When a user provides a file path, first identify the file type:

1. Extract the file extension
2. Look up the extension in the appropriate reference file
3. Identify the file category and format description
4. Load format-specific information

**Example:**
```
User: "Analyze data.fastq"
→ Extension: .fastq
→ Category: bioinformatics_genomics
→ Format: FASTQ Format (sequence data with quality scores)
→ Reference: references/bioinformatics_genomics_formats.md
```
```

**File:** scientific-skills/exploratory-data-analysis/SKILL.md (L100-108)
```markdown
### Step 2: Load Format-Specific Information

Based on the file type, read the corresponding reference file to understand:
- **Typical Data:** What kind of data this format contains
- **Use Cases:** Common applications for this format
- **Python Libraries:** How to read the file in Python
- **EDA Approach:** What analyses are appropriate for this data type

Search the reference file for the specific extension (e.g., search for "### .fastq" in `bioinformatics_genomics_formats.md`).
```

**File:** scientific-skills/exploratory-data-analysis/SKILL.md (L110-153)
```markdown
### Step 3: Perform Data Analysis

Use the `scripts/eda_analyzer.py` script OR implement custom analysis:

**Option A: Use the analyzer script**
```python
# The script automatically:
# 1. Detects file type
# 2. Loads reference information
# 3. Performs format-specific analysis
# 4. Generates markdown report

python scripts/eda_analyzer.py <filepath> [output.md]
```

**Option B: Custom analysis in the conversation**
Based on the format information from the reference file, perform appropriate analysis:

For tabular data (CSV, TSV, Excel):
- Load with pandas
- Check dimensions, data types
- Analyze missing values
- Calculate summary statistics
- Identify outliers
- Check for duplicates

For sequence data (FASTA, FASTQ):
- Count sequences
- Analyze length distributions
- Calculate GC content
- Assess quality scores (FASTQ)

For images (TIFF, ND2, CZI):
- Check dimensions (X, Y, Z, C, T)
- Analyze bit depth and value range
- Extract metadata (channels, timestamps, spatial calibration)
- Calculate intensity statistics

For arrays (NPY, HDF5):
- Check shape and dimensions
- Analyze data type
- Calculate statistical summaries
- Check for missing/invalid values

```

**File:** scientific-skills/exploratory-data-analysis/SKILL.md (L154-191)
```markdown
### Step 4: Generate Comprehensive Report

Create a markdown report with the following sections:

#### Required Sections:
1. **Title and Metadata**
   - Filename and timestamp
   - File size and location

2. **Basic Information**
   - File properties
   - Format identification

3. **File Type Details**
   - Format description from reference
   - Typical data content
   - Common use cases
   - Python libraries for reading

4. **Data Analysis**
   - Structure and dimensions
   - Statistical summaries
   - Quality assessment
   - Data characteristics

5. **Key Findings**
   - Notable patterns
   - Potential issues
   - Quality metrics

6. **Recommendations**
   - Preprocessing steps
   - Appropriate analyses
   - Tools and methods
   - Visualization approaches

#### Template Location
Use `assets/report_template.md` as a guide for report structure.
```

**File:** scientific-skills/exploratory-data-analysis/SKILL.md (L193-197)
```markdown
### Step 5: Save Report

Save the markdown report with a descriptive filename:
- Pattern: `{original_filename}_eda_report.md`
- Example: `experiment_data.fastq` → `experiment_data_eda_report.md`
```

**File:** scientific-skills/statistical-analysis/SKILL.md (L58-79)
```markdown
## Workflow Decision Tree

Use this decision tree to determine your analysis path:

```
START
│
├─ Need to SELECT a statistical test?
│  └─ YES → See "Test Selection Guide"
│  └─ NO → Continue
│
├─ Ready to check ASSUMPTIONS?
│  └─ YES → See "Assumption Checking"
│  └─ NO → Continue
│
├─ Ready to run ANALYSIS?
│  └─ YES → See "Running Statistical Tests"
│  └─ NO → Continue
│
└─ Need to REPORT results?
   └─ YES → See "Reporting Results"
```
```
