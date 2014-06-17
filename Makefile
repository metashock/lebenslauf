default:
	pdflatex *.tex && evince *.pdf

clean:
	rm -v *.out *.aux *.log

