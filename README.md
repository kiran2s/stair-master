# Stair Master: Artificial Creature Evolution in Stair Climbing

### Abstract

There have previously been works in creating artificial models that evolve using 
information from the environment in order to become more fit. 
In this paper, we present one such experiment in which a snake-like model learns to 
climb stairs over multiple generations using the information of how successful models 
in the previous generation were. The paper details the specifications of our simulation, 
the implementation using a Python library called Panda3D, and an analysis 
of the model's evolution.

[Full Report](./submission/report/evolution-artificial-creatures.pdf)

### To run StairMaster.py:
1) Install panda3d via:
	1.1) pip install panda3d
	or for Windows:
	1.2) https://www.panda3d.org/download.php

2) Move .egg files (s0-9.egg and rectangle.egg) in src folder into:
	For Mac/Linux:
		/usr/local/lib/python2.7/site-packages/panda3d/models/
	For Windows:
		C:\Python27\Lib\site-packages\panda3d\models\

3) python StairMaster.py
