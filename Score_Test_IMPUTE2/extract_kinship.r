#!/usr/bin/Rscript --vanilla
###############################################################################
#  File        : extract_kinship.r
#
#  Author      : Andrew Lee, The University of Cambridge
#                email: andrewl@srl.cam.ac.uk
#
#  Date        : 09/02/2012
#
#  Description : Script to extract the kinship matrix from a Rdata file
#                and write it to plain text.
#
#  Usage       : $./extract_kinship.r --input_file=<in_file_name>
#
###############################################################################
#       COPYWRITE ANDREW LEE, 2012, THE UNIVERSITY OF CAMBRIDGE
#       DO NOT EDIT, DISTRIBUTE OR COPY WITHOUT EXPRESS PERMISSION OF THE AUTHOR
###############################################################################
# Should read in the name from the command line.
rm( list = ls( all = TRUE ) )

#infile  <- "../DATA/kinship.brca1.icogs.forScore.Rdata"

# First the input file
initial_options <- commandArgs( trailingOnly = FALSE )
in_file_arg_name <- '--input_file='
in_file_name <- sub( in_file_arg_name, '', initial_options[ grep( in_file_arg_name,
                     initial_options ) ] )

###############################################################################
load( in_file_name )

rm( in_file_name, in_file_arg_name, initial_options )

all_objects <- ls( )
found <- FALSE
for( i in 1:length( all_objects ) ){
   obj_class <- class( get( all_objects[[ i ]] ) )
   if( length( obj_class ) != 1 ){
      next
   }
   if( obj_class == 'matrix' ){
      input_data <- all_objects[[ i ]]
      found <- TRUE
      break
   }
}
outfile <- paste( input_data, '.dat', sep = "" )

write.table( get( input_data ), file = outfile, sep = " ", row.names = TRUE, col.names = FALSE )
quit( status = 0 )
###############################################################################
