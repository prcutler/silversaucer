[![Project Type: Toy](https://img.shields.io/badge/project%20type-toy-blue)](https://project-types.github.io/#toy)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Build Status](https://dev.azure.com/prcutler/Silver%20Saucer/_apis/build/status/prcutler.silversaucer?branchName=main)](https://dev.azure.com/prcutler/Silver%20Saucer/_build/latest?definitionId=8&branchName=main)

# Overview

Silver Saucer is a domain I registered many years ago and kept because I like the name. Both the name and the logo are inspired from both a poem by Neil Gaiman, *The Day the Saucers Came* and *The X-Files*.

Silver Saucer's main goal is to integrate my record collection, using the Discogs API, with my record collection.

## Project Goals

I have separted my goals for the project into three phases to help make it more manageable:

Phase 1 will integrate Discogs to choose a record at random for me to play.

Phase 2  will have me build physical hardware using CircuitPython.  Using a CircuitPython MatrixPortal from Adafruit, after the random record is chosen, I will display the album art on the LED matrix.  (My record player and stereo are in a different room, on the other side of the wall from my home office.)  I will also add the ability to just choose the album that is playing and have the artwork display.

In Phase 3 I hope to build an "On this Day" feature with a web page that shows information from my record collection of things that match the calendar date.  This could include which albums were released, an artist's birthday, etc.  This will be more complicated due to the way Discogs stores some of this information.

## Development Goals

* Switch from the Pyramid web framework to the FastAPI framework.
* Still need to learn testing and 'pytest'.  Just can't wrap my head around it.
* Migrate to Github Actions from Azure Pipelines.
* Learn the Discogs API (and potentially MusicBrainz).
* Learn how to use the CircuitPython MatrixPortal.  (This is more complex than it sounds!)
* Potentially look at deploying this to Azure instead of hosting on Digital Ocean.  But that's a way out.

Want to know more? You can view my [blog posts about Silver Saucer and my progress here](https://paulcutler.org/tags/silver-saucer/).