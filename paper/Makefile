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

FIGURES+= 	figures/probabilistic-routes-cropped.png
FIGURES+= 	figures/incremental-onion-routing-cropped.png

p2p-private-cloud.pdf: p2p-private-cloud.tex preamble.tex revision_macros.tex
p2p-private-cloud.pdf: ${SRC} ${DEPENDS} ${FIGURES}

probabilistic-routes-cropped.png: figures/probabilistic-routes.png
incremental-onion-routing-cropped.png: figures/incremental-onion-routing.png

%-cropped.png: %.png
	convert -trim $< $@



.PHONY: clean
clean:
	${RM} p2p-private-cloud.pdf
	${RM} figures/*-cropped.png


.PHONY: print todo
print: p2p-private-cloud.pdf
todo: ${SRC}


INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/doc.mk
INCLUDE_BIBSP=../bibsp
include ${INCLUDE_BIBSP}/bibsp.mk
