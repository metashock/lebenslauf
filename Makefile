.PHONY: cv preview clean

cv: ./data/cv.en.yml
	python3 rendercv.py > cv.tex
	./pdflatex

preview: cv
	evince cv.pdf

clean:
	rm -vf *.out *.aux *.log

