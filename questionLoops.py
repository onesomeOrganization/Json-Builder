from helper import find_nodes_before, add_quotation_mark


def create_questionloops(trip, loop_chain_array, loop_dict):
    
    # PROGRESS
    exit_nodes = get_loop_exit_nodes(loop_chain_array, trip, loop_dict)
    create_progress_for_question_loop_screen(loop_chain_array, trip, exit_nodes)

    # JSON ERSTELLEN
    questionLoops = []   
    for count, key in enumerate(loop_dict):
        questionLoops.append(QuestionLoop(trip, key, count, loop_dict[key]))

    # JSON EINFÜGEN
    # add qloop am ende jeder etappe
    for q in trip.all_questions_array:
        if 'Neue Etappe' in q.structure:
            q.questionLoops = ''
            for loop in questionLoops:
                if q.etappe == str(int(loop.etappe)+1):
                    q.questionLoops += loop.json # TODO funkts nicht
            q.questionLoops = q.questionLoops[:-1]

    questionLoops_json = ''
    for loop in questionLoops:
        if loop.etappe == str(trip.etappen_count):
            questionLoops_json += loop.json
    return questionLoops_json[:-1]
        
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

def create_progress_for_question_loop_screen(loop_chain_array, trip, exit_nodes):
    for chain in loop_chain_array:
        # Startprogress definement
        first_id = chain[0]
        for q in trip.all_questions_array:
            if q.excel_id == first_id:
                start_progress = q.progress
        befores = find_nodes_before(trip.graph, first_id) # if it is not the first chain, then there might be a screen before it which already has a progress
        if len(befores) == 0 or first_id == trip.all_questions_array[0].excel_id or first_id in trip.etappen_start_screens:
            if start_progress is None: # or first id is the first id of the entire array you start from 0
                raise Exception('Fall ist eingetreten, wo first_id noch nicht vergeben ist, aber erster screen')
        else:
            for bef in befores:
                if bef in chain:
                    befores.remove(bef)
            possible_start_progess = []
            for q in trip.all_questions_array:
                if q.excel_id in befores:
                    possible_start_progess.append(q.progress)
            start_progress = max(possible_start_progess)

        # End progress definement
        end_progress = exit_nodes[first_id][3]
        index = exit_nodes[first_id][1]

        step = round((end_progress-1)/(index+1))
        min_step = 5

        for i, node in enumerate(chain):
            for q in trip.all_questions_array:
                if q.excel_id == node and q.progress is None:
                    if i <= index:
                        q.progress = start_progress + (step*(i+1))
                    else:
                        q.progress = start_progress + (step*index) + min_step*(i+1-index)
        
                    
        
    
class QuestionLoop:
    def __init__(self, trip, start_node, count, loop_arrays) -> None:
        self.trip = trip
        self.graph = trip.graph
        self.start_node = start_node
        self.etappe = self.start_node.split('.')[0]
        self.count = count
        self.id = self.trip.id + '-' + self.etappe + '-q' + str(self.count) # selber hochzählen
        self.firstQuestionId = self.trip.id + '-' + self.etappe + '-' + self.start_node.split('.')[1]
        self.refQuestionId = self.firstQuestionId
        self.type = 'REF_ANSWER_OPTION_INTERRUPTIBLE'
        self.loop_nodes = set()
        for loop in loop_arrays:
            # check for nestes array
            if isinstance(loop, list) and all(isinstance(sublist, list) for sublist in loop):
                for inner_loop in loop:
                    for node in inner_loop:
                        self.loop_nodes.add(node)
            else:
                for node in loop:
                    self.loop_nodes.add(node)

        self.add_qids_at_nodes()
        self.json = self.create_json()

    def add_qids_at_nodes(self):
        for q in self.trip.all_questions_array:
            if q.excel_id in self.loop_nodes:
                q.questionLoopId = add_quotation_mark(self.id)


    def create_json(self):
        json = '''
        {
          "id": "%s",
          "type": "%s",
          "refAdaptionType": null,
          "refAdaptionNumber": null,
          "counter": null,
          "refOrderType": null,
          "refOrderColumn": null,
          "refOffset": null,
          "refLimit": null,
          "firstQuestionId": "%s",
          "lastQuestionId": null,
          "refQuestionId": "%s",
          "questionRefLogicId": null,
          "cycles": []
        },'''%(self.id, self.type, self.firstQuestionId, self.refQuestionId)
        return json