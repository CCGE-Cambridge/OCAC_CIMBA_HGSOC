Usage of score_test_prog.exe
./score_test_prog.exe [B/O] phenotype.data kinship.matrix impute2.data
[B/O] determines whether the breast cancer [B] or ovarian cancer [O] phenotype are to be analysed. Default is B

Description of data input:
1) Phenotype file: space delimited file with six columns, with header
ID Stratum Family Phenotype_bc Phenotype_oc Consent
ID = individual ID
Stratum = analytical strata e.g. country and Ashkenazi Jewish ancestry
Family = family ID
Phenotype_bc = score test phenotype for breast cancer: breast cancer censoring status (0=unaffected, 1=affected) minus cumulative breast cancer incidence up to censoring age for breast cancer
Phenotype_oc = score test phenotype for ovarian cancer: ovarian cancer censoring status (0=unaffected, 1=affected) minus cumulative ovarian cancer incidence up to censoring age for ovarian cancer
Consent = inclusion/exclusion for analysis. 0=include, 1=exclude

2) Kinship matrix: space delimited kinship matrix
For N individuals, the matrix has N rows and N+1 columns
First column is the individual ID, the remaining columns make up the NxN kinship matrix
The main diagonal values are all 1 (within person kinship = 1)
Off diagonal entries are the kinship value between person individuals (i,j)
Entries (i,j) are equal to (j,i)

3) Genetic data file(s)
Data in IMPUTE2 gen format (may be gzipped)
First 5 columns describe variant information, namely
chromosome name position other_allele effect_allele
The remaining data are 3xN columns contain genotype probabilities
