class Area:
    
    def __init__(self, nodes, objects, connections, player):
        self.nodes = nodes.split(',')
        self.objects = objects.split(',')
        self.connections = connections.split(',')
        self.players = [player]

