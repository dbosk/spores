.PHONY: all
all: p2p-private-cloud.pdf

SRC+=		preamble.tex
SRC+=		abstract.tex contents.tex

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
