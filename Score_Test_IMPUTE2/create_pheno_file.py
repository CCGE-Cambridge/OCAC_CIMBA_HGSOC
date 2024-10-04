#!/usr/bin/python
################################################################################
#
#  File        : create_pheno_file.py
#
#  Author      : Andrew Lee, The University of Cambridge
#                email: andrewl@srl.cam.ac.uk
#
#  Date        : 08/02/2012
#
#  Description : This file takes impute2 output file and creates the pheno file.
#
#  Usage       : $./create_pheno_file.py -i <input_file>
#
################################################################################
#  COPYRIGHT ANDREW LEE 2012
#  DO NOT EDIT, DISTRIBUTE OR COPY  WITH EXPRESS PERMISSION OF THE AUTHOR.
################################################################################
# Import the necessary libraries.
import sys, os, csv, optparse
from os.path import exists

################################################################################
# The required columns
id_col_name       = 'Subject_id'
stratum_col_name  = 'Country_AJ'
family_col_name   = 'globalfamid_num'
bc_pheno_col_name = 'obs_phenotype_bc'
oc_pheno_col_name = 'obs_phenotype_oc'

out_id_col_name       = 'ID'
out_stratum_col_name  = 'Stratum'
out_family_col_name   = 'Family'
out_bc_pheno_col_name = 'Phenotype_bc'
out_oc_pheno_col_name = 'Phenotype_oc'


################################################################################
# Read in the command line arguments and check that all necessary variable are present
# Process command line arguments

# Some default values

# Set up a parser, with the desired options
parser = optparse.OptionParser( conflict_handler = "resolve" )

desc_text = """\n%prog -i <input_file> -o <output_file>

This program takes a file, creates the pheno file.\n"""

parser.set_usage( desc_text )

parser.add_option(
   '-i',
   '--in',
   help = 'Name of the input file',
   dest = 'input_file',
   default = None,
   type = 'string',
   action = 'store'
   )

( options, arguments ) = parser.parse_args( )

# convert the parsed object to local variables
in_file_name  = options.input_file
out_file_name = in_file_name + '_pheno'

################################################################################
# Check that the input files exist

if not exists( in_file_name ):
   print 'ERROR: The input file, "%s", cannot be found.' %( in_file_name )
   print 'STOPPING'
   sys.exit( 1 )


################################################################################
phenotypes = [ id_col_name,
               stratum_col_name,
               family_col_name, 
               bc_pheno_col_name, 
               oc_pheno_col_name ]

out_phenotypes = [ out_id_col_name,
                   out_stratum_col_name,
                   out_family_col_name, 
                   out_bc_pheno_col_name,
                   out_oc_pheno_col_name ]

################################################################################
# Open the input file
try :
   in_file = open( in_file_name, 'r' )
except :
   print 'ERROR: Unable to open the file "%s"' %( in_file_name )
   print 'STOPPING'
   sys.exit( 2 )
in_data = csv.reader( in_file, delimiter = ' ', quotechar = '"' )

# Look for the required columns
# Read in the first line, which should contain the column names
column_names = in_data.next( )

# Determine which colums contian the required phenotypes
# and that all required fields are present
pheno_colmns = [ ]

for pheno in phenotypes :
   if pheno in column_names :
      pheno_colmns.append( column_names.index( pheno ) )
   else :
      print 'No "' + pheno + '" column found in ' + in_file_name
      print 'STOPPING'
      sys.exit( 3 )

# Read in the next line, which is junk
in_data.next( )

################################################################################
# Open the output file
try :
   out_file = open( out_file_name, 'w' )
except :
   print 'ERROR: Unable to open the file "%s"' %( out_file_name )
   print 'STOPPING'
   sys.exit( 2 )
out_data = csv.writer( out_file, delimiter = ' ', quotechar = '"' )

# Write out the column headings
out_data.writerow( out_phenotypes )

# Loop over the remaining lines in the file, and extract the required info.
for line in in_data :
   out_data.writerow( [ line[ i ] for i in pheno_colmns ] )


out_file.close( )
in_file.close( )

sys.exit( 0 )
################################################################################
#     END OF FILE
################################################################################
