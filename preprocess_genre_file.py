import subprocess

# Take in an ATF file, split it into several temporary files by document
# or maybe modify Nuolenna to add in these markers in the unicode file it makes?
# Maybe this is unnecessary and we should go by lines in a document?

# A good place to split would be around here:
# &P424664 = BAM 5, 498 (Rm 254)
# atf: lang akk 
# @tablet 
# Splitting at the '=' would work, @tablet wouldn't necessarily work since there are a few inscriptions not on a tablet
# perhaps at the '&' character, since a line like this can appear: &P396882 = BAM 512 = K 6894 -- Geer’s J 105




# Run each document by Nuolenna

# Combine the results into a single file

# Based on User Input in the argument, generate a file of class labels
# To go the with the combined file


