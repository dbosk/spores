.PHONY: all
all: slides.pdf
all: abstract.pdf


slides.pdf: slides.tex preamble.tex contents.tex
slides.pdf: beamer-didactic.sty

ART+= 		spores-squads.png
ART+= 		sphinx-route.png
ART+= 		sphinxes-route.png

slides.pdf: ${ART}

%.png: ../art/%.png
	ln $< $@

../%:
	${MAKE} -C $(dir $@) $(notdir $@)

abstract.pdf: abstract.md
	pandoc -s $^ -o $@


.PHONY: clean
clean:
	${RM} abstract.pdf
	${RM} slides.pdf
	${RM} ${ART}
	${MAKE} -C ../art clean


INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/doc.mk
include ${INCLUDE_MAKEFILES}/tex.mk
INCLUDE_BEAMERDIDACTIC=../beamer-didactic
include ${INCLUDE_BEAMERDIDACTIC}/beamer-didactic.mk
