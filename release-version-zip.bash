#!/bin/bash

version="0.3.2"
zipName="plugin.video.yogaglo-$version.zip"

zip -r $zipName . -x=*.git* -x=\.* -x=*test* -x=*.org -x=*.bash
