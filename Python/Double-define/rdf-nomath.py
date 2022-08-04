import ROOT

LOOP_REPS=500000
N_ENTRIES=10000

verbosity = ROOT.Experimental.RLogScopedVerbosity(ROOT.Detail.RDF.RDFLogChannel(), ROOT.Experimental.ELogLevel.kInfo)

loop = f"int volatile s = 0; for (int i = 0; i < {LOOP_REPS}; ++i){{s += i;}}"

# Spaces are included to make the two strings different, and obtain two different jitted functions.
# If the strings match, the same function will appear in the flame graph
to_be_jitted_calc_x = f" {loop}; return (int)rdfentry_;"
to_be_jitted_calc_y = f"{loop}; return (int)rdfentry_; "

to_be_jitted_sum = f"{loop}; return x+y;"

def use_RDF():
	d = ROOT.RDataFrame(N_ENTRIES)
	dx = d.Define("x", to_be_jitted_calc_x)
	dy = dx.Define("y", to_be_jitted_calc_y)
	dz = dy.Define("z", to_be_jitted_sum)
	c = dz.Sum("z")
	print(c.GetValue())
	
if __name__ == "__main__":

	use_RDF()
