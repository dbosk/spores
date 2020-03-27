.PHONY: all
all: avail.pdf
all: bw_and_pending_files.pdf bw_mean.pdf bw.pdf
all: completion_vs_size.pdf
all: file_transfer_v2.pdf
all: logistic_many_0-001.pdf
all: nodes_per_layer_vs_theta.pdf
all: outline_figure_only.pdf outline_figure_only.pdf_tex
all: outline.pdf outline.pdf_tex

all: OverviewSPORES_cropped.pdf OverviewSPORES.pdf

OverviewSPORES.pdf: 		OverviewSPORES.pptx
OverviewSPORES_cropped.pdf: OverviewSPORES.pdf
	pdfcrop $< $@

all: pors2.pdf
all: principle_SPOR.pdf
all: sample_usage.pdf
all: success_rate_vs_t.pdf
all: transfer_time_vs_size.pdf

%.pdf %.pdf_tex: svg/%.svg


.PHONY: clean
clean:
	true

.PHONY: distclean
distclean:
	true


INCLUDE_MAKEFILES=../../makefiles
include ${INCLUDE_MAKEFILES}/doc.mk
