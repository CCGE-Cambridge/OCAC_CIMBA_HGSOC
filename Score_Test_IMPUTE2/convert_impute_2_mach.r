#!/usr/bin/Rscript --vanilla
###############################################################################
#  File        : convert_impute_2_mach.r
#
#  Author      : Andrew Lee, The University of Cambridge
#                email: andrewl@srl.cam.ac.uk
#
#  Date        : 08/02/2012
#
#  Description : Script to extract the kinship matrix from a Rdata file
#                and write it to plain text.
#
#  Usage       : $./convert_impute_2_mach.r --geno_file=<geno_file> --info_file=<info_file> --sample_file=<sample_file> --out_file=<out_file>
#
###############################################################################
#       COPYWRITE ANDREW LEE, 2012, THE UNIVERSITY OF CAMBRIDGE.
#       DO NOT EDIT, DISTRIBUTE OR COPY WITHOUT EXPRESS PERMISSION OF THE AUTHOR.
###############################################################################

#geno_file   <- 'test.impute2_renamed_duplicates'
#info_file   <- 'test.impute2_info_renamed_duplicates'
#sample_file <- '17q21_icogs.sample'
#out_file    <- '17q21'

# 1) parse the command line
initial_options <- commandArgs( trailingOnly = FALSE )

in_geno_file_arg_name <- '--geno_file='
geno_file <- sub( in_geno_file_arg_name, '', 
                  initial_options[ grep( in_geno_file_arg_name, initial_options ) ] )

in_info_file_arg_name <- '--info_file='
info_file <- sub( in_info_file_arg_name, '', 
                  initial_options[ grep( in_info_file_arg_name, initial_options ) ] )

in_sample_file_arg_name <- '--sample_file='
sample_file <- sub( in_sample_file_arg_name, '', 
                    initial_options[ grep( in_sample_file_arg_name, initial_options ) ] )

in_out_file_arg_name <- '--out_file='
out_file <- sub( in_out_file_arg_name, '', 
                 initial_options[ grep( in_out_file_arg_name, initial_options ) ] )


###############################################################################
# 2) Load GenABEL
library( GenABEL )

###############################################################################
# 3) Perform the conversion
impute2mach( geno_file, info_file, sample_file, out_file, maketextdosefile=TRUE )

###############################################################################
# 4) Exit
quit( status = 0 )
###############################################################################
