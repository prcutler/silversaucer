[![Build Status](https://dev.azure.com/prcutler/Silver%20Saucer/_apis/build/status/prcutler.silversaucer?
branchName=main)](https://dev.azure.com/prcutler/Silver%20Saucer/_build/latest?definitionId=8&branchName=main)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=prcutler/silversaucer)](https://dependabot.com)

# Overview

Silver Saucer originally started as an idea for a business name ten years ago when I considered going into business for myself.  I quickly decided consulting wasn't for me, but I've kept the domain name all these years.  The logo is inspired from both a poem by Neil Gaiman, *The Day the Saucers Came* and *The X-Files*.

I have five current goals of thing I want to learn by building Silver Saucer:

## Pyramid

It’s my third project using the [Pyramid web framework](https://www.trypyramid.com).  I don’t have an urge to learn Flask or another framework - I would like to get better at Pyramid, which I know a little.  I also really like the Pyramid community.  The few times I’ve become stuck and asked for help in the Pyramid IRC channel, they’ve been both welcoming and helpful.  My first two Pyramid projects were based on the first training Talk Python offered for Pyramid, which used a package called `pyramid_handlers` which is no longer the recommend way to build a web app in Pyramid.  I’m doing it the recommended way this time, using a class based approach.

*Status: 75%*

## Bootstrap and CSS
I know a little of HTML, enough to get by.  But CSS and Bootstrap, not so much.  I’ve already integrated a Bootstrap theme and tweaked it where it’s almost working, but I’m just hacking at it - I don’t really know what I’m doing and it’s something I want to get better at.  I should probably find some good HTML / CSS tutorials and go through those.

*Status: 10%*

## Discogs API Integration
The goal for Silversaucer.com is to integrate with the [Discogs API](https://www.discogs.com/developers/)).  Discogs.com is a website that lets you catalog your record collection and also includes community features and a marketplace where you can buy and sell records (or CDs or almost any kind of media).  There are two things I want to build using the Discogs API:

### Play a random record
I know that Discogs already has a feature on their website where you can have it randomly choose an item in your collection and if you shake the mobile app it will also show you a random item in your collection.  I want to take that to the next level and sort by type (record, 45, CD, etc.).

### On this day
The second things I want to build is a page that shows all records released for today’s date.  This one is going to be more complicated and I’ll share more in a separate blog post.

*Status: 30%*

## Testing
I’ve blogged about it before, but I struggle to learn `pytest`.  I’m going to continue to try and learn more about software testing, starting with this app.

*Status: Not started*

## Infrastructure
I’ve already hooked up Silver Saucer to Azure Pipelines to automatically do continuous integration.  I want to integrate `pytest` and code coverage next.  After that I may look into continuous delivery, but there’s is a lot about Azure that I don’t know. 

*Status: 25%*

You can view my [blog posts about Silver Saucer and my progress here](https://paulcutler.org/tags/silver-saucer/).
