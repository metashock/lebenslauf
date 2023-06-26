# Thanks to: https://tex.stackexchange.com/a/442652
FROM ubuntu

RUN ln -snf /usr/share/zoneinfo/Etc/UTC /etc/localtime \
    && echo "Etc/UTC" > /etc/timezone \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra xzdec -y \
    && rm -rf /var/lib/apt/lists/* \
