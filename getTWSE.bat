@echo off
start /wait python getTWSE/index.py
start /wait node getTWSE/filter.js
start /wait node node getTWSE/run.js