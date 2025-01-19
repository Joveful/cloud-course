FROM alpine:3.18

WORKDIR /app

ENV COUNT=8 MSG="Hello Docker!"

COPY lucas.sh echo.sh ./
CMD ["./echo.sh", "./lucas.sh"]
