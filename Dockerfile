#
# Build :
# docker build --tag aocxchange:latest .
#
# Run :
# docker run -ti aocxchange:latest
#
#################################################
# FROM continuumio/miniconda
# FROM show0k/alpine-miniconda
FROM conda/miniconda2

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# numpy + PythonOCC
RUN conda install -y numpy
RUN conda install -c conda-forge -c dlr-sc -c pythonocc -c oce pythonocc-core==0.18 python=2

# aocutils
RUN cd /tmp && git clone https://github.com/guillaume-florent/aoc-utils && cd aoc-utils && python setup.py install

# aocxchange
RUN cd /tmp && git clone https://github.com/guillaume-florent/aoc-xchange && cd aoc-xchange && python setup.py install



# HOW TO MAKE THE CONVERSION SCRIPTS EXECUTABLES?



CMD ["/bin/bash"]