# hackatech_ovh


## Build docker image
Set in repo directory
> cd hackatech_ovh



Launch image building (will use existing Dockerfile)
> docker build -t scrap_hackaton .

Building should take ~5 minutes.

Then Check if docker is available :
> docker images | grep scrap_hackathon

Image size should be ~125MB.


## To run an extract on hostadvice website using builded docker image:

> docker run --detach --mount type=bind,source="$(pwd)"/scrap_data,target=/scrap_data scrap_hackhaton https://hostadvice.com/hosting-company/ddos-guard-reviews/en-fr/

Folder scrap_data is mounted on the container as a shareable folder.



## To run extracts in parallel ( will use the list of companies available in companies_url.txt), use parallel_scrap.sh script.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tdenimal/hackatech_ovh/master?filepath=index.ipynb)
