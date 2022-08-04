#include <ROOT/RLogger.hxx>
#include <ROOT/RDataFrame.hxx>

#include <iostream>

#define LOOP_REPS 500000
#define N_ENTRIES 10000

auto verbosity = ROOT::Experimental::RLogScopedVerbosity(ROOT::Detail::RDF::RDFLogChannel(), ROOT::Experimental::ELogLevel::kInfo);

void waste_time(void)
{
        int volatile s = 0;
	for (int i = 0; i < LOOP_REPS; ++i){s += i;}
}

int calc_x(ULong64_t entry)
{
        waste_time();
        return (int)entry;
}

int calc_y(ULong64_t entry)
{
        waste_time();
        return (int)entry;
}


void use_RDF(void)
{
	auto d = ROOT::RDataFrame(N_ENTRIES);
	auto dx = d.Define("x", calc_x, {"rdfentry_"});
	auto dy = dx.Define("y", calc_y, {"rdfentry_"});
	auto dz = dy.Define("z", [](int x, int y){waste_time(); return x+y;}, {"x","y"});
	auto s = dz.Sum<int>("z");
	
	std::cout << "Complicated result: " << s.GetValue() <<std::endl;
	std::cout << "I am Double Define :D" << std::endl;
}

int main(void)
{
	use_RDF();
}
