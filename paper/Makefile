.PHONY: all
all: paper.pdf

SRC+=		contents.tex abstract.tex
SRC+= 		intro.tex
SRC+=		UCOR.tex
SRC+= 		sphinxes.tex sphinxes-security.tex
SRC+=		spor.tex spor-security.tex
SRC+=		spores.tex spores-security.tex

#SRC+= 		system-model.tex

#SRC+= 		squad-overlay-design.tex 
#SRC+=		file-transfer-design.tex

SRC+= 		evaluation.tex
SRC+= 		related.tex
SRC+=		conclusion.tex

DEPENDS+= 	bibsp.sty meta.bib osn.bib anon.bib be.bib crypto.bib p2p.bib
DEPENDS+= 	otrmsg.bib ac.bib privacy.bib
DEPENDS+= 	adrien.bib spores.bib
DEPENDS+=	figures/*.pdf
DEPENDS+= 	acrox.sty

paper.pdf: paper.tex preamble.tex revision_macros.tex
paper.pdf: ${SRC} ${DEPENDS}

figures/%::
	${MAKE} -C $(dir $@) $(notdir $@)

acrox.sty: ../acrox/acrox.sty
	${LN} $^ $@

../acrox/acrox.sty:
	${MAKE} -C $(dir $@) $(notdir $@)

.PHONY: clean
clean:
	${RM} paper.pdf
	${MAKE} -C figures clean
	${RM} acrox.sty
	${MAKE} -C ../acrox clean

.PHONY: distclean
distclean:
	${MAKE} -C figures distclean
	${MAKE} -C ../acrox distclean


.PHONY: print todo
print: paper.pdf
todo: ${SRC}


INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/doc.mk
INCLUDE_BIBSP=../bibsp
include ${INCLUDE_BIBSP}/bibsp.mk
