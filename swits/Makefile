slides.pdf: slides.tex preamble.tex contents.tex
slides.pdf: fig/principle-SPOR.pdf
slides.pdf: beamer-didactic.sty

fig/%:
	${MAKE} -C $(dir $@) $(notdir $@)

abstract.pdf: abstract.md
	pandoc -s $^ -o $@

INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/doc.mk
include ${INCLUDE_MAKEFILES}/tex.mk
INCLUDE_BEAMERDIDACTIC=../beamer-didactic
include ${INCLUDE_BEAMERDIDACTIC}/beamer-didactic.mk
