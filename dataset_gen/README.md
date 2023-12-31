# Dataset tools documentation

## Generating a dataset
A pre-generated dataset is provided under dataset/Model.zip, but perhaps you want to generate your own improved dataset, or generate a slightly different one for a different classification problem.

### Obtain the CDLI transliterations (ATF files)
1. Head to CDLI, we classified by genres, so headed to https://cdli.mpiwg-berlin.mpg.de/genres
2. Click on different genres, then click to view the artifacts.
3. Change from the tile view to the list view, at the bottom of the page, select 1000 results per page.
4. Open filters, transliteration > With, apply this filter. Then apply any other filters you want (in our case, the only other filter was the genre filter, provided we wanted to exclude certain sub-genres).
5. Click 'Export', then "As ATF". This will download all 1000 current transliterated results as a single ATF file we can process later.
6. Click onto the next page and repeat the export step for however many pages of data you want. Generally you will want to err on the side of more, especially for categories such as Administrative which have lots of small or incomplete documents.
** Note that the dataset generation tool assumes every document in a single ATF file is of the same class, if this assumption does not hold true for your case, you will have to modify nuolenpy.py

### Folders
1. In the dataset folder, create the following sub-folders:
- ATF
- Model
- Unicode
- debug (optional, for developers)
2. Drop your ATF files in the ATF folder
### Generating the Dataset
1.  For each ATF file, run the following: `python nuolenpy.py ATF/Example.atf Label_Name -s -d > Unicode/Example.txt`
- This will convert the ATF file to a unicode representation, with each document within the file separated by `"NEWDOC Label_Name"`.
- The `-s` option tells nuolenpy to preserve spaces between words on the same line. Technically real cuneiform was not written this way, but this allows language models to make use of start and end of word information. 
- The `-d` option adds the document separators
- An extra option for developes is `-a`, which makes the program print any characters which couldn't be matched in the sign list in their ascii representation, examples from ours include `[biṭ₂]`, `[šeriš]`. This is very useful for debugging or improving the conversion tool.
2.  In your dataset/Model folder, create `train.data.txt`, `train.label.txt`, do the same for `dev` and `test`, you should have 6 text files in total, do not write anything into these files.
3. Run `python gen_datasets.py` This script will grab every text file in /Unicode and split it roughly evenly into training, development, and testing subsets under the model folder.
- Note that for now, this script also relies on the assumption of one Label per unicode .txt file, removing this assumption would be a good improvement.
4. Do any manual cleanup of the data that is needed.
5. You have now generated your own Cuneiform dataset!

## Nuolenpy.py code
### Layout
#### def load\_sign\_list(ascii_debug=False)
- Loads the ascii and unicode representation pairs from sign_list.txt
#### def toUnicode(atfName,label,doc\_markers,spaces,ascii\_debug=False)
- Converts to ATF transliteration files to a  unicode representation of the cuneiform
#### main
- Collects user parameters and runs the program
### Limitations and potential improvement
 Known issues:
- incomplete sign list (no proto cuneiform among other missing word)
 - \_kun4!(|ID+LU|)\_ misses ID and LU
 - |šu₂.3xan| will make the 3 into a subscript
- some repetitions will be off due to preceding characters ex "ZUTA651xKA" might give 51 ka characters
- More examples of signs not in the sign list:
[biṭ₂], [enuru],[sila₂],[shar],[kamad],[šeriš]

## gen_datasets.py code
### Layout
#### def parse\_file(file,trainData,trainLabels,devData,devLabels,testData,testLabels)
Finds the label of the documents in a /Unicode file, and splits the files by "NEWDOC". writes the documents to one of the file descriptor passed to it by the main process
#### main
- Opens all the files used in the final dataset, and every file in the /Unicode folder and distribute the documents to form the dataset.
### Limitations and potential improvement
- This script requires that the .data.txt and the .label.txt files be already created.
- Only the first label in a unicode file matters, it is assumed that all following labels would be the same. This assumption holds for the current version of nuolenpy.py