#include <ROOT/RLogger.hxx>
#include <ROOT/RDataFrame.hxx>

#include <iostream>
#include <cmath>

#define LOOP_REPS 10000
#define N_ENTRIES 500000

auto verbosity = ROOT::Experimental::RLogScopedVerbosity(ROOT::Detail::RDF::RDFLogChannel(), ROOT::Experimental::ELogLevel::kInfo);

double calc_x(ULong64_t entry)
{
	double s = 1.0;
	for (int i = 0; i < LOOP_REPS; ++i){s = std::sin(s);}
	return s;
}

void use_RDF(void)
{
	auto d = ROOT::RDataFrame(N_ENTRIES);
	auto df = d.Define("x", calc_x, {"rdfentry_"});
	auto s = df.Sum<double>("x");
	
	std::cout << "Complicated result: " << s.GetValue() <<std::endl;
}

int main(void)
{
	use_RDF();
}
