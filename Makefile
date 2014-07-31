cv:
	pdflatex 'Thorsten Heymann.tex' && evince 'Thorsten Heymann.pdf'

clean:
	rm -vf *.out *.aux *.log

