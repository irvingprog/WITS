#!/usr/bin/env python
# -*- coding: utf-8 -*-
from CfgUtils import CfgUtils

calification = CfgUtils('configuration/levels_rating.cfg')

def reset():
	for i in range(1,16):
		calification.write("AfricaEasy",str(i),0)
		calification.write("AfricaMedium",str(i),0)
		calification.write("AfricaHard",str(i),0)

		calification.write("AmericaEasy",str(i),0)
		calification.write("AmericaMedium",str(i),0)
		calification.write("AmericaHard",str(i),0)

def fill():
	for i in range(1,16):
		calification.write("AfricaEasy",str(i),3)
		calification.write("AfricaMedium",str(i),3)
		calification.write("AfricaHard",str(i),3)

		calification.write("AmericaEasy",str(i),3)
		calification.write("AmericaMedium",str(i),3)
		calification.write("AmericaHard",str(i),3)	

reset()