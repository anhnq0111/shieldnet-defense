FROM public.ecr.aws/o5x5t0j3/amd64/api_development:integration_test_shieldnet-defend-generic

ARG SHIELDNET_DEFEND_BRANCH

## install ShieldnetDefend
RUN mkdir shieldnetdefend && curl -sL https://github.com/shieldnetdefend/shieldnetdefend/tarball/${SHIELDNET_DEFEND_BRANCH} | tar zx --strip-components=1 -C shieldnetdefend
ADD base/agent/preloaded-vars.conf /shieldnetdefend/etc/preloaded-vars.conf
RUN /shieldnetdefend/install.sh

COPY base/agent/entrypoint.sh /scripts/entrypoint.sh

HEALTHCHECK --retries=900 --interval=1s --timeout=40s --start-period=30s CMD /usr/bin/python3 /tmp_volume/healthcheck/healthcheck.py || exit 1
