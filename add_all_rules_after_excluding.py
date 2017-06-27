#!/usr/bin/bash
import copy
import final_algo
import pprint
final_algo.se_number = final_algo.se_number + 1
def add_all_rules(src_ip_list, dst_ip_list, src_port_list, dst_port_list, mydict, gamma, pyt_src, pyt_dst):
	count = 0
	q = final_algo.se_number
	great = []
	for sip in src_ip_list:
		for dip in dst_ip_list:
			for sport in src_port_list:
				for dport in dst_port_list:
					cmydict = copy.deepcopy(gamma)
					cmydict['src_ip'] = sip
					cmydict['dst_ip'] = dip
					cmydict['src_start'] = str(sport[0])
					cmydict['src_end'] = str(sport[-1])
					cmydict['dst_start'] = str(dport[0])
					cmydict['dst_end'] = str(dport[-1])
					cmydict['aasno'] = str(final_algo.se_number)
					count = count + 1
					my_copy = copy.deepcopy(cmydict)
					great.append(my_copy)
					final_algo.se_number = final_algo.se_number + 1
#	print("------",count,src_ip_list,dst_ip_list,len(src_port_list),len(src_port_list),"-------""\n")
	return great
