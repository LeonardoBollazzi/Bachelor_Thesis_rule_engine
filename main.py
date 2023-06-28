import associationAnalysis
import pdfHandler
from paragraphObject import Paragraph
from clusterObject import Cluster
import documentCluster
import silouhetteScore
import xmlHandler
import replaceStringXML
import xmlCategoricalValues
import loopFinder
import outputSaving
import warnings
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)

if __name__ == '__main__':

    # Specify the paths to the XML files
    xml_file_paths = ['XML/VRL2_1.xml', 'XML/VRL2_2.xml', 'XML/VRL2_3.xml']
    #xml_file_paths = ['XML/VRL1_1.xml', 'XML/VRL1_2.xml', 'XML/VRL1_3.xml']

    # Read the XML files
    xml_data_list = xmlHandler.read_xml_files(xml_file_paths)

    # Specify the paths to the XML files
    pdf_files = ["PDF\VRL2_1.pdf","PDF\VRL2_2.pdf", "PDF\VRL2_3.pdf"]
    #pdf_files = ["PDF\VRL1_1.pdf", "PDF\VRL1_2.pdf", "PDF\VRL1_3.pdf"]


    # Create paragraph objects for each found paragraph and assign the corresponding xml data to it
    paragraphObject_list = []
    for i, pdf in enumerate(pdf_files):
        # Get paragraph list of each PDF
        paragraphList, extracted_tables = pdfHandler.pdf_to_text_and_tables(pdf)

        for paragraph in paragraphList:
            # For each paragraph create paragraph object and add accodring xml to it
            paraObject = Paragraph(paragraph, xml_data_list[i])

            # Add modified text to the paragraphs for better clustering
            modContent = replaceStringXML.replaceValues(paraObject.xml, paraObject.content)
            paraObject.modContent = modContent
            paragraphObject_list.append(paraObject)


    # find optimal K for clustering the text
    optimalClusterK = silouhetteScore.get_Optimal_K(paragraphObject_list)
    # create cluster objects
    clusterObjects = []
    for i in range(optimalClusterK):
        cluster = Cluster()
        cluster.clusterN = i
        clusterObjects.append(cluster)
    # gets list with each paragraph and its cluster number
    clusterObjects = documentCluster.getTextCluster(paragraphObject_list,clusterObjects, optimalClusterK)


    # transform XML data
    modifiedXML = xmlHandler.group_tags(xml_data_list)
    categoricalValues = xmlCategoricalValues.categoriesCluster(modifiedXML)
    #categoricalValues = xmlCategoricalValues.categoriesPredefined(modifiedXML)

    paragraphObject_list = []
    for c in clusterObjects:
        for p in c.paragraphs:
            paragraphObject_list.append(p)


    associationAnalysis.associationRules(categoricalValues, paragraphObject_list)

    xmlLoops = loopFinder.findLoopXML(xml_data_list)

    loopFinder.findLoopParagraph(clusterObjects, xmlLoops)

    for cluster in clusterObjects:
        for p in cluster.paragraphs:

            # Mark clusters with a rule if one of its paragraphs has a rule
            if len(p.ruleA) > 0 and len(cluster.paragraphs) > 1:
                cluster.clusterRule = p.ruleA
                break

    outputPath = 'Output/output.txt'
    outputSaving.saveOutput(clusterObjects, outputPath)

