import pandas as pd
from pybatfish.client.session import Session
from pybatfish.datamodel import *
from pybatfish.datamodel.answer import *
from pybatfish.datamodel.flow import *
from pybatfish.client.commands import *
from pybatfish.question import bfq
from pybatfish.question.question import load_questions

BF_SERVICE_IP = "127.0.0.1"
BF_SNAPSHOT_PATH = "networks/example/live"
BF_SNAPSHOT_NAME = "demo-session"
BF_NETWORK_NAME = "demo-network"

bf_session.host = BF_SERVICE_IP

load_questions()

bf_set_network(BF_NETWORK_NAME)

bf_session.init_snapshot(BF_SNAPSHOT_PATH, name=BF_SNAPSHOT_NAME, overwrite=True)

df = bfq.interfaceProperties().answer().frame()

bfq.interfaceProperties(nodes="/core/").answer().frame()

df.iloc[1]

for row in df.itertuples():
    print(row.Interface, "--MTU-->",row.MTU)

bfq.ipOwners().answer().frame()

bfq.ipOwners(duplicatesOnly=True).answer().frame()

if not bfq.ipOwners(duplicatesOnly=True).answer().frame().empty:
    ipc = bfq.ipOwners(duplicatesOnly=True).answer().frame()
    print("ERROR: duplicate IP addresses found\n", str(ipc))

bfq.bgpProcessConfiguration().answer().frame()

bfq.bgpSessionStatus().answer().frame()
bfq.bgpSessionStatus(status="!ESTABLISHED").answer().frame()
bfq.bgpSessionCompatibility(status="!UNIQUE_MATCH").answer().frame()

bfq.ospfSessionCompatibility().answer().frame()
    
result = bfq.reachability(pathConstraints=PathConstraints(startLocation = '/as2/'), headers=HeaderConstraints(dstIps='host1', srcIps='0.0.0.0/0', applications='DNS'), actions='SUCCESS').answer().frame()
result.Flow
result.Traces[0]
result.Traces[0][0].disposition

result = bfq.bidirectionalReachability(pathConstraints=PathConstraints(startLocation = '/as2dist1/'), headers=HeaderConstraints(dstIps='host1', srcIps='0.0.0.0/0', applications='DNS'), returnFlowType='SUCCESS').answer().frame()

result = bfq.filterLineReachability().answer().frame()
result.head(5)
result.iloc[0]

result = bfq.testFilters(headers=HeaderConstraints(srcIps='1.1.1.1', dstIps='2.128.0.101', applications = ['dns']), nodes='as2dept1', filters='RESTRICT_HOST_TRAFFIC_IN').answer().frame()
result.head(5)
result.iloc[0]

result = bfq.testFilters(headers=HeaderConstraints(srcIps='2.128.1.1', dstIps='2.128.0.101', applications = ['dns']), nodes='as2dept1', filters='RESTRICT_HOST_TRAFFIC_IN').answer().frame()