#!/bin/sh

ffmpeg -i rock.webm -vf fps=30 rock/out%d.png
ffmpeg -i paper.webm -vf fps=30 paper/out%d.png
ffmpeg -i scissors.webm -vf fps=30 scissors/out%d.png
