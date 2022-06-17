[![Project Type: Toy](https://img.shields.io/badge/project%20type-toy-blue)](https://project-types.github.io/#toy)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Build Status](https://dev.azure.com/prcutler/Silver%20Saucer/_apis/build/status/prcutler.silversaucer?branchName=main)](https://dev.azure.com/prcutler/Silver%20Saucer/_build/latest?definitionId=8&branchName=main)

# Overview

Silver Saucer is a domain I registered many years ago and kept because I like the name. Both the name and the logo are inspired from both a poem by Neil Gaiman, *The Day the Saucers Came* and my love of *The X-Files*.

Silver Saucer's main goal is to integrate my record collection, using the Discogs API, with a website to display album art when an album is chosen or randomply picked.

## Project Goals

I have separated my goals for the project into three phases to help make it more manageable:

Phase 1 - Complete: Build a website that integrates with the Discogs API to display information about an album. 

Phase 2 - Complete:  Using an Adafruit PyPortal, build a display that automatically displays album art for the album chosen on SilverSaucer.com.

Phase 3 - 50%: Build an "On this Day" feature that displays which albums were released on a given day. As of June 2022, this is 50% complete.  Using `discodos`, I was able to get about half of the MusicBrainz IDs for my collection and I have built a form to manually enter the other 50%.  I have already integrated MusicBrainz's API  to fetch the release day, which Discogs doesn't have (only year) and this can run after all MusicBrainz IDs are stored in the database.

## Development Goals

* [x] Switch from the Pyramid web framework to the FastAPI framework.
* [ ] Still need to learn testing and 'pytest'.  Just can't wrap my head around it.
* [x] Migrate to Github Actions from Azure Pipelines.
* [x] Learn the Discogs API (and potentially MusicBrainz).
* [x] Learn how to use the CircuitPython MatrixPortal.  (This is more complex than it sounds!)
* [ ] Learn how to use HTMX in place of Javascript.
* [ ] Potentially look at deploying this to Azure instead of hosting on Digital Ocean.  But that's a way out.

Want to know more? You can view my [blog posts about Silver Saucer and my progress here](https://paulcutler.org/tags/silver-saucer/).