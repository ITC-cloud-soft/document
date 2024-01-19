FROM mcr.microsoft.com/windows/servercore:ltsc2022
ARG INSTALL_JDK=false

# Download the latest self-hosted integration runtime installer into the SHIR folder
COPY SHIR C:/SHIR/
WORKDIR C:/SHIR/

RUN ["powershell", "tzutil.exe /s 'Tokyo Standard Time'; C:/SHIR/build.ps1"]

ENV SHIR_WINDOWS_CONTAINER_ENV True

ENTRYPOINT ["powershell", "C:/SHIR/setup.ps1"]

HEALTHCHECK --start-period=120s CMD ["powershell", "C:/SHIR/health-check.ps1"]
