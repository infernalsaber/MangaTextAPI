# MangaTextAPI

An API to search the text of a particular manga
In part, meant to extend [another project](https://github.com/infernalsaber/comic-scans) into a fully-functional API

<!-- **If you want a manga added please raise an PR or contact @fenix.er on discord** -->

## Basic Usage

For eg. to search the word "mari" in Renai Daikou:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/search/renai?q=mari' \
  -H 'accept: application/json'
```
And if you don't know how to convert curl into `<your language of choice>`, use [Curl Convertor](https://curlconverter.com/)

## List of manga supported:

- Renai Daikou
- Brainrot Girlfriend

Planned:
- Mayonaka Heart Tune
- Kaoru Hana wa Rin to Saku
- Oshi no Ko


## API Documentation
TBD