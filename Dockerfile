FROM python:2.7-alpine

# Run updates.
RUN apk update \
    && apk upgrade \
    && apk add --no-cache nmap nmap-scripts \
        ca-certificates \
        libpcap-dev

# Install Masscan, Source: https://github.com/jessfraz/dockerfiles/blob/master/masscan/Dockerfile 
ENV MASSCAN_VERSION 1.0.5

RUN set -x \
	&& apk add --no-cache --virtual .build-deps \
		build-base \
		clang \
		clang-dev \
		git \
		linux-headers \
	&& rm -rf /var/lib/apt/lists/* \
	&& git clone --depth 1 --branch "$MASSCAN_VERSION" https://github.com/robertdavidgraham/masscan.git /usr/src/masscan \
	&& ( \
	cd /usr/src/masscan \
	&& make \
	&& make install \
	) \
	&& rm -rf /usr/src/masscan \
	&& apk del .build-deps

WORKDIR /asnlookup
COPY asnlookup.py /asnlookup
COPY requirements.txt /asnlookup

RUN pip install -r /asnlookup/requirements.txt
RUN mkdir /asnlookup/output

ENTRYPOINT ["python","asnlookup.py"]
