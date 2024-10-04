  Title       : Stratified Robust Test Scores for Imputed iCOGS Data

  Author      : Andrew Lee, The University of Cambridge
                email: andrewl@srl.cam.ac.uk

  Date        : 24/02/2012

  Description : A collection of programs to calculate the test scores for
                imputed iCOGS data, in impute2 format.


########################################################################################
       COPYWRITE ANDREW LEE, 2012, THE UNIVERSITY OF CAMBRIDGE
       DO NOT EDIT OR DISTRIBUTE ANY OF THIS MATERIAL WITHOUT EXPRESS PERMISSION OF THE AUTHOR
########################################################################################
########################################################################################


Contents : rename_duplicates.py
           convert_impute_2_mach.r
           extract_kinship.r
           create_pheno_file.py
           stratified_robust_score_imputed_data.f90
           stratified_robust_score_imputed_data_IMPUTE2.f90
           file_names.nml
           file_names_IMPUTE2.nml
           test_scores.py
           file_names.py
           README.txt


Usage:
Included in this directory are three methods for calculating the same test statistics.
In both cases we assume that we have the same input data, i.e. data in the IMPUTE2 format.
For example suppose that we have the files
   *imputation_results.txt
   *imputation_results.txt_info
   *imputation_results.sample
   *kinship.Rdata


The first two methods use Fortran:
The first three steps are common to both programs
1) Rename the duplicate snps
   We must first rename the duplicate snps
   $ ./rename_duplicates.py -d imputation_results.txt -i imputation_results.txt_info

   This will create the files :
   imputation_results.txt_renamed_duplicates
   imputation_results.txt_info_renamed_duplicates


2) Create the pheno file
   Create the pheno file using 
   $ ./create_pheno_file.py -i imputation_results.sample

   This will create the file :
   imputation_results.sample_pheno


3) Extract the kinship matrix
   $ ./extract_kinship.r --input_file=kinship.Rdata

   This will create the file :
   kinship.dat


At this point the methods bifurcate.

A) The first method
   This method converts the IMPUTE2 data to MACH output and then processes it using an existing code.

   4) Convert the impute2 data to MACH format
      $ ./convert_impute_2_mach.r --geno_file=imputation_results.txt_renamed_duplicates --info_file=imputation_results.txt_info_renamed_duplicates --sample_file=imputation_results.sample --out_file=mach_imputations

      This will create the files :
      mach_imputations.machdose
      mach_imputations.machinfo
      mach_imputations.machlegend
      imputation_results.txt_renamed_duplicates.dose.fvd
      imputation_results.txt_renamed_duplicates.dose.fvi
      imputation_results.txt_renamed_duplicates.prob.fvd
      imputation_results.txt_renamed_duplicates.prob.fvi


   5) Calculate the test scores
      a) Compile the code using 
         $ gfortran -O3 stratified_robust_score_imputed_data.f90 -o prog_strat.exe

         This will produce the executable file : 
         prog_strat.exe

      b) Enter the file names and analysis type in the file file_names.nml
         $ more file_names.nml
           &filenames
           PHENO_FILE    = 'imputation_results.sample_pheno'
           KINSHIP_FILE  = 'kinship.dat'
           SNP_INFO_FILE = 'mach_imputations.machinfo'
           GENO_FILE     = 'mach_imputations.machdose'
           RESULTS_FILE  = 'score_tests_results.csv'
           OVARIAN       = .FALSE.
           /

         To run breast cancer analysis set: OVARIAN = .FALSE.
         To run ovarian cancer analysis set: OVARIAN = .TRUE.

          c) Execute the code to preform the calculation
          $ ./prog_strat.exe

           The results will be written to the file :
           score_tests_results.csv


B) The second method
   This method uses the IMPUTE2 data directly.


   4) 
      a) Compile the code using
         $ gfortran -O3 stratified_robust_score_imputed_data_IMPUTE2.f90 -o prog_strat_IMPUTE2.exe

      b) Enter the file names and analysis type in the file file_names_IMPUTE2.nml
         $ more file_names_IMPUTE2.nml
           &filenames
           PHENO_FILE    = 'imputation_results.sample_pheno'
           KINSHIP_FILE  = 'kinship.dat'
           GENO_FILE     = 'imputation_results.txt_renamed_duplicates
           RESULTS_FILE  = 'score_tests_results_IMPUTE2.csv'
           OVARIAN       = .FALSE.
           /

         To run breast cancer analysis set: OVARIAN = .FALSE.
         To run ovarian cancer analysis set: OVARIAN = .TRUE.

          c) Execute the code to preform the calculation
          $ ./prog_strat_IMPUTE2.exe

           The results will be written to the file :
           score_tests_results_IMPUTE2.csv


The third method uses python. It shoould be quicker than Fortran for small numbers of snps, 
but slower for larger numbers of files.


1) Rename the duplicate snps (as in Fortran case)
   We must first rename the duplicate snps
   $ ./rename_duplicates.py -d imputation_results.txt -i imputation_results.txt_info

   This will create the files :
   imputation_results.txt_renamed_duplicates
   imputation_results.txt_info_renamed_duplicates


2) Extract the kinship matrix (as in Fortran case)
   $ ./extract_kinship.r --input_file=kinship.Rdata

   This will create the file :
   kinship.dat


3) Run the program 
   a) Enter the file names and analysis type in the file file_names.py
      $ more file_names.py
        pheno_file_name   = 'imputation_results.sample_pheno'
        kinship_file_name = 'kinship.dat'
        geno_file_name    = 'imputation_results.txt_renamed_duplicates
        info_file_name    = 'imputation_results.txt_info'
        results_file_name = 'score_tests_results_py.csv'
        ovarian = False

   b) Run the analysis:
      $ ./test_scores.py

      The results will be written to the file :
      score_tests_results_py.csv

 
 
