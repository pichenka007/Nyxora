

def close(code=0, trace=None):
	if not trace:
		info(f"Program successfully terminated with code: {code}")
	else:
		info(f"Error: Program terminated with error code: {code}")
		info(f"Trace Back: {trace}")
		input("Enter to close")
	sys.exit()