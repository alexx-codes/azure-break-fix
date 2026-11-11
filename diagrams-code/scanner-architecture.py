from diagrams import Diagram, Cluster, Edge
from diagrams.programming.language import Python
from diagrams.azure.identity import AppRegistrations, ActiveDirectory
from diagrams.azure.general import AllResources

graph_attr = {"splines": "spline", "nodesep": "1.2", "ranksep": "2.5", "fontsize": "20"}

with Diagram("Scanner Architecture", filename="flow", show=False,
             direction="LR", graph_attr=graph_attr):
    with Cluster("Your machine (trust boundary)"):
        scanner = Python("Scanner")

    with Cluster("Azure tenant (trust boundary)"):
        with Cluster("Entra ID"):
            entra = ActiveDirectory("Verifies identity")
            sp = AppRegistrations("Service Principal\n(the identity)")
        arm = AllResources("Resource Manager (ARM)\n+ RBAC: Reader role check")

    scanner >> Edge(label="1. client ID + secret", color="firebrick") >> entra
    entra >> Edge(label="2. access token (~1hr)", color="darkgreen") >> scanner
    scanner >> Edge(label="3. API request + token", color="firebrick") >> arm
    arm >> Edge(label="4. allow/deny, config JSON", color="darkgreen") >> scanner
    entra - Edge(style="dotted", label="looks up") - sp