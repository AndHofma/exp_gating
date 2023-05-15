####################################################################################
## Experiment: gating experiment coordinates Potsdam
## cutting_files_into_gates.praat
## script for cutting recordings into gates
## the annotated coordinates will be cut into chunks of syllables
## gate 1: Mo
## gate 2: Moni (incl. possible pause) 
## gate 3: Moni und
## gate 4: Moni und Li
## gate 5: Moni und Lilli (incl. possible pause)
## gate 6: Moni und Lilli und
## gate 7: Moni und Lilli und Manu
##
## Clara Huttenlauch, June 2019
##
####################################################################################

clearinfo

# specify the directory of the folder from which the sound files should be read in
# this folder should contain .wav-files and the corresponding TextGrids
d$ = "C:\Users\Andrea Hofmann\OneDrive\PhD\exp_gating\stimuli\ungated\practice\new\"
Create Strings as file list... list 'd$'*.wav

# specify the directory of the folder for the cut gates
dir$ = "C:\Users\Andrea Hofmann\OneDrive\PhD\exp_gating\stimuli\gated\practice\new\"

# query number of objects in the stringslist and store in variable n
n = Get number of strings
printline number of strings: 'n'

# for-loop, goes through each object in the list
for i from 1 to n
	select Strings list
	filename$ = Get string... 'i'
	Read from file... 'd$''filename$'

	# store basename in variable name
	name$ = selected$ ("Sound")
	# open the corresponding TextGrid
	Read from file... 'd$''name$'.TextGrid

	# query TexGrid and store time points for cutting
	# segments are annotated on tier 3
	tier3 = Get number of intervals... 3
	start = Get start time of interval... 3 2
	e1 = Get end time of interval... 3 3
	
# gate1	
	select Sound 'name$'
	Extract part: 'start', 'e1', "rectangular", 1, "no"
	Save as WAV file... 'dir$''name$'_g1.wav

# gate7
	select TextGrid 'name$'
	e7 = Get start time of interval... 3 'tier3'
	select Sound 'name$'
	Extract part: 'start', 'e7', "rectangular", 1, "no"
	Save as WAV file... 'dir$''name$'_g7.wav

	for j from 5 to tier3-1
		select TextGrid 'name$'
		label3$ = Get label of interval... 3 'j'
		label3_$ = Get label of interval... 3 'j'+1

# gate2
		select TextGrid 'name$'
		if label3_$ = "p1"
			# if there is a pause after name1, it belongs to the gate2
			e2 = Get end time of interval... 3 'j'+1
			select Sound 'name$'
			Extract part: 'start', 'e2', "rectangular", 1, "no"
			Save as WAV file... 'dir$''name$'_g2.wav
		elsif label3$ = "s4"
			# otherwise gate2 ends with name1
			e2 = Get end time of interval... 3 'j'
			select Sound 'name$'
			Extract part: 'start', 'e2', "rectangular", 1, "no"
			Save as WAV file... 'dir$''name$'_g2.wav
	endif

# gate3
		select TextGrid 'name$'
		if label3_$ = "p2"
			# if there is a pause after und1, it belongs to the gate3
			e3 = Get end time of interval... 3 'j'+1
			select Sound 'name$'
			Extract part: 'start', 'e3', "rectangular", 1, "no"
			Save as WAV file... 'dir$''name$'_g3.wav
		elsif label3$ = "c1"
			# otherwise gate3 ends with und1
			e3 = Get end time of interval... 3 'j'
			select Sound 'name$'
			Extract part: 'start', 'e3', "rectangular", 1, "no"
			Save as WAV file... 'dir$''name$'_g3.wav
		endif

# gate4
		if label3$ = "s6"
			select TextGrid 'name$'
			e4 = Get end time of interval... 3 'j'
			select Sound 'name$'
			Extract part: 'start', 'e4', "rectangular", 1, "no"
			Save as WAV file... 'dir$''name$'_g4.wav
		endif

# gate5
		select TextGrid 'name$'
		if label3_$ = "p3"
			# if there is a pause after name2, it belongs to the gate5
			e5 = Get end time of interval... 3 'j'+1
			select Sound 'name$'
			Extract part: 'start', 'e5', "rectangular", 1, "no"
			Save as WAV file... 'dir$''name$'_g5.wav
		elsif label3$ = "s8"
			# otherwise gate5 ends with name2
			e5 = Get end time of interval... 3 'j'
			select Sound 'name$'
			Extract part: 'start', 'e5', "rectangular", 1, "no"
			Save as WAV file... 'dir$''name$'_g5.wav
		endif

# gate6
		select TextGrid 'name$'
		if label3_$ = "p4"
			# if there is a pause after und2, it belongs to the gate6
			e6 = Get end time of interval... 3 'j'+1
			select Sound 'name$'
			Extract part: 'start', 'e6', "rectangular", 1, "no"
			Save as WAV file... 'dir$''name$'_g6.wav
		elsif label3$ = "c2"
			# otherwise gate6 ends with und2
			e6 = Get end time of interval... 3 'j'
			select Sound 'name$'
			Extract part: 'start', 'e6', "rectangular", 1, "no"
			Save as WAV file... 'dir$''name$'_g6.wav
		endif
		
	endfor

printline sound 'name$' processed

endfor

select all
minus Strings list
Remove


