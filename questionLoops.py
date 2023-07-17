
def create_questionloops(trip):
    for question in trip.all_questions_array:
        question.questionLoopId = 'null'

    get_questionLoops(trip)

    questionLoops = ''
    return questionLoops

def get_questionLoops(trip):
    etappe = '' # über excel und start screen
    loop_id = '' # selber hochzählen + über etappe
    start_screen = '' # über excel
    #loop_screens = find_loop_nodes(trip.graph)
    

def find_loop(graph, start, visited, recursion_stack, loop_nodes):
    visited[start] = True
    recursion_stack[start] = True

    for neighbor in graph[start]:
        if not visited[neighbor]:
            if find_loop(graph, neighbor, visited, recursion_stack, loop_nodes):
                loop_nodes.add(neighbor)
                return True
        elif recursion_stack[neighbor]:
            loop_nodes.add(neighbor)
            return True

    recursion_stack[start] = False
    return False

def find_loop_nodes(graph):
    vertices = len(graph)
    visited = [False] * vertices
    recursion_stack = [False] * vertices
    loop_nodes = set()

    for vertex in range(vertices):
        if not visited[vertex]:
            find_loop(graph, vertex, visited, recursion_stack, loop_nodes)

    return loop_nodes

