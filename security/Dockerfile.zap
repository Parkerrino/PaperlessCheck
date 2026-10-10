FROM ghcr.io/zaproxy/zaproxy:stable
USER root
RUN mkdir -p /zap/wrk && chown zap:zap /zap/wrk
USER zap
WORKDIR /zap/wrk
