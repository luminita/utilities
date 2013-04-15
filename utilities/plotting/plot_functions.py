'''
Plotting functions
'''

import matplotlib.pyplot as pyplot   


def plot_scatterplot_series(data_x, data_y, labels, colors_markers=None, \
        markersize=5.0, xlabel='', ylabel='', legend_location='lower right', \
        xlim=None, ylim=None, out_file=None, format_file='png'):
    i = 0
    while i < len(data_x):
        if colors_markers != None:
            pyplot.plot(data_x[i], data_y[i], colors_markers[i], \
                    markersize=markersize, label=labels[i])
        else:
            pyplot.plot(data_x[i], data_y[i], marker='o', markersize=markersize, \
                    label=labels[i], linewidth=0.0)
        i += 1
    pyplot.xlabel(xlabel, fontsize=20)                
    pyplot.ylabel(ylabel, fontsize=20)                
    if legend_location != None:
        pyplot.legend(loc=legend_location)
    if xlim != None:
        pyplot.xlim(xlim)
    if ylim != None:
        pyplot.ylim(ylim)        
    if out_file != None:
        pyplot.savefig(out_file+"."+format_file, format=format_file)
    else:
        pyplot.show()
    pyplot.cla()
    pyplot.close()
    

def plot_boxplot(matrix, xticks, labelx, labely, xticks_rotation=45, \
        xlimits=None, ylimits=None, no_tch=1, vertical=1, title=None, \
        dpi=100, filename=None):
    pyplot.boxplot(matrix, notch = no_tch, vert = vertical, \
            sym = "")
    pyplot.xlabel(labelx, fontsize = 20)
    pyplot.ylabel(labely, fontsize = 20)
    if ylimits != None:
        pyplot.ylim(ylimits)
    if xlimits != None:
        pyplot.xlim(xlimits)
    pyplot.xticks(range(1, len(matrix)+1), xticks, size='x-small', \
        rotation=xticks_rotation)
    pyplot.grid(True)  
    if title != None:
        pyplot.title(title)
    pyplot.gcf().subplots_adjust(bottom=0.15)    
    if (filename != None):
        pyplot.savefig(filename + '.png', format='png', dpi=dpi)
    else:
        pyplot.show()
    pyplot.cla()
    pyplot.close()


def plot_histogram(data, labelx, labely, nbins = 100, color = 'blue', \
        xlimits=None, ylimits=None, title=None, dpi=100, filename=None):
    pyplot.hist(data, nbins, color=color)            
    pyplot.xlabel(labelx, fontsize = 20)
    pyplot.ylabel(labely, fontsize = 20)
    if ylimits != None:
        pyplot.ylim(ylimits)
    if xlimits != None:
        pyplot.xlim(xlimits)
    if title != None:
        pyplot.title(title)
    if (filename != None):
        pyplot.savefig(filename + '.png', format='png', dpi=dpi)
    else:
        pyplot.show()
    pyplot.cla()
    pyplot.close()
    
    
def plot_multiple_histogram(data_matrix, labelx, labely, data_labels, \
        bins, xlimits=none, ylimits=None, colors=None, alpha=None, \
        dpi=100, filename=None):
    pass 

  
def main():
    # Multiple scatter plots 
    x = [range(1,4), range(5, 10)]        
    y = [[2*xx for xx in x[0]], [xx for xx in x[1]]]
    labels = ['2x', 'x']
    plot_scatterplot_series(x, y, labels)
          
            
if __name__ == '__main__':
    main()
        
        
