#!/usr/bin/python
################################################################################
#
#  File        : rename_duplicates.py
#
#  Author      : Andrew Lee, The University of Cambridge
#                email: andrewl@srl.cam.ac.uk
#
#  Date        : 08/02/2012
#
#  Description : This file takes impute2 output files and renames
#                snps that occur more than once.
#
#  Usage       : $./rename_duplicates.py -d <dose_file> -i <info_file>
#
################################################################################
#  COPYRIGHT ANDREW LEE 2012
#  DO NOT EDIT, DISTRIBUTE OR COPY WITH EXPRESS PERMISSION OF THE AUTHOR.
################################################################################
# Import the necessary libraries.
import sys, os, optparse, shutil
from os.path import exists

################################################################################

# Read in the command line arguments and check that all necessary variable are present
# Process command line arguments

# Some default values

# Set up a parser, with the desired options
parser = optparse.OptionParser( conflict_handler = "resolve" )

desc_text = """\n%prog -d <dose_file> -i <info_file>

This program takes a file, and renames any duplicate snps.\n"""

parser.set_usage( desc_text )

parser.add_option(
   '-d',
   '--dose',
   help = 'Name of the dose input file',
   default = None,
   dest = 'dose_input_file',
   type = 'string',
   action = 'store'
   )

parser.add_option(
   '-i',
   '--info',
   help = 'Name of the info input file',
   dest = 'info_input_file',
   default = None,
   type = 'string',
   action = 'store'
   )

( options, arguments ) = parser.parse_args( )

# convert the parsed object to local variables
in_dose_file_name  = options.dose_input_file
in_info_file_name  = options.info_input_file

################################################################################
# Create the the output file names

out_dose_file_name = in_dose_file_name + '_renamed_duplicates'
out_info_file_name = in_info_file_name + '_renamed_duplicates'


################################################################################
# Check that the input files exist

if not exists( in_info_file_name ):
   print 'ERROR: The info file, "%s", cannot be found.' %( in_info_file_name )
   print 'STOPPING'
   sys.exit( 1 )

if not exists( in_dose_file_name ):
   print 'ERROR: The dose file, "%s", cannot be found.' %( in_dose_file_name )
   print 'STOPPING'
   sys.exit( 2 )


################################################################################
# As we wish to rename all the repeated snps (including the initial instance),
# we must first create a list of all the snps.
# We will do this by reading in the the info file

# Create a list of all snps
snps_all = [ ]
info_file = open( in_info_file_name, 'r' )
info_file.next( )
for line in info_file :
   line = line.split( )
   snps_all.append( line[ 1 ] )
info_file.close( )

# Count the total number of snps
n_snps = len( snps_all )

# Create a list of the unique snps
snps_unique = list( set( snps_all ) )

# Create a list of the duplicates
snps_duplicate = [ ]
for snp in snps_unique :
   if snps_all.count( snp ) > 1 :
      snps_duplicate.append( snp )


################################################################################
# Check to see if the list of duplicated snps is empty.
# If it is simpy copy the original files
if len( snps_duplicate ) == 0 :
   shutil.copyfile( in_info_file_name, out_info_file_name )
   shutil.copyfile( in_dose_file_name, out_dose_file_name )
   sys.exit( 0 )

################################################################################
# Read in the files line by line, identify the lines with duplicated names,
# rename them if necessary, and write them out to the new file.

info_file     = open(  in_info_file_name, 'r' )
out_info_file = open( out_info_file_name, 'w' )
out_info_file.write( info_file.next( ) )

dose_file     = open(  in_dose_file_name, 'r' )
out_dose_file = open( out_dose_file_name, 'w' )

counts = [ 0 for i in snps_duplicate ]
for i in range( n_snps ) :
   info_line = info_file.next( ).split( )
   dose_line = dose_file.next( ).split( )
   snp = info_line[ 1 ]
   if dose_line[ 1 ] != snp:
      print 'ERROR: snp names do not agree on line %s: "%s", "%s"' %(
            str( i + 1 ), info_line[ 1 ] ,dose_line[ 1 ] )
      print 'STOPPING'
      info_file.close( )
      out_info_file.close( )
      dose_file.close( )
      out_dose_file.close( )
      sys.exit( 3 )
   if snp in snps_duplicate :
      counts[ snps_duplicate.index( snp ) ] += 1
      snp = snp + '.' + str( counts[ snps_duplicate.index( snp ) ] )
      info_line[ 1 ] = snp
      dose_line[ 1 ] = snp

   out_info_file.write( ' '.join( info_line + [ '\n' ] ) )
   out_dose_file.write( ' '.join( dose_line + [ '\n' ] ) )

info_file.close( )
out_info_file.close( )
dose_file.close( )
out_dose_file.close( )

sys.exit( 0 )
################################################################################
#     END OF FILE
################################################################################
