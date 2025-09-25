FROM ubuntu:latest
LABEL authors="tfahrtdinov"

ENTRYPOINT ["top", "-b"]