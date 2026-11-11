from diagrams import Diagram, Cluster, Edge
from diagrams.programming.language import Python
from diagrams.onprem.network import Internet
from diagrams.azure.compute import VM
from diagrams.azure.network import NetworkInterfaces, PublicIpAddresses, NetworkSecurityGroupsClassic
from diagrams.azure.storage import StorageAccounts
from diagrams.azure.monitor import DiagnosticsSettings, LogAnalyticsWorkspaces

graph_attr = {"splines": "spline", "nodesep": "0.9", "ranksep": "1.6", "fontsize": "20"}

with Diagram("Cloud Architecture: rg-scanner-test", filename="cloud", show=False,
             direction="LR", graph_attr=graph_attr):
    internet = Internet("Internet")
    scanner = Python("Scanner\n(Reader role)")

    with Cluster("Resource Group: rg-scanner-test"):
        storage = StorageAccounts("Storage Account\n(public blob access)")

        with Cluster("VNet"):
            nsg = NetworkSecurityGroupsClassic("NSG\n(SSH open to 0.0.0.0/0)")
            pip = PublicIpAddresses("Public IP")
            nic = NetworkInterfaces("NIC")
            vm = VM("VM")

        with Cluster("Monitoring"):
            diag = DiagnosticsSettings("Diagnostic Settings\n(missing)")
            logs = LogAnalyticsWorkspaces("Log Analytics\nWorkspace")

    internet >> Edge(label="SSH :22", color="firebrick") >> pip >> nic >> vm
    nsg - Edge(style="dotted", label="filters") - nic
    diag >> Edge(style="dashed", color="firebrick", label="not connected") >> logs

    scanner >> Edge(style="dashed", color="darkgreen", label="read-only") >> [storage, nsg, vm, diag]