import pickle

def unpickle(filename):
    inputfile = open(filename,'rb')
    pickled = pickle.load(inputfile)
    inputfile.close()
    return pickled

def nupickle(data,filename):
    outputfile = open(filename,'wb')
    pickle.dump(data,outputfile,protocol=pickle.HIGHEST_PROTOCOL)
    outputfile.close()

# Object stored is a dict, of the form:
# datadict = {"flow_mean_mlpermin": np.array(aq),
#             "flow_std_mlpermin": np.array(aqstd),
#             "avg_time_s": avg_time_end - avg_time_start,
#             "flow_imposed_mlpermin": flowrates}