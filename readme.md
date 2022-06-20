[![Project Type: Toy](https://img.shields.io/badge/project%20type-toy-blue)](https://project-types.github.io/#toy)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Azure Build Succeeded](https://github.com/prcutler/silversaucer/actions/workflows/main_silversaucer.yml/badge.svg)](https://github.com/prcutler/silversaucer/actions/workflows/main_silversaucer.yml)

# Overview

### Project Status:  Completed

Silver Saucer is a domain I registered many years ago and kept because I like the name. Both the name and the logo are inspired from both a poem by Neil Gaiman, *The Day the Saucers Came* and my love of *The X-Files*.

Silver Saucer's main goal is was a Python learning exercise to integrate my record collection, using the Discogs API, with a website to display album art when an album is chosen or randomly picked.

You can visit [Silversaucer.com](https://silversaucer.com/) to see the site in action.

## Project Goals

The project had three main goals:

* Complete: Build a website that integrates with the Discogs API to display information about an album, either chosen at random or picked specifically.
* Integrate with an Adafruit PyPortal and using CircuitPython, display the album art on the PyPortal.
* Build an "On this Day" feature to display albums released on a specific day.  This required a number of steps to integrate the MusicBrainz into the app.

Want to know more? You can view my [blog posts about Silver Saucer and my progress here](https://paulcutler.org/tags/silver-saucer/).


## Development Goals

* [x] Switch from the Pyramid web framework to the FastAPI framework.
* [ ] Still need to learn testing and 'pytest'.  Just can't wrap my head around it.
* [x] Migrate to Github Actions from Azure Pipelines.
* [x] Learn the Discogs API (and potentially MusicBrainz).
* [x] Learn how to use the CircuitPython MatrixPortal.  (This is more complex than it sounds!)

