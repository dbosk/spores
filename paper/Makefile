.PHONY: all
all: p2p-private-cloud.pdf

SRC+=		p2p-private-cloud.tex contents.txt preamble.tex revision_macros.tex
SRC+=		abstract.tex intro.tex related.tex

p2p-private-cloud.pdf: p2p-private-cloud.tex
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
