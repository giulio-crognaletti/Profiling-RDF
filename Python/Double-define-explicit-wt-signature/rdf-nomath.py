import ROOT

LOOP_REPS=500000
N_ENTRIES=10000

verbosity = ROOT.Experimental.RLogScopedVerbosity(ROOT.Detail.RDF.RDFLogChannel(), ROOT.Experimental.ELogLevel.kInfo)

loop = f"int volatile s = 0; for (int i = 0; i < {LOOP_REPS}; ++i){{s += i;}}"

waste_time_str = f"void waste_time(){{ {loop} }}"

ROOT.gInterpreter.Declare(waste_time_str)

ROOT.gInterpreter.Declare(
       f"""int calc_x_with_options(int x, float param, bool opt, double another_param){{
            volatile float a = param;
            volatile bool b = opt;
            volatile double c = another_param; 
            {loop}
            return x+a+b+c;
        }}""")

ROOT.gInterpreter.Declare(
        f"""int calc_y_with_options(int y, bool opt, bool another_opt, unsigned long long param){{
            volatile bool a = opt;
            volatile bool b = another_opt;
            volatile unsigned long long c = param;
            {loop}
            return y+a+b+c;
        }}""")

to_be_jitted_sum = f"waste_time(); return x+y;"

def use_RDF():

    d = ROOT.RDataFrame(N_ENTRIES)
    dx = d.Define("x", "calc_x_with_options((int)rdfentry_, 1.5, true, -2.65e8)")
    dy = dx.Define("y", "calc_y_with_options((int)rdfentry_, true, false, 100201302)")
    dz = dy.Define("z", to_be_jitted_sum)
    c = dz.Sum("z")
    print(c.GetValue())

if __name__ == "__main__":

	use_RDF()
