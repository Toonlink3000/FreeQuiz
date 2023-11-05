import importlib.util
import os
import sys
#from tkinter import *\\

QUESTION_TYPES = {}
QTYPE_MODULES = {}	

def scan_type_plugins():
	#maybe needs to be changed for os independance?
	files = os.listdir("./qtype")
	pyfiles = []
	for file in files:
		if file.endswith(".py"):
			#python file
			if file == "base.py":
				continue

			#redo for cross platrofm.....
			spec = importlib.util.spec_from_file_location("module.name", "qtype/" + file)
			modu = importlib.util.module_from_spec(spec)
			sys.modules["module.name"] = modu
			spec.loader.exec_module(modu)

			type_name = file[:len(file)-3]

			QUESTION_TYPES[type_name] = modu.type_class
			QTYPE_MODULES[type_name] = modu