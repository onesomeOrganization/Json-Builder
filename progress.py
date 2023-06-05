import numpy as np

def find_longest_chain(graph, start_node, end_nodes):
    visited = {node: False for node in graph}
    longest_chain = []
    join_node_id = None

    current_chain = []
    join_node_id = dfs(graph, start_node, visited, current_chain, longest_chain, end_nodes, join_node_id)
    #dfs(graph, start_node, visited, current_chain, longest_chain, end_nodes)

    return longest_chain, join_node_id

def dfs(graph, node, visited, current_chain, longest_chain, end_nodes, join_node_id):
    visited[node] = True
    current_chain.append(node)

    if node in end_nodes and len(current_chain) > len(longest_chain):
        join_node_id = node
        return join_node_id
    elif len(current_chain) > len(longest_chain) and node not in end_nodes:
        longest_chain[:] = current_chain
        join_node_id = None

    for neighbor in graph[node]:
        if not visited[neighbor]:
            join_node_id = dfs(graph, neighbor, visited, current_chain, longest_chain, end_nodes, join_node_id)
    current_chain.pop()
    visited[node] = False
    return join_node_id


def create_adjazenzliste(questions_array):
    adjazenzliste = {}
    for num, q in enumerate(questions_array):
        # add id as key
        adjazenzliste[q.id] = []
        arrow_flag = False
        for text in q.texts:
            if "->" in text:
                arrow_flag = True
                # add ids after the -> as values
                json_id = text.split('->')[1].strip()
                # Retrieve the current value
                current_value = adjazenzliste[q.id]
                # Update the value by appending the new value
                current_value.append(json_id)
                # Assign the updated value back to the key
                adjazenzliste[q.id] = current_value
        if not arrow_flag:
            if not 'weiter mit Screen' in q.structure and not 'letzter Screen' in q.structure and not num == len(questions_array)-1:
                # add id+1 as value, e.g. id = flora-v13-1-3 -> flora-v13-1-4
                adjazenzliste[q.id] = [q.id.split('.')[0]+'.'+str(int(q.id.split('.')[1])+1)]
            elif 'weiter mit Screen' in q.structure:
                # add weiter mit screen id
                json_id = q.texts[np.where(q.structure == 'weiter mit Screen')][0]
                adjazenzliste[q.id] = [json_id]
    return adjazenzliste

def create_progress_along_chain(chain, start_progress, end_progress):
    # erste progress schon plus progresssteps
    progress_steps = round((end_progress-start_progress)/(len(chain)+1))
    progress = start_progress + progress_steps
    for question in chain:
        question.progress = progress
        progress += progress_steps
        if 'letzter Screen' in question.structure:
            question.progress = 99


def chain_to_array(chain, questions_array):
    chain_array = []
    for chain_id in chain:
        for q in questions_array:
            if q.id == chain_id:
                chain_array.append(q)
    return chain_array

def find_node_before(graph, node):
    for n, neighbors in graph.items():
        if node in neighbors:
            return n
    return None

def progress_recursive(progress_not_done, graph, progress_done, questions_array):
    # done when all progress is done
    if len(progress_not_done) == 0:
        return
    start_node = progress_not_done[0]
    # Längste Kette finden
    longest_chain, join_node_id = find_longest_chain(graph, start_node, progress_done)
    # longest_chain(start_node, graph, progress_done) -> bis ende oder bis rejoin with already done -> rejoin wiedergeben
    # start_progress: check progress from question before or if question does not exist it is 0
    first_id = longest_chain[0]
    id_before = find_node_before(graph, first_id)
    if id_before == None:
        start_progress = 0
    for q in questions_array:
        if q.id == id_before:
            start_progress = q.progress
    # end progress: 90 wenn letzte_id letzer screen oder ende vom question_array oder progress vom node wo sie zusammenführen
    last_id = longest_chain[-1]
    last_q = next((q for q in questions_array if q.id == last_id), None)
    if join_node_id != None:
        end_progress = next((q.progress for q in questions_array if q.id == join_node_id), None)
    elif 'letzter Screen' in last_q.structure or questions_array[-1].id == last_id:
        end_progress = 100
    # create the progress
    create_progress_along_chain(chain_to_array(longest_chain, questions_array), start_progress, end_progress)
    
    if len(progress_not_done) != 0:
        # update progress done and not done
        for id in longest_chain:
            if len(progress_not_done) == 0:
                return
            progress_not_done.remove(id)
            progress_done.append(id)
        # start again with updated values
        progress_recursive(progress_not_done, graph, progress_done, questions_array)


def create_progress(questions_array):
    graph = create_adjazenzliste(questions_array)
    # put all ids in not done
    progress_not_done = []
    progress_done = []
    for q in questions_array:
        progress_not_done.append(q.id)
    progress_recursive(progress_not_done, graph, progress_done, questions_array)
