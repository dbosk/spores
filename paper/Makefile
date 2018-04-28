.PHONY: all
all: p2p-private-cloud.pdf

SRC+=		contents.tex abstract.tex
SRC+= 		intro.tex
SRC+= 		privacy.tex

SRC+=		design.tex
SRC+= 		building-blocks.tex 
SRC+= 		squad-overlay-design.tex 
SRC+=		global-overlay-design.tex
SRC+= 		message-passing.tex
SRC+=		file-exchange.tex

SRC+= 		security-analysis.tex
SRC+= 		performance.tex
SRC+= 		related.tex
SRC+=		conclusion.tex

DEPENDS+= 	bibsp.sty meta.bib osn.bib anon.bib be.bib crypto.bib p2p.bib
DEPENDS+= 	otrmsg.bib
DEPENDS+= 	adrien.bib
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
