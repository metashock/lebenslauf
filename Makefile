default:
	pdflatex *.tex && evince *.pdf

clean:
	rm -vf *.out *.aux *.log

