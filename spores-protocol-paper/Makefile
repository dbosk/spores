.PHONY: all
all: spores.pdf

SRC+=		contents.tex abstract.tex
SRC+= 		intro.tex
SRC+= 		system-model.tex
SRC+= 		approach.tex

SRC+= 		sphinxes.tex
SRC+=		design.tex spor.tex file-transfer-design.tex

SRC+= 		security-discussion.tex
SRC+= 		related.tex
SRC+=		conclusion.tex

DEPENDS+= 	bibsp.sty meta.bib osn.bib anon.bib be.bib crypto.bib p2p.bib
DEPENDS+= 	otrmsg.bib ac.bib privacy.bib
DEPENDS+= 	spores.bib
DEPENDS+=	$(wildcard figures/*.pdf)

spores.pdf: spores.tex usenix2019_v3.sty preamble.tex revision_macros.tex
spores.pdf: ${SRC} ${DEPENDS}

figures/%::
	${MAKE} -C $(dir $@) $(notdir $@)


usenixart.sty: usenixart/usenixart.sty
	${LN} $^ $@


.PHONY: clean
clean:
	${RM} spores.pdf
	${MAKE} -C figures clean

.PHONY: distclean
distclean:
	${MAKE} -C figures distclean
	${RM} usenix2019_v3.sty


.PHONY: print todo
print: spores.pdf
todo: ${SRC}


INCLUDE_MAKEFILES=../makefiles
include ${INCLUDE_MAKEFILES}/tex.mk
include ${INCLUDE_MAKEFILES}/doc.mk
INCLUDE_BIBSP=../bibsp
include ${INCLUDE_BIBSP}/bibsp.mk
