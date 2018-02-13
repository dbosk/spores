.PHONY: all
all: p2p-private-cloud.pdf

SRC+=		p2p-private-cloud.tex preamble.tex revision_macros.tex
SRC+=		contents.tex abstract.tex intro.tex related.tex
SRC+= 		algorithm.tex

DEPENDS+= 	bibsp.sty

p2p-private-cloud.pdf: ${SRC}


.PHONY: clean
clean:
	${RM} p2p-private-cloud.pdf


.PHONY: print todo
print: p2p-private-cloud.pdf
todo: ${SRC}


INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/doc.mk
INCLUDE_BIBSP=../bibsp
include ${INCLUDE_BIBSP}/bibsp.mk
