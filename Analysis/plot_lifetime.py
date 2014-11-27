###########
# Header  #
###########




###########
# Imports #
###########

import argparse

# import everything we need from kafe
from kafe import *
from kafe.function_library import exp_2par, exp_3par

from numpy import exp, cos

###################
# Argument-Parser #
###################

def argumente():
	"""Diese Funktion liest Argumente von der Kommandozeile ein."""
	parser = argparse.ArgumentParser()

	parser.add_argument('-f', '--filename', type=str, default=" ",
	help="Name of the file to analyze.")
	parser.add_argument('-o', '--offset', action="store_true",
	help="Fitting an exponential function with or without offset to the muon lifetime data. Default is True = with offset.")
			
	return parser.parse_args()


################
# Fit-Function #
################

#def decay_function(x,N=38000,a_c=1,tau_c=1,a_mu=1,tau_mu=2.2,a_b=1,tau_b=3,a_n=1,tau_n=0.1):
#	return N*(a_c*exp(-x/tau_c)+a_mu*exp(-x/tau_mu)+a_b*exp(-x/tau_b)+a_n*exp(-x/tau_n))

#def decay_function(x,N=38000,a_c=1,lambda_c=1,a_m=1,lambda_m=2.2):
#	return N*(a_c*exp(-x*lambda_c)+a_m*exp(-x*lambda_m))

#def decay_function(x,N=100,a=1,b=1,tau_c=0.3,tau_mu=2.2):
#	return N*(a*exp(-x/tau_c)+b*exp(-x/tau_mu))

#def decay_function(x,a=10,tau_c=0.5,b=7,tau_m=2.2):
#	if x<= splitter:
#		return a-x*tau_c
#	else:
#		return b-x*tau_m


############
# Workflow #
############

opt=argumente()



# load the experimental data from a file
my_dataset = parse_column_data(
    opt.filename,
    field_order="x,y,yabserr",
    title="Decay Time"
)
# Create Fit-Object
my_fit = Fit(my_dataset,
             exp_2par)

# Create first to find the splitting point
print 'Creating logarithmic plot to analyse and finding the splitting point\n'

my_plot = Plot(my_fit,ylog=True, )
my_plot.axis_labels = ['$t [ms]$', '$events$']
my_plot.plot_all(show_function_for=None)
my_plot.show()

#Ask for the splitting point
print 'Enter the point of the time-axis, where the the slope gets smaller:'
splitter=float(input())
#print '\n'+'splitter=' + str(splitter) + '\n'

#Generating two data sets divided by splitter
firstobj=open("before_splitter.dat", "w")
secondobj=open("after_splitter.dat", "w")

with open(opt.filename,"r") as data:
	linecounter=0
	for line in data:
		linecounter=linecounter+1
		line.strip()
		spl=line.split('\t')
		if linecounter == 1:
			firstobj.write(str(line))
			secondobj.write(str(line))
		elif float(spl[0]) < splitter:
			firstobj.write(str(line))
		else:
			secondobj.write(str(line))

firstobj.close()
secondobj.close()

#####################################
# Creating dataset-objects for fits #
#####################################

first_dataset = parse_column_data(
    'before_splitter.dat',
    field_order="x,y,yabserr",
    title="Decay Time"
)
second_dataset = parse_column_data(
    'after_splitter.dat',
    field_order="x,y,yabserr",
    title="Decay Time"
)

############################################
# Creating Fit-objects and performing fits #
############################################

first_fit = Fit(first_dataset,
             exp_3par)
             
            
if opt.offset:
	second_fit = Fit(second_dataset,
             exp_3par)
else:
	second_fit = Fit(second_dataset,
             exp_2par)
            
first_fit.do_fit()
second_fit.do_fit()


###########################################
# Creating Plot-Object with data and fits #
###########################################

final_plot =Plot(my_fit,second_fit,ylog=True) 
final_plot.axis_labels = ['$t [ms]$', '$events$']
final_plot.plot(0,show_function=False)
final_plot.plot(1,show_data=False)
#final_plot.plot(2,show_data=False)
final_plot.show()
final_plot.save("lifetime_plot.pdf")
