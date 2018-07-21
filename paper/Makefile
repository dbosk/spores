.PHONY: all
all: p2p-private-cloud.pdf

SRC+=		contents.tex abstract.tex
SRC+= 		intro.tex
SRC+= 		system-model.tex

SRC+=		design.tex
SRC+= 		sphinxes.tex
SRC+=		spor.tex
SRC+= 		squad-overlay-design.tex 
#SRC+=		file-exchange-design.tex

SRC+= 		security-discussion.tex
SRC+= 		evaluation.tex
SRC+= 		related.tex
SRC+=		conclusion.tex

DEPENDS+= 	bibsp.sty meta.bib osn.bib anon.bib be.bib crypto.bib p2p.bib
DEPENDS+= 	otrmsg.bib ac.bib
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
