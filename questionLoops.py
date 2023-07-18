from helper import add_quotation_mark


def create_questionloops(trip, loop_dict):
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