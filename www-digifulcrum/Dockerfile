FROM nginx

ENV HTML_ROOT /usr/share/nginx/html
ENV GIT_REPO https://github.com/amorphitec/digifulcrum.com.git

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN rm -rvf $HTML_ROOT/*

RUN git clone $GIT_REPO $HTML_ROOT
