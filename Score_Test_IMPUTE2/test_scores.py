#!/usr/bin/python
################################################################################
#
#  File        : test_scores.py
#
#  Author      : Andrew Lee, The University of Cambridge
#                email: andrewl@srl.cam.ac.uk
#
#  Date        : 20/02/2012
#
#  Description : This file takes impute2 output files and calculates the
#                standard standard chi^2, kinship adjusted and robust score 
#                tests
#
#  Usage       : $./test_scores.py
#
################################################################################
#  COPYRIGHT ANDREW LEE 2012
#  DO NOT EDIT, DISTRIBUTE OR COPY WITH EXPRESS PERMISSION OF THE AUTHOR.
################################################################################
#   This program is written in python
#   It requires the package numpy, which is available from http://numpy.scipy.org/
################################################################################

################################################################################
# Define the input file names.
################################################################################

file_names_file_name = 'file_names.txt'

################################################################################
# Define the column names from the pheno file that we wish to use.
################################################################################

id_col_name       = 'Sample_id'
stratum_col_name  = 'Country_AJ'
family_col_name   = 'globalfamid_num'
bc_pheno_col_name = 'obs_phenotype_bc'
oc_pheno_col_name = 'obs_phenotype_oc'

################################################################################
# Define the column names from the info file that we wish to use.
################################################################################

info_col_names = [ 'exp_freq_a1',
                   'info',
                   'certainty',
                   'type',
                   'info_type1',
                   'concord_type1',
                   'r2_type1',
                   'info_type0',
                   'concord_type0',
                   'r2_type0' ]

info_snp_id_col_name = 'rs_id'

################################################################################
# DO NOT EDIT ANYTHING BELOW THIS LINE
################################################################################
# Import the required libraries

import sys, csv, optparse
from numpy import *

################################################################################
# FUNCTIONS
################################################################################

def file_exists( file_name ) :
   from os.path import exists
   if not exists( file_name ):
      print 'The file "%s" does not exist.' %file_name
      print 'STOPPING'
      sys.exit( 1 )
   return

################################################################################

def bias_corr_var( seq ) :
   # This function calculates the bias-corrected variance (normalised to N - 1 rather than N).
    ubvar = len( seq )*var( seq ) / ( len( seq ) - 1 )
    return ubvar

################################################################################

def subtract_average( data ) :
   # This function takes a sequence of numbers and, calculated the average, and subtracts it.
   seq = array( data )
   seq = seq - average( seq )
   return seq

################################################################################

def start_end( seq ) :
   current_stratum = seq[ 0 ]
   strata_indices = [ ]
   start = 0
   len_stratum = 0
   for i in seq :
      if i == current_stratum :
         len_stratum += 1
      else :
         strata_indices.append( ( start, start + len_stratum ) )
         start += len_stratum
         len_stratum = 1
         current_stratum = i
   strata_indices.append( ( start, start + len_stratum ) )

   return strata_indices

################################################################################

def sort_strata( strata, famalies ) :

   order = lexsort( ( famalies, strata ) )
   strata_indices = start_end( [ strata[ i ]   for i in order ] )
   fam_sorted = [ famalies[ i ] for i in order ]
   famaly_indices = [ ]
   for strat in strata_indices :
      famaly_indices.append( start_end( fam_sorted[ strat[ 0 ] : strat[ 1 ] ] ) )

   return order, strata_indices, famaly_indices

################################################################################
# MAIN PROGRAM
################################################################################

if __name__ == "__main__" :

   # Read in the file names.
   from file_names import *

   # Write the file names to the screen.
   print '\n\npheno_file_name: %s' %pheno_file_name
   print 'kinship_file_name: %s' %kinship_file_name
   print 'geno_file_name: %s' %geno_file_name
   print 'info_file_name: %s' %info_file_name
   print 'results_file_name: %s' %results_file_name
   print 'ovarian: %s' %str(ovarian)


   # Test to see if the input file exists.
   file_exists( pheno_file_name )
   file_exists( kinship_file_name )
   file_exists( geno_file_name )
   file_exists( info_file_name )

   ################################################################################
   # Read in the phenotypic data.

   # Determine the desired columns.
   if ovarian :
      pheno_col_name = oc_pheno_col_name
   else :
      pheno_col_name = bc_pheno_col_name

   phenotypes = [ id_col_name,
                  stratum_col_name,
                  family_col_name,
                  pheno_col_name ]

   # Open the input file.
   pheno_file = open( pheno_file_name, 'r' )
   pheno_data = csv.reader( pheno_file, delimiter = ' ', quotechar = '"' )

   # Read in the first line that should contain the column names.
   column_names = pheno_data.next( )
   # Read the second line as it contians junk.
   pheno_data.next( )

   # Determine which colums contian the required phenotypes
   # and that all required fields are present.
   pheno_colmns = [ ]

   print '\nReading the phenotypes.'
   for pheno in phenotypes :
      if pheno in column_names :
         pheno_colmns.append( column_names.index( pheno ) )
      else :
         print 'No "' + pheno + '" column found in ' + pheno_file_name
         print 'STOPPING'
         sys.exit( 2 )


   # Read in the phenotypes.
   people = [ ]
   for row in pheno_data :
      people.append( [ row[ pheno_colmns[ phenotypes.index( pheno ) ] ] for pheno in phenotypes ] )

   pheno_file.close( )


   # Sort out the correct order.
   order, strat_indicies, fam_indicies = sort_strata( [ person[ 1 ] for person in people ],
                                                      [ person[ 2 ] for person in people ] )

   n_people = len( people )
   n_strata = len( strat_indicies )
   print 'No. people: ', n_people
   print 'No. strata: ', n_strata

   phenos = [ float( people[ i ][ 3 ] ) for i in order ]
   name_order = dict( [ ( people[ order[ i ] ][ 0 ], i ) for i in range( len( order ) ) ] )

   ################################################################################
   # Read in the kinship matrix.

   print '\nReading the kinship matrix.'

   # Open the input file
   kinship_file = open( kinship_file_name, 'r' )
   kinship_data = csv.reader( kinship_file, delimiter = ' ', quotechar = '"' )

   order2 = [ 0 for i in range( n_people ) ]
   kinship = zeros( ( n_people, n_people ), float )
   i = 0
   for row in kinship_data :
      index = name_order[ row[ 0 ] ]
      order2[ index ] = i
      i += 1
      kinship[ index, : ] = row[ 1: ]

   # Close the input file.
   kinship_file.close( )

   # Reoder the columns
   kinship = kinship[ :, order2 ]

   print 'kinship: ', shape( kinship )

   ################################################################################
   # Perform the initial calculations

   print '\nInitial calculations.'

   pheno_strats = [ ]
   for strat in strat_indicies :
      vector = subtract_average( phenos[ strat[ 0 ] : strat[ 1 ] ] )
      strat_kinship = kinship[ strat[ 0 ] : strat[ 1 ], strat[ 0 ] : strat[ 1 ] ]
      num1 = dot( vector, vector )
      num2 = dot( vector, dot( strat_kinship, vector ) )
      pheno_strats.append( ( vector, num1, num2 ) )

   del kinship

   ################################################################################
   # Read in the info file

   print '\nReading in the snp info.'

   # Open the file as a csv reader.
   info_file = open( info_file_name, 'r' )
   info_data = csv.reader( info_file, delimiter = ' ', quotechar = '"' )

   # The first line contains the column names.
   column_names = info_data.next( )

   # Find the column that contains the snp's rs_id
   info_snp_id_col = None
   if info_snp_id_col_name in column_names :
      info_snp_id_col = column_names.index( info_snp_id_col_name )
   else :
      print ( 'WARNING: Unable to find the column "%s" in the file "%s"'
             %( info_snp_id_col_name, info_file_name ) )

   info_columns = [ ]
   info_titles = [ ]
   info = { }

   if info_snp_id_col :
      # Now decide which of the required columns are present
      for col_n in info_col_names :
         if col_n in column_names :
            info_columns.append( column_names.index( col_n ) )
            info_titles.append( col_n )

      # Loop over the lines in the files, extracting the required info.
      for line in info_data :
         info[ line[ info_snp_id_col ] ] = [ line[ n ] for n in info_columns ]

   info_file.close( )

   blank_info = [ '' for n in info_columns ]

   ################################################################################


   print '\nReading the genotypic information.'

   # Increase the size of the csv field limit
   csv.field_size_limit(1000000000)

   # Open the geno file.
   geno_file = open( geno_file_name, 'r' )
   geno_data = csv.reader( geno_file, delimiter = ' ', quotechar = '"' )

   # Open the results file, and write the column headings.
   try :
      results_file = open( results_file_name, 'w' )
   except :
      print 'The file "%s" can not be opened.' %results_file_name
      print 'STOPPING'
      sys.exit( 1 )

   results_data = csv.writer( results_file, delimiter = ',', quotechar = '"' )

   results_data.writerow( [ 'snp_id', 'rs_id', 'position', 'A0', 'A1', 'Score',
                            'Var_standard', 'Var_Kinship', 'Var_Robust', 'Chi_sq',
                            'Kinship_adjusted', 'Robust' ] + info_titles )

   # Loop over the lines in the file.
   for line in geno_data :
      # Split the line
      snp_info = line[ 0: 5 ]

      # Extract the dosages, and sort them to the correct order.
      genos = zeros( ( n_people ), float )
      for i in range( n_people ) :
         genos[ i ] = float( line[ 3*i + 6 ] ) + 2.0*float( line[ 3*i + 7 ] )
      genos = genos[ order ]

      # Reset the rolling sums.
      score  = 0.0
      var_ch = 0.0
      var_ka = 0.0
      var_ro = 0.0

      # Loop over the strata.
      for stratum in range( n_strata ) :

         strat = strat_indicies[ stratum ]
         fams = fam_indicies[ stratum ]
         pheno_vector, num1, num2 = pheno_strats[ stratum ]

         # Create the geno vector.
         geno_vector = subtract_average( genos[ strat[ 0 ] : strat[ 1 ] ] )

         # Calculate it's variance
         variance = bias_corr_var( geno_vector )

         # Calculate the denominators
         score += dot( pheno_vector, geno_vector )
         var_ch += variance*num1
         var_ka += variance*num2
         for fam in fams :
            var_ro += dot( pheno_vector[ fam[ 0 ] : fam[ 1 ] ],
                           geno_vector[  fam[ 0 ] : fam[ 1 ] ] )**2

      # Calculate the test scores
      chi_sq_score  = score**2 / var_ch
      kin_adj_score = score**2 / var_ka
      robust_score  = score**2 / var_ro

      # Write the results to the file.
      if snp_info[ 1 ] in info :
         tmp_info = info[ line[ 1 ] ]
      else :
         tmp_info = blank_info

      results_data.writerow( snp_info + [ score, var_ch, var_ka, var_ro,
                             chi_sq_score, kin_adj_score, robust_score ] +
                             tmp_info )

   # Close the geno and results files.
   geno_file.close( )
   results_file.close( )

################################################################################
# END OF FILE
################################################################################
