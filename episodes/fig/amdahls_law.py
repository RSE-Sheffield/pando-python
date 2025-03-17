"""
Construct a graph demonstrating Amdahl's law

"""
import matplotlib.pyplot as plt

def calc_overall_speedup(acute_proportion, acute_speedup):
  original_time = 1
  unaffected_time = (1-acute_proportion)*original_time
  affected_time = (acute_proportion*original_time)/acute_speedup
  overall_time = unaffected_time + affected_time
  overall_speedup = original_time / overall_time
  return overall_speedup

plt.rcParams['text.usetex'] = True
# How much the acute piece of code is optimised
acute_speedup = [2 ** i for i in range(17)]

# 1 plot for each "proportion" of the runtime taken up by the acute piece of code to be optimised
for proportion in [0.95, 0.9, 0.75, 0.5, 0.01]:
  overall_speedup = [calc_overall_speedup(proportion, i) for i in acute_speedup]
  plt.plot(acute_speedup, overall_speedup, label=f"{proportion*100}%")

plt.xlabel("$S$")
plt.ylabel("$S_{overall}$")
#plt.ticklabel_format(style='plain')
plt.xscale('symlog')
plt.minorticks_off()
plt.xticks(acute_speedup, acute_speedup, rotation=90)
plt.xlim(xmin=1)
plt.yticks([i for i in range(2, 22, 2)], [str(i) for i in range(2, 22, 2)])
plt.ylim(ymin=0)
plt.legend(title = "$P$") 
plt.tight_layout()
plt.savefig('amdahls_law.png')
plt.show()