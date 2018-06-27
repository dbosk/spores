.PHONY: all
all: spores.pdf

SRC+=		contents.tex abstract.tex
SRC+= 		intro.tex
SRC+= 		system-model.tex

SRC+=		design.tex
SRC+= 		building-blocks.tex 
SRC+= 		squad-overlay-design.tex 
SRC+=		global-overlay-design.tex
SRC+= 		message-passing-design.tex
SRC+=		file-exchange-design.tex

SRC+= 		security-discussion.tex
SRC+= 		evaluation.tex
SRC+= 		related.tex
SRC+=		conclusion.tex

DEPENDS+= 	bibsp.sty meta.bib osn.bib anon.bib be.bib crypto.bib p2p.bib
DEPENDS+= 	otrmsg.bib ac.bib
DEPENDS+= 	adrien.bib
DEPENDS+=	figures/*.pdf

spores.pdf: spores.tex preamble.tex revision_macros.tex
spores.pdf: ${SRC} ${DEPENDS}


.PHONY: clean
clean:
	${RM} spores.pdf


.PHONY: print todo
print: spores.pdf
todo: ${SRC}


INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/doc.mk
INCLUDE_BIBSP=../bibsp
include ${INCLUDE_BIBSP}/bibsp.mk
