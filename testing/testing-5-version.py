#!/usr/bin/python

import pytricia
import python3_reading_file_to_dict 
import sys
import pprint
import csv
import p_trie
import excluding_ip
import excluding_port
import add_all_rules_after_excluding
import ipaddress
import copy
from operator import itemgetter


final_device_values = []
se_number = 20 
#rap = 100

with open("new_table99", "w"):
	pass

#f_new=open("new_table99","w+")
#f_new.close()


def creating_dict():
	device_values = python3_reading_file_to_dict.csv_dict_list(sys.argv[1])  # Calls the csv_dict_list function, passing the named csv
	device_values = sorted(device_values, key=itemgetter('priority'))
#	device_values = sorted(device_values, key=itemgetter('priority'))
	pprint.pprint(device_values)     # Prints the results nice and pretty like
	return device_values

# Finding list of all parents
def find_all_parents(pyt,ip):
	parent_all = []
	ip = pyt.parent(ip)
	while ip != None :
		parent_all.append(ip)
		ip = pyt.parent(ip)
	return parent_all

def check_tcp_udp(flow_rule):			# checking whether tcp or udp
	if(flow_rule["nw_proto"]=="6"):
		return "True"
	else :
		return "False"

def JUST(gate):
	print(gate)
	return "Hiiii"


def add_rule_to_newft(flow_rule):		#Adding rule to flow
	with open("new_table99", "a") as myfile:
		myfile.write(str(flow_rule))

def finding_patricia_empty(pyt):		#Checking whether patricia tree is empty or not
	if(len(pyt)==0):
		return True
	else :
		return False

def check_and_delete_in_final_device_values(flow_rule):
#	final_device_values
	for x in final_device_values:
		if x['aasno'] == flow_rule['aasno']:
#			print(flow_rule['aasno'],"Removed")
			final_device_values.remove(flow_rule)
			break
		else:
			continue	


def add_rule_to_patricia(pyt_src,pyt_dst,flow_rule):
	temp = []
	isthere = 0
#	print(final_device_values[-1])
	if len(final_device_values) == 0:
#		print(isthere,"Not addng length 0000")
		final_device_values.append(flow_rule)
	else:
		for x in final_device_values:
			if x['aasno'] == flow_rule['aasno']:
				isthere = 1
#				print(isthere,"Not addng")
				break
		if isthere != 1:
#			print(isthere,"--- addng")
			final_device_values.append(flow_rule)
			isthere = 0
			

	if pyt_src.has_key(flow_rule['src_ip']):
		temp = pyt_src.get(flow_rule['src_ip'])
		if int(flow_rule['aasno']) not in temp:
			temp.append(int(flow_rule['aasno']))
			pyt_src.insert(flow_rule['src_ip'],temp)
	else :
		pyt_src.insert(flow_rule['src_ip'],[int(flow_rule['aasno'])])
	temp1 = []
	if pyt_dst.has_key(flow_rule['dst_ip']):
		temp1 = pyt_dst.get(flow_rule['dst_ip'])
		if int(flow_rule['aasno']) not in temp1:
			temp1.append(int(flow_rule['aasno']))
			pyt_dst.insert(flow_rule['dst_ip'],temp1)
	else:
		pyt_dst.insert(flow_rule['dst_ip'],[int(flow_rule['aasno'])])
	return None

def check_exact_proceed(Ips,Ipd,prio,pyt_src,pyt_dst):
	temp = []
	if pyt_src.has_key(Ips):
		temp = pyt_src.get(Ips)
		temp.append(prio)
		pyt_src.insert(Ips,temp)
	else:
		pyt_src.insert(Ips,[prio])
# For Destination insertion
	temp = []
	if pyt_dst.has_key(Ipd):
		temp = pyt_dst.get(Ipd)
		temp.append(prio)
		pyt_dst.insert(Ipd,temp)
	else:
		pyt_dst.insert(Ipd,[prio])
#       print "Inserted  ---"+str(prio)



def subset_for_port(src_a_start, src_a_end, dst_a_start, dst_a_end, src_b_start, src_b_end, dst_b_start, dst_b_end):
	src_a = list(range(int(src_a_start), int(src_a_end)))
	dst_a = list(range(int(dst_a_start), int(dst_a_end)))
	src_b = list(range(int(src_b_start),int(src_b_end)))
	dst_b = list(range(int(dst_b_start), int(dst_b_end)))
	src_inter = list(set(src_a) & set(src_b))
	dst_inter = list(set(dst_a) & set(dst_b))
#	print(len(dst_b),type(dst_b),dst_b_end,dst_b_start)
#       print "subset for port"
	if ((int(src_a_start) == int(src_b_start)) and (int(src_a_end) == int(src_b_end))) and ((int(dst_a_start) == int(dst_b_start)) and (int(dst_a_end) == int(dst_b_end))):
		var2 = "exact"
	elif ((int(src_a_start) >= int(src_b_start) and int(src_a_end) <= int(src_b_end)) and (int(dst_a_start) >= int(dst_b_start) and int(dst_a_end) <= int(dst_b_end))):
		var2 = "equal"
	elif ((int(src_a_start) <= int(src_b_start) and int(src_a_end) >= int(src_b_end)) and (int(dst_a_start) <= int(dst_b_start) and int(dst_a_end) >= int(dst_b_end))):
		var2 = "reverse"
	elif src_inter and dst_inter:
		var2 = "intersect"
	else :
		var2 = "completely"
	src_port_intersection_part = src_inter
	dst_port_intersection_part = dst_inter
	print(len(src_port_intersection_part),len(dst_port_intersection_part))
	return var2,src_port_intersection_part,dst_port_intersection_part

def subset_for_ip(pyt_src, pyt_dst, gamma, mydict ,src_same_conflict_rules,src_child_conflict_rules,src_paren_conflict_rules,dst_same_conflict_rules,dst_child_conflict_rules,dst_paren_conflict_rules):
	'''print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
	print src_same_conflict_rules
	print src_child_conflict_rules
	print src_paren_conflict_rules
	print dst_same_conflict_rules
	print dst_child_conflict_rules
	print dst_paren_conflict_rules
	print mydict['aasno']	
	print (mydict['aasno'] in src_paren_conflict_rules)
	print (mydict['aasno'] in src_same_conflict_rules)
	print type(src_paren_conflict_rules)
	print type(mydict['aasno'])
	print "@@@@@@@@@@@@@@"
	'''
	compare = int(gamma['aasno'])
	if (compare in src_same_conflict_rules) and (compare in dst_same_conflict_rules):
		var1 = "exact"
		src_intersection_part = mydict['src_ip']
		dst_intersection_part = mydict['dst_ip']
	elif (((compare in src_paren_conflict_rules) or (compare in src_same_conflict_rules)) and ((compare in dst_paren_conflict_rules) or (compare in dst_same_conflict_rules))):
		var1 = "equal"
		src_intersection_part = mydict['src_ip']
		dst_intersection_part = mydict['dst_ip']
	elif (((compare in src_child_conflict_rules) or (compare in src_same_conflict_rules)) and ((compare in dst_child_conflict_rules) or (compare in dst_same_conflict_rules))):
		var1 = "reverse"
		src_intersection_part = gamma['src_ip']
		dst_intersection_part = gamma['dst_ip']
	elif ((compare in src_child_conflict_rules) and (compare in dst_paren_conflict_rules)):
		var1 = "intersect"
		src_intersection_part = gamma['src_ip']
		dst_intersection_part = mydict['dst_ip']
	elif ((compare in src_paren_conflict_rules) and (compare in dst_child_conflict_rules)):
		var1 = "intersect"
		src_intersection_part = mydict['src_ip']
		dst_intersection_part = gamma['dst_ip']
# Swapping r gamma
#	temp = mydict
#	mydict = gamma
#	gamma = temp
	print(mydict['aasno'],"--",gamma['aasno'],"--",mydict['src_start'], mydict['src_end'], mydict['dst_start'], mydict['dst_end'], gamma['src_start'], gamma['src_end'], gamma['dst_start'], gamma['dst_end'])
# Now calling subset_for port
	var2,src_port_intersection_part,dst_port_intersection_part = subset_for_port(mydict['src_start'], mydict['src_end'], mydict['dst_start'], mydict['dst_end'], gamma['src_start'], gamma['src_end'], gamma['dst_start'], gamma['dst_end'])
# Comparing port and Ip
#return var1, var2
	print(var1, var2)
#	print "End --------------------of subset"
	if var1 == "exact" and var2 == "exact":
		final = "exact"
	elif var1 == "equal" and var2 == "equal":
		final = var1
	elif var1 == "reverse" and var2 == "reverse":
		final = var1
	elif var1 == "reverse" and var2 == "exact":
		final = "reverse"
	elif var1 == "exact" and var2 == "reverse":
		final = "reverse"
	elif var1 == "reverse" and var2 == "equal":
		final = "intersect"
	elif var1 == "equal" and var2 == "reverse":
		final = "intersect"
	elif var1 == "equal" and var2 == "exact":
		final = "equal"
	elif var1 == "exact" and var2 == "equal":
		final = "equal"
	elif var1 == "intersect" or var2 == "intersect":
		final = "intersect"
	elif var2 == "completely":
		final = "different"
	else :
		final = "intersect"
	return final,src_intersection_part,dst_intersection_part,src_port_intersection_part,dst_port_intersection_part

def check_rule_for_similars(pyt_src,pyt_dst,mydict):
#       print "check_similar started"
	src_conflict_rules = []
	dst_conflict_rules = []
	src_same_conflict_rules = []
	dst_same_conflict_rules = []
	if pyt_src.has_key(mydict['src_ip']):
		src_same_conflict_rules = src_same_conflict_rules + pyt_src.get(mydict['src_ip'])
	if pyt_dst.has_key(mydict['dst_ip']):
		dst_same_conflict_rules = dst_same_conflict_rules + pyt_dst.get(mydict['dst_ip'])
#		print "Inside destination"
#		print src_same_conflict_rules, dst_same_conflict_rules	
#	Adding trule to patricia
	add_rule_to_patricia(pyt_src, pyt_dst, mydict)
#	print len(pyt_src), len(pyt_dst)        
	src_child = pyt_src.children(mydict["src_ip"])
	src_paren = find_all_parents(pyt_src, mydict['src_ip'])
	dst_child = pyt_dst.children(mydict['dst_ip'])
	dst_paren = find_all_parents(pyt_dst, mydict['dst_ip'])
	src_child_conflict_rules = []
	dst_child_conflict_rules = []
	src_paren_conflict_rules = []
	dst_paren_conflict_rules = []
	if src_child != None :
		for i in src_child:
			src_child_conflict_rules = src_child_conflict_rules + pyt_src.get(i)
	if dst_child != None :
		for i in dst_child:
			dst_child_conflict_rules = dst_child_conflict_rules + pyt_dst.get(i)
	if src_paren != None :
		for i in src_paren:
			src_paren_conflict_rules = src_paren_conflict_rules + pyt_src.get(i)
	if dst_paren != None :
		for i in dst_paren:
			dst_paren_conflict_rules = dst_paren_conflict_rules + pyt_dst.get(i)

	src_all = src_child + src_paren
	dst_all = dst_child + dst_paren
#	print "---------------"
#	print src_child, src_paren, dst_child, dst_paren
#	print "---------"
	if src_all != None :
		for i in src_all:
			src_conflict_rules = src_conflict_rules + pyt_src.get(i)
	if dst_all != None :
		for i in dst_all:
			dst_conflict_rules = dst_conflict_rules + pyt_dst.get(i)
	src_conflict_rules = src_conflict_rules + src_same_conflict_rules
	dst_conflict_rules = dst_conflict_rules + dst_same_conflict_rules
	final_conflict_rules = list(set(src_conflict_rules) & set(dst_conflict_rules))
#	print src_conflict_rules, dst_conflict_rules
#       print final_conflict_rules
#       print "check_similar finished"
#	Deleting flows added just to check
	delete_rule_from_pt_ft(pyt_src, pyt_dst, mydict)
#	pyt_src.delete(mydict['src_ip'])
#	pyt_dst.delete(mydict['dst_ip'])
	return final_conflict_rules,src_same_conflict_rules,src_child_conflict_rules,src_paren_conflict_rules,dst_same_conflict_rules,dst_child_conflict_rules,dst_paren_conflict_rules


def check_layer2_layer4(a):
	if (a['src_ip'],a['dst_ip']) == ('0.0.0.0/0','0.0.0.0/0'):	
		if (a['src_mac'],a['dst_mac'],a['src_start'],a['dst_end']) != ('00:00:00:00:00:00','00:00:00:00:00:00','0','0'):
			return True
		else:
			return False
	else :
		return False


def detection_algorithm(gamma,mydict,pyt_src,pyt_dst,src_same_conflict_rules,src_child_conflict_rules,src_paren_conflict_rules,dst_same_conflict_rules,dst_child_conflict_rules,dst_paren_conflict_rules,rap):

	final,src_intersection_part,dst_intersection_part,src_port_intersection_part,dst_port_intersection_part = subset_for_ip(pyt_src, pyt_dst, gamma, mydict,src_same_conflict_rules,src_child_conflict_rules,src_paren_conflict_rules,dst_same_conflict_rules,dst_child_conflict_rules,dst_paren_conflict_rules)

#	print(final,src_intersection_part,dst_intersection_part,src_port_intersection_part,dst_port_intersection_part,"\n")
	print(final,src_intersection_part,dst_intersection_part,"\n")	

	if((check_tcp_udp(mydict) != check_tcp_udp(gamma)) or (final == "different")):
		add_rule_to_patricia(pyt_src,pyt_dst,mydict)
		add_rule_to_newft(mydict)
		print("Just added")
	elif(final == "exact"):
		if(mydict["action "]==gamma["action "]):
			print("Conflict is Redundancy : Sent to resolving")
			rap = conflict_resolver(pyt_src, pyt_dst, mydict,gamma,"redundancy",rap)
		else:
			if(mydict["priority"]==gamma["priority"]):
				print("Conflict is Correlation_prompt : Sent to resolving")
				rap = conflict_resolver(pyt_src, pyt_dst, mydict,gamma,"correlation_prompt",rap,src_intersection_part,dst_intersection_part,src_port_intersection_part,dst_port_intersection_part)
			else:
				print("Conflict is Shadowing : Sent to resolving")
				rap = conflict_resolver(pyt_src, pyt_dst, mydict,gamma,"shadowing",rap)
	elif(final == "equal"): #do subset here
		if(mydict["action "]==gamma["action "]):
			print("Conflict is Redundancy : Sent to resolving")
			rap = conflict_resolver(pyt_src, pyt_dst, mydict,gamma,"redundancy",rap)
		else:
			if(mydict["priority"]==gamma["priority"]):
				print("Conflict is Correlation_prompt : Sent to resolving")
				rap = conflict_resolver(pyt_src, pyt_dst, mydict,gamma,"correlation_prompt",rap,src_intersection_part,dst_intersection_part,src_port_intersection_part,dst_port_intersection_part)
			else:
				print("Conflict is Generalization : Sent to resolving")
				rap = conflict_resolver(pyt_src, pyt_dst, mydict,gamma,"generalization",rap,src_intersection_part,dst_intersection_part,src_port_intersection_part,dst_port_intersection_part)
#				print("Conflict is Generalization : Sent to resolving")
#				conflict_resolver(pyt_src, pyt_dst, mydict,gamma,"generalization",src_intersection_part,dst_intersection_part,src_port_intersection_part,dst_port_intersection_part)
	elif(final == "reverse"): #do subset here
		if(mydict["action "]==gamma["action "]):
			print("Conflict is Redundancy_gamma_Removing : Sent to resolving")
			rap = conflict_resolver(pyt_src, pyt_dst, mydict,gamma,"redundancy_gamma_removing",rap)
		else:
			if(mydict["priority"]==gamma["priority"]):
				print("Conflict is Correlation_prompt : Sent to resolving")
				rap = conflict_resolver(pyt_src, pyt_dst, mydict,gamma,"correlation_prompt",rap,src_intersection_part,dst_intersection_part,src_port_intersection_part,dst_port_intersection_part)
			else:
				print("Conflict is Shadowing : Sent to resolving")
				rap = conflict_resolver(pyt_src, pyt_dst, mydict,gamma,"shadowing",rap,src_intersection_part,dst_intersection_part,src_port_intersection_part,dst_port_intersection_part)
	elif(final == "intersect"):
		if(mydict["action "]==gamma["action "]):
			print("Conflict is Overlap : Sent to resolving")
			rap = conflict_resolver(pyt_src, pyt_dst, mydict,gamma,"overlap",rap,src_intersection_part,dst_intersection_part,src_port_intersection_part,dst_port_intersection_part)
		else:
			if(mydict["priority"]==gamma["priority"]):
				print("Conflict is Correlation_prompt : Sent to resolving")
				rap = conflict_resolver(pyt_src, pyt_dst, mydict,gamma,"correlation_prompt",rap,src_intersection_part,dst_intersection_part,src_port_intersection_part,dst_port_intersection_part)
			else:
				print("Conflict is Correlation : Sent to resolving")
				rap = conflict_resolver(pyt_src, pyt_dst, mydict,gamma,"correlation",rap,src_intersection_part,dst_intersection_part,src_port_intersection_part,dst_port_intersection_part)
#	print("\n",len(pyt_src),len(pyt_dst))
	print("----------------------------------------------------------------------------------")
	return rap
'''
def detection_algorithm(gamma,mydict,pyt_src,pyt_dst,src_same_conflict_rules,src_child_conflict_rules,src_paren_conflict_rules,dst_same_conflict_rules,dst_child_conflict_rules,dst_paren_conflict_rules):
print gamma,mydict,"\t"
rock = subset_for_ip(pyt_src, pyt_dst, gamma,mydict,src_same_conflict_rules,src_child_conflict_rules,src_paren_conflict_rules,dst_same_conflict_rules,dst_child_conflict_rules,dst_paren_conflict_rules)
print rock
'''

def delete_rule_from_pt_ft(pyt_src, pyt_dst, gamma):
	check_and_delete_in_final_device_values(gamma)
	temp = []
	Ips = gamma['src_ip']
	prio = int(gamma['aasno'])
#	print prio
	temp = pyt_src.get(Ips)
#	print(temp,type(temp))
	if temp is not None:
		if (prio not in temp):
			return None
		else:
			if len(temp) > 1 :
				temp.remove(prio)
				pyt_src.insert(Ips,temp)
			else:
				pyt_src.delete(Ips)
# For Destination insertion
	temp = []
	Ipd = gamma['dst_ip']
	temp = pyt_dst.get(Ipd)
#	print len(temp),"Length of temp"
	if temp is not None:
		if (prio not in temp):
			return None
		else:
			if len(temp) > 1 :
				temp.remove(prio)
				pyt_dst.insert(Ipd,temp)
			else:
				pyt_dst.delete(Ipd)
# deleting a flow fro flow table
	bad_words = ["'aasno': '"+str(prio)+"',"]

	with open('new_table99') as oldfile, open('new_table22', 'w') as newfile:
		for line in oldfile:
			if not any(bad_word in line for bad_word in bad_words):
				newfile.write(line)

	with open('new_table99', 'w+') as output, open('new_table22', 'r') as input1:
		while True:
			data = input1.read(100000)
			if data == '': # end of file reached
				break
			output.write(data)


def conflict_resolver(pyt_src, pyt_dst, mydict, gamma, conflict_type,rap,src_intersection_part = None,dst_intersection_part = None,src_port_intersection_part = None,dst_port_intersection_part = None):
	if(conflict_type=="shadowing"):
		delete_rule_from_pt_ft(pyt_src, pyt_dst, gamma)
		rap = 200
		print("Hold R")
	elif(conflict_type=="redundancy_gamma_removing"):
		delete_rule_from_pt_ft(pyt_src, pyt_dst, gamma)
		add_rule_to_patricia(pyt_src, pyt_dst, mydict)
		add_rule_to_newft(mydict)
		print("REDUNDANCY GAMMA REMOVED AND R ADDED")
	elif(conflict_type == "redundancy"):
		print("No adding of R")
	elif(conflict_type=="generalization"):
		'''a=input('generalization conflict. Choose one flow rule : ')
		if(a=="gamma"):
			print("No need to add rule")
		else :
			delete_rule_from_pt_ft(pyt_src, pyt_dst, gamma)
			add_rule_to_patricia(pyt_src, pyt_dst, mydict)
			add_rule_to_newft(mydict)
		print("Resolved Generalization:")'''
#		delete_rule_from_pt_ft(pyt_src, pyt_dst, mydict)
		print(src_intersection_part,dst_intersection_part)
		rap = 200
		src_ip_list=excluding_ip.func_exclude_ip(gamma["src_ip"],src_intersection_part)
		dst_ip_list=excluding_ip.func_exclude_ip(gamma["dst_ip"],dst_intersection_part)
		src_port_list=excluding_port.func_exclude_port(list(range(int(gamma["src_start"]),int(gamma["src_end"]))),src_port_intersection_part)
		dst_port_list=excluding_port.func_exclude_port(list(range(int(gamma["dst_start"]),int(gamma["dst_end"]))),dst_port_intersection_part)
		f_list = add_all_rules_after_excluding.add_all_rules(src_ip_list, dst_ip_list, src_port_list, dst_port_list, mydict, gamma, pyt_src, pyt_dst)
		for x in f_list:
			add_rule_to_patricia(pyt_src, pyt_dst, x)
			add_rule_to_newft(x)
		delete_rule_from_pt_ft(pyt_src, pyt_dst, gamma)
	elif(conflict_type=="overlap"):
		''''a=input('Overlap conflict. Choose one flow rule : ')
		if(a=="gamma"):
			print("No need to add rule")
		else :
			delete_rule_from_pt_ft(pyt_src, pyt_dst, gamma)
			add_rule_to_patricia(pyt_src, pyt_dst, mydict)
			add_rule_to_newft(mydict)
		print("Resolved Overlap:")
# 		print "Do union here"  #union operation'''
#		delete_rule_from_pt_ft(pyt_src, pyt_dst, mydict)
		rap = 200
		src_ip_list=excluding_ip.func_exclude_ip(gamma["src_ip"],src_intersection_part)
		dst_ip_list=excluding_ip.func_exclude_ip(gamma["dst_ip"],dst_intersection_part)
		src_port_list=excluding_port.func_exclude_port(list(range(int(gamma["src_start"]),int(gamma["src_end"]))),src_port_intersection_part)
		dst_port_list=excluding_port.func_exclude_port(list(range(int(gamma["dst_start"]),int(gamma["dst_end"]))),dst_port_intersection_part)
		f_list = add_all_rules_after_excluding.add_all_rules(src_ip_list, dst_ip_list, src_port_list, dst_port_list, mydict, gamma, pyt_src, pyt_dst)
		for x in f_list:
			add_rule_to_patricia(pyt_src, pyt_dst, x)
			add_rule_to_newft(x)
#			print(x['aasno'])
#		print("ADDng FNSHED",gamma['aasno'])
		delete_rule_from_pt_ft(pyt_src, pyt_dst, gamma)
	elif(conflict_type=="correlation_prompt"):
		'''a=input('Correlation conflict. Choose one flow rule : ')
		if(a=="gamma"):
			print("No need to add rule")
		else :
			delete_rule_from_pt_ft(pyt_src, pyt_dst, gamma)
			add_rule_to_patricia(pyt_src, pyt_dst, mydict)
			add_rule_to_newft(mydict)		'''
#		delete_rule_from_pt_ft(pyt_src, pyt_dst, mydict)
		rap = 200
		src_ip_list=excluding_ip.func_exclude_ip(gamma["src_ip"],src_intersection_part)
		dst_ip_list=excluding_ip.func_exclude_ip(gamma["dst_ip"],dst_intersection_part)
		src_port_list=excluding_port.func_exclude_port(list(range(int(gamma["src_start"]),int(gamma["src_end"]))),src_port_intersection_part)
		dst_port_list=excluding_port.func_exclude_port(list(range(int(gamma["dst_start"]),int(gamma["dst_end"]))),dst_port_intersection_part)
		f_list = add_all_rules_after_excluding.add_all_rules(src_ip_list, dst_ip_list, src_port_list, dst_port_list, mydict, gamma, pyt_src, pyt_dst)
		for x in f_list:
#			print(x)
			add_rule_to_patricia(pyt_src, pyt_dst, x)
			add_rule_to_newft(x)
#			print(x['aasno'])
#		print("ADDng FNSHED",gamma['aasno'])
		delete_rule_from_pt_ft(pyt_src, pyt_dst, gamma)
		print("Resolved correlation:")	
	elif(conflict_type=="correlation"):
#		delete_rule_from_pt_ft(pyt_src, pyt_dst, mydict)
		rap = 200
		src_ip_list=excluding_ip.func_exclude_ip(gamma["src_ip"],src_intersection_part)
		dst_ip_list=excluding_ip.func_exclude_ip(gamma["dst_ip"],dst_intersection_part)
		src_port_list=excluding_port.func_exclude_port(list(range(int(gamma["src_start"]),int(gamma["src_end"]))),src_port_intersection_part)
		dst_port_list=excluding_port.func_exclude_port(list(range(int(gamma["dst_start"]),int(gamma["dst_end"]))),dst_port_intersection_part)
		f_list = add_all_rules_after_excluding.add_all_rules(src_ip_list, dst_ip_list, src_port_list, dst_port_list, mydict, gamma, pyt_src, pyt_dst)	
		for x in f_list:
			add_rule_to_patricia(pyt_src, pyt_dst, x)
			add_rule_to_newft(x)
		delete_rule_from_pt_ft(pyt_src, pyt_dst, gamma)
	'''elif(conflict_type=="imbrication"):
		a=input('Cross layer conflict. Choose one flow rule : ')
		if(a=="gamma"):
			print("No need to add rule")
		else :
			add_rule_to_patricia(pyt_src, pyt_dst, mydict)
			add_rule_to_newft(mydict)
		print("Resolved Imbrication:")'''
	return rap

#def Reconcile(pyt_src, pyt_dst, device_values, mydict):
#	for gamma in final_device_values:
#		if(mydict["nw_proto"]==gamma["nw_proto"]):
#			var2 = subset_for_port(mydict['src_start'], mydict['src_end'], mydict['dst_start'], mydict['dst_end'], gamma['src_start'], gamma['src_end'], gamma['dst_start'], gamma['dst_end'])
#			print(var2, "subset reurn value")
#		if(var2 != "intersection"):
#			print("Conflict is Imbrication : Sent to resolving")
#			conflict_resolver(pyt_src, pyt_dst, mydict,gamma,"imbrication")
#	print("\n")
#	return True
#def get_by_aasno(vals, expId): return next((x for x in vals if x['aasno'] == expId),None)

def detection(device_values,pyt_src,pyt_dst):
	print("Hello detection starts from here")
	for mydict in device_values :
		if check_layer2_layer4(mydict) == True :
			print(("\n\nReconcile %s" %mydict['aasno']))
#			Reconcile(pyt_src, pyt_dst, device_values, mydict)
		else :
			print(("\n\nNO Reconc %s" %mydict['aasno']))
			conflict_rule_numbers,src_same_conflict_rules,src_child_conflict_rules,src_paren_conflict_rules,dst_same_conflict_rules,dst_child_conflict_rules,dst_paren_conflict_rules = check_rule_for_similars(pyt_src,pyt_dst,mydict)     #Gives list of conflict ru
			print(conflict_rule_numbers,src_same_conflict_rules,src_child_conflict_rules,src_paren_conflict_rules,dst_same_conflict_rules,dst_child_conflict_rules,dst_paren_conflict_rules,"Conflicted_numbers")
			if len(conflict_rule_numbers) == 0 :
				add_rule_to_patricia(pyt_src,pyt_dst,mydict)
				add_rule_to_newft(mydict)
			else :
				fd = final_device_values
				rap = 100
				for i in conflict_rule_numbers:
					it = str(i)
					print(it)
#					print(fd)
					my_item = 100 
					for item in fd:
						if item['aasno'] == it:
							my_item = item
							break
					if my_item != 100:
						gamma = my_item
#					gamma = next((item for item in final_device_values if item['aasno'] == it),None)
#					if gamma == None:
#					gamma = item
#						continue	
#					detection_algorithm(gamma, mydict, pyt_src, pyt_dst,src_same_conflict_rules,src_child_conflict_rules,src_paren_conflict_rules,dst_same_conflict_rules,dst_child_conflict_rules,dst_paren_conflict_rules)
#					else:
						print(gamma)
						rap1 = detection_algorithm(gamma, mydict, pyt_src, pyt_dst,src_same_conflict_rules,src_child_conflict_rules,src_paren_conflict_rules,dst_same_conflict_rules,dst_child_conflict_rules,dst_paren_conflict_rules,rap)
					else:
						pass
#				print(":::::::::::::",rap1)
				if rap1 == 200:
#					print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
					add_rule_to_patricia(pyt_src,pyt_dst,mydict)
					add_rule_to_newft(mydict)
	print("DETECTION COMPLETE:")


if __name__ == "__main__" :
	device_values = creating_dict()
	pyt_src,pyt_dst = p_trie.patricia()
	detection(device_values,pyt_src,pyt_dst)
	pprint.pprint(final_device_values)
	print(len(final_device_values))

