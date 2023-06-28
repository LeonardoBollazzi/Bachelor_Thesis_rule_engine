
# Define the Cluster class
class Cluster:
    def __init__(self):
        self.clusterN = None
        self.paragraphs = []
        self.clusterRule = []
        self.loop = []

    def set_clusterN(self, new_value):
        self.clusterN = new_value


    def get_parentClusterN(self):
        return self.clusterN