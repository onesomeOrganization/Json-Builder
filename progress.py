import numpy as np
from helper import find_nodes_before, get_one_excel_id_higher, create_ref_value_condition_dict, create_ref_count_condition_dict, create_ref_option_condition_dict, create_value_condition_dict
import math
import re

def create_adjazenzliste(questions_array):
    adjazenzliste = {}
    for num, q in enumerate(questions_array):
        # add id as key
        if not 'Neue Etappe' in q.structure: # check for neue etappe and skip entry
            adjazenzliste[q.excel_id] = []
        arrow_or_condition_flag = False
        ref_value_pattern = r'(\d+\.\d+)\s*\(\s*wenn\s+(\w+)\s*([><=]=?)\s*(\d+\.\d+)\)'
        ref_count_pattern = r'(\d+\.\d+)\s*\(wenn\s*(\d+\.\d+)\s*([=><]=?|!=)\s*(\d+)\s*(Antwort(en)?|antwort(en)?)\)'
        ref_option_pattern = r'(\d+\.\d+)\s*\(wenn\s+(\d+\.\d+)\s*=\s*([^\d+\.\d+]*)\)'
        value_pattern = r'(\d+\.\d+)\s*\((.*?)\)'
        for i, text in enumerate(q.texts):
            if ('(wenn' in text or '( wenn' in text) and q.structure[i] == 'weiter mit Screen' :
                arrow_or_condition_flag = True
                if re.match(ref_value_pattern, text):
                    condition_dict = create_ref_value_condition_dict(text)
                elif re.match(ref_count_pattern, text):
                    condition_dict = create_ref_count_condition_dict(text)
                elif re.match(ref_option_pattern, text):
                    condition_dict = create_ref_option_condition_dict(text)
                elif re.match(value_pattern, text):
                    condition_dict = create_value_condition_dict(text)
                else:
                    raise Exception ('check adjazenzliste')
                # Retrieve the current value
                current_value = adjazenzliste[q.excel_id]
                for key in condition_dict:
                    # Update the value by appending the new value
                    current_value.append(key)
                # Assign the updated value back to the key
                adjazenzliste[q.excel_id] = current_value
            elif "->" in text and not ('(wenn' in text or '( wenn' in text) and (q.structure[i] == 'ITEM(Multiple)' or q.structure[i] == 'ITEM(Single)' or q.structure[i] == 'weiter mit Screen' or q.structure[i] == 'BUTTON'):
                arrow_or_condition_flag = True
                # add ids after the -> as values
                json_id = text.split('->')[1].strip()
                # Retrieve the current value
                current_value = adjazenzliste[q.excel_id]
                # Update the value by appending the new value
                current_value.append(json_id)
                # Assign the updated value back to the key
                adjazenzliste[q.excel_id] = current_value    
        # normal Case
        if not 'weiter mit Screen' in q.structure and not 'letzter Screen' in q.structure and not num == len(questions_array)-1 and not 'Neue Etappe' in questions_array[num+1].structure and not 'Neue Etappe' in q.structure and not arrow_or_condition_flag:
            # add id+1 as value, e.g. id = flora-v13-1-3 -> flora-v13-1-4
            #adjazenzliste[q.excel_id] = [q.excel_id.split('.')[0]+'.'+str(int(q.excel_id.split('.')[1])+1)]
            adjazenzliste[q.excel_id] = [get_one_excel_id_higher(q.excel_id)]
        # weiter mit Screen case ohne ->
        elif 'weiter mit Screen' in q.structure and not arrow_or_condition_flag:
            # add weiter mit screen id
            json_id = q.texts[np.where(q.structure == 'weiter mit Screen')][0]
            adjazenzliste[q.excel_id] = [json_id]
    return adjazenzliste

def create_progress(trip, questions_array):
    # PREPARATION
    normal_chain_array = []
    loop_chain_array = []
    # put all ids in not done
    not_visited = []
    visited = []
    for q in questions_array:
        if not 'Neue Etappe' in q.structure:
            not_visited.append(q.excel_id)

    find_chains(not_visited, trip.graph, visited, normal_chain_array, loop_chain_array)
    normal_chain_array, loop_dict, loop_chain_array = update_and_clean_chain_arrays(normal_chain_array, trip)

    # PROGRESS
    create_normal_chain_progress(normal_chain_array, questions_array, trip)
    #exit_nodes = get_loop_exit_nodes(loop_chain_array, trip, loop_dict)
    create_progress_for_question_loop_screen(trip, loop_chain_array)
    return loop_dict

def find_chains(not_visited, graph, visited, normal_chain_array, loop_chain_array):
    # done when all progress is done
    if len(not_visited) == 0:
        return
    start_node = not_visited[0]
    # Längste Kette finden
    longest_chain, join_node = find_longest_chain(graph, start_node, visited) 

    # check if chain or loop chain:
    chain_flag = False
    for element in graph[longest_chain[-1]]:
        if element in longest_chain:
            chain_flag = True
            index = longest_chain.index(element)
            longest_chain = longest_chain[index:]
            loop_chain_array.append(longest_chain)
    
    if not chain_flag:
        normal_chain_array.append(longest_chain)

    if len(not_visited) != 0:
        # update progress done and not done
        for id in longest_chain:
            if len(not_visited) == 0:
                return
            if id in not_visited:
                not_visited.remove(id)
            if not id in visited:
                visited.append(id)
        # start again with updated values
        find_chains(not_visited, graph, visited, normal_chain_array, loop_chain_array)

def update_and_clean_chain_arrays(normal_chain_array, trip):
    loop_dict = create_loop_dict(trip)
    loop_chain_array = []
    for value in loop_dict.values():
        # check for nestes array
        if isinstance(value, list) and all(isinstance(sublist, list) for sublist in value):
            for val in value:
                loop_chain_array.append(val)
        else:
            loop_chain_array.append(value)
    
    # Update normal chains with q loop chain parts
    # A) check if normal cain is entirely contained in loop chain
    clean_normal_chain_array = normal_chain_array[:]
    for sub_chain in normal_chain_array:
        for main_chain in loop_chain_array:
            if all(item in main_chain for item in sub_chain):
                if sub_chain in clean_normal_chain_array:
                    clean_normal_chain_array.remove(sub_chain)
    normal_chain_array = clean_normal_chain_array
    # B) enlongate at the beginning
    for i, chain in enumerate(normal_chain_array):
        befores = find_nodes_before(trip.graph, chain[0])
        for bef in befores:
            for loop_chain in loop_chain_array:
                if bef in loop_chain:
                    index_of_bef = loop_chain.index(bef) 
                    if not all(item in normal_chain_array[i] for item in loop_chain[:index_of_bef+1]):
                        normal_chain_array[i] = loop_chain[:index_of_bef+1]+chain
    # C) try to connect the normal chains with qloop chains
    for chain1 in normal_chain_array:
        for chain2 in normal_chain_array:
            if chain2[0] in trip.graph[chain1[-1]]:
                normal_chain_array.remove(chain1)
                normal_chain_array.remove(chain2)
                normal_chain_array.append(chain1+chain2)
            elif chain1[0] in trip.graph[chain2[-1]]:
                normal_chain_array.remove(chain1)
                normal_chain_array.remove(chain2)
                normal_chain_array.append(chain2+chain1)
    return(normal_chain_array, loop_dict, loop_chain_array)

def create_normal_chain_progress(normal_chain_array, questions_array, trip):
    # NORMAL CHAIN PROGRESS
    for chain in normal_chain_array:
        first_id = chain[0]
        befores = find_nodes_before(trip.graph, first_id) # if it is not the first chain, then there might be a screen before it which already has a progress
        if len(befores) == 0 or first_id == questions_array[0].excel_id or first_id in trip.etappen_start_screens: # or first id is the first id of the entire array you start from 0
            start_progress = 0
        else:
            possible_start_progess = []
            for q in questions_array:
                if q.excel_id in befores:
                    if q.progress != None:
                        possible_start_progess.append(q.progress)
            start_progress = min(possible_start_progess)
        # end progress: 90 wenn letzte_id letzer screen oder ende vom question_array oder progress vom node wo sie zusammenführen
        last_id = chain[-1]
        if questions_array[-1].excel_id == last_id or any(last_id in value for value in trip.etappen_end_screens.values()):
            end_progress = 100
        else:
            nexts = trip.graph[last_id]
            if len(nexts) == 0:
                raise Exception ('Check end progress -> there is no next node with a progress already assigned')
            progresses = []
            for n in nexts:
                for q in questions_array:
                    if q.excel_id == n and q.progress != None:
                        progresses.append(q.progress)
            end_progress = min(progresses)-1
        # create the progress
        create_progress_along_chain(chain_to_array(chain, questions_array), start_progress, end_progress)

def get_loop_exit_nodes(loop_chain_array, trip, loop_dict):
    exit_nodes = {}
    # start_id: id_ausgang, index in loop_ausgang, next_id, min progress of next
    for loop in loop_chain_array:
        for node in loop:
            nexts = trip.graph[node] 
            for n in nexts:
                if n not in loop: # only real exit nodes not nodes part of a loop
                    if node in exit_nodes:
                        exit_nodes[loop[0]][2].append(n)
                    else:
                        exit_nodes[loop[0]] = [[node], loop.index(node), [n]] 
    # handle loops which originate from the same startscreen
    for key in loop_dict:
        number_loops = len(loop_dict[key])
        for key2 in exit_nodes:
            if key == key2:
                if number_loops > 1:
                    exit_nodes[key2][2] = delete_infrequent_entries(number_loops, exit_nodes[key2][2])
    
    for value in exit_nodes.values():
        progresses = []
        for exit_node in value[2]:
            for question in trip.all_questions_array:
                if question.excel_id == exit_node:
                    progresses.append(question.progress)
        value.append(min(progresses))
    return exit_nodes


def create_progress_for_question_loop_screen(trip, loop_chain_array):
    for chain in loop_chain_array:
        for node in chain:
            for i, q in enumerate(trip.all_questions_array):
                if q.excel_id == node and q.progress is None:
                    befores = find_nodes_before(trip.graph, node)
                    if len(befores) == 0 or node == trip.all_questions_array[0].excel_id or node in trip.etappen_start_screens:
                        start_progress = 0
                    else:
                        possible_start_progess = []
                        for q in trip.all_questions_array:
                            if q.excel_id in befores:
                                if q.progress != None:
                                    possible_start_progess.append(q.progress)
                        start_progress = max(possible_start_progess)
                    trip.all_questions_array[i].progress = start_progress+5
        

# ------------- HELPER FUNCTIONS --------------------

def delete_infrequent_entries(n, arr):
    # Create a dictionary to count occurrences of each element
    counts = {}
    for elem in arr:
        counts[elem] = counts.get(elem, 0) + 1
    # Filter the array to keep only elements with frequency >= n
    frequent_entries = [elem for elem in arr if counts[elem] >= n]
    # Create a new set to keep track of already processed frequent entries
    processed_entries = set()
    # Remove additional occurrences of frequent entries
    reduced_entries = []
    for elem in frequent_entries:
        if counts[elem] >= n and elem not in processed_entries:
            reduced_entries.append(elem)
            processed_entries.add(elem)

    return reduced_entries

def create_loop_dict(trip):
    loops = [[node]+path  for node in trip.graph for path in find_loops(trip.graph, node, node)]
    # only loops starting with starting node count
    starting_screen_loops = []
    for loop in loops:
        for id in trip.qloop_start_screens_ids:
            if loop[0] == id:
                starting_screen_loops.append(loop)
    loops = starting_screen_loops

    # delete double starting loop
    for loop in loops:
        loop.pop()
    # assign to start_nodes
    loop_dict = {}
    for loop in loops:
        if loop[0] in loop_dict:
            if not loop in loop_dict[loop[0]]:
                loop_dict[loop[0]].append(loop)
        else:
            loop_dict[loop[0]] = [loop]
    return loop_dict

def find_loops(graph, start, end):
    fringe = [(start, [])]
    while fringe:
        state, path = fringe.pop()
        if path and state == end:
            yield path
            continue
        for next_state in graph[state]:
            if next_state in path:
                continue
            fringe.append((next_state, path+[next_state]))


def find_longest_chain(graph, start_node, end_nodes):
    visited = {node: False for node in graph}
    longest_chain = []
    join_node_id = None

    current_chain = []
    join_node_id = dfs(graph, start_node, visited, current_chain, longest_chain, end_nodes, join_node_id)

    return longest_chain, join_node_id

def dfs(graph, node, visited, current_chain, longest_chain, end_nodes, join_node_id):
    visited[node] = True
    current_chain.append(node)

    if node in end_nodes and len(current_chain) > len(longest_chain):
        longest_chain[:] = current_chain
        join_node_id = node
        return join_node_id
    elif len(current_chain) > len(longest_chain) and node not in end_nodes:
        longest_chain[:] = current_chain
        join_node_id = None

    for neighbor in graph[node]:
        if not visited[neighbor] and not neighbor in end_nodes:
            join_node_id = dfs(graph, neighbor, visited, current_chain, longest_chain, end_nodes, join_node_id)
    current_chain.pop()
    visited[node] = False
    return join_node_id


def create_progress_along_chain(chain, start_progress, end_progress):
    # erste progress schon plus progresssteps
    progress_steps = (end_progress-start_progress)/(len(chain))
    progress = start_progress + progress_steps
    for question in chain:
        if question.progress != None:
            print('WARNING: Check progress, chains and function create_progess_along_chain')
            continue
        question.progress =  math.floor(progress)
        progress += progress_steps
        if 'letzter Screen' in question.structure:
            question.progress = 99


def chain_to_array(chain, questions_array):
    chain_array = []
    for chain_id in chain:
        for q in questions_array:
            if q.excel_id == chain_id:
                chain_array.append(q)
    return chain_array