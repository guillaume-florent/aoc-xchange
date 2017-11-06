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

# corelib (used by aocutils)
RUN cd /tmp && \
    git clone https://github.com/fullmar/corelib && \
    cp -r /tmp/corelib/corelib /usr/local/lib/python2.7/site-packages

# aocutils
# the following command invalidates the cache
# ADD https://api.github.com/repos/guillaume-florent/aoc-utils/git/refs/heads/master version.json
RUN cd /tmp && \
    git clone https://github.com/guillaume-florent/aoc-utils && \
    cp -r /tmp/aoc-utils/aocutils /usr/local/lib/python2.7/site-packages

# aocxchange
# the following command invalidates the cache
# ADD https://api.github.com/repos/guillaume-florent/aoc-xchange/git/refs/heads/master version.json
RUN cd /tmp && \
    git clone https://github.com/guillaume-florent/aoc-xchange && \
    cp -r /tmp/aoc-xchange/aocxchange /usr/local/lib/python2.7/site-packages

RUN cp /tmp/aoc-xchange/bin/step_to_obj /usr/local/bin && \
    cp /tmp/aoc-xchange/bin/step_to_stl /usr/local/bin && \
    chmod +x /usr/local/bin/step_to_stl && \
    chmod +x /usr/local/bin/step_to_obj

CMD ["/bin/bash"]