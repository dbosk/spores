.PHONY: all
all: p2p-private-cloud.pdf

SRC+=		contents.tex abstract.tex
SRC+= 		intro.tex
SRC+= 		privacy.tex
SRC+= 		user-model.tex
SRC+= 		algorithm.tex
SRC+= 		related.tex

DEPENDS+= 	bibsp.sty meta.bib osn.bib anon.bib
DEPENDS+=	figures/*.pdf

p2p-private-cloud.pdf: p2p-private-cloud.tex preamble.tex revision_macros.tex
p2p-private-cloud.pdf: ${SRC} ${DEPENDS}


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
