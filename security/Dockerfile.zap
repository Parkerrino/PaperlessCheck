FROM ghcr.io/zaproxy/zaproxy:stable
# checkov:skip=CKV_DOCKER_2:One-shot scan job, not a service; runner enforces timeout, exit status and report validation.
USER root
RUN mkdir -p /zap/wrk && chown zap:zap /zap/wrk
USER zap
WORKDIR /zap/wrk
