<?xml version="1.0" encoding="UTF-8"?>
<core:Model xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:application="org.eclipse.jwt/application" xmlns:core="org.eclipse.jwt/core" xmlns:data="org.eclipse.jwt/data" xmlns:organisations="org.eclipse.jwt/organisations" xmlns:processes="org.eclipse.jwt/processes" name="Workflow" author="" version="" fileversion="1.1.0">
  <subpackages name="Applications">
    <ownedComment text="The standard package for applications"/>
    <elements xsi:type="application:Application" name="Social Farm"/>
  </subpackages>
  <subpackages name="Roles">
    <ownedComment text="The standard package for roles"/>
    <elements xsi:type="organisations:Role" name="Writer" icon=""/>
    <elements xsi:type="organisations:Role" name="Researcher" icon=""/>
    <elements xsi:type="organisations:Role" name="Editor" icon=""/>
    <elements xsi:type="organisations:Role" name="Customer"/>
  </subpackages>
  <subpackages name="Data">
    <ownedComment text="The standard package for data"/>
    <subpackages name="Datatypes">
      <ownedComment text="The standard package for datatypes"/>
      <elements xsi:type="data:DataType" name="URL"/>
      <elements xsi:type="data:DataType" name="dioParameter"/>
      <elements xsi:type="data:DataType" name="qualifier"/>
      <elements xsi:type="data:DataType" name="searchquery"/>
      <elements xsi:type="data:DataType" name="filename"/>
    </subpackages>
    <elements xsi:type="application:WebServiceApplication"/>
  </subpackages>
  <elements xsi:type="processes:Activity" name="Social News Workflow">
    <ownedComment text="This is a basic activity"/>
    <nodes xsi:type="processes:InitialNode" name="start" out="//@elements.0/@edges.0"/>
    <nodes xsi:type="processes:FinalNode" name="stop" in="//@elements.0/@edges.2"/>
    <nodes xsi:type="processes:ActivityLinkNode" name="Research Phase" in="//@elements.0/@edges.0" out="//@elements.0/@edges.1" linksto="//@elements.2"/>
    <nodes xsi:type="processes:ActivityLinkNode" name="Revision Phase" in="//@elements.0/@edges.1" out="//@elements.0/@edges.2" linksto="//@elements.3"/>
    <edges source="//@elements.0/@nodes.0" target="//@elements.0/@nodes.2"/>
    <edges source="//@elements.0/@nodes.2" target="//@elements.0/@nodes.3"/>
    <edges source="//@elements.0/@nodes.3" target="//@elements.0/@nodes.1"/>
  </elements>
  <elements xsi:type="data:Data" name="article " value=""/>
  <elements xsi:type="processes:Activity" name="Research Phase" icon="">
    <nodes xsi:type="processes:Action" out="//@elements.2/@edges.0"/>
    <nodes xsi:type="processes:FinalNode" in="//@elements.2/@edges.3"/>
    <nodes xsi:type="processes:Action" name="Request" in="//@elements.2/@edges.0" out="//@elements.2/@edges.1" performedBy="//@subpackages.1/@elements.0"/>
    <nodes xsi:type="processes:Action" name="Research" in="//@elements.2/@edges.1" out="//@elements.2/@edges.5" performedBy="//@subpackages.1/@elements.1"/>
    <nodes xsi:type="processes:Action" name="Review" in="//@elements.2/@edges.5" out="//@elements.2/@edges.2" performedBy="//@subpackages.1/@elements.0"/>
    <nodes xsi:type="processes:DecisionNode" in="//@elements.2/@edges.2" out="//@elements.2/@edges.3 //@elements.2/@edges.4"/>
    <nodes xsi:type="processes:ActivityLinkNode" name="Repeat Research" in="//@elements.2/@edges.4" linksto="//@elements.2"/>
    <edges source="//@elements.2/@nodes.0" target="//@elements.2/@nodes.2"/>
    <edges source="//@elements.2/@nodes.2" target="//@elements.2/@nodes.3"/>
    <edges source="//@elements.2/@nodes.4" target="//@elements.2/@nodes.5"/>
    <edges source="//@elements.2/@nodes.5" target="//@elements.2/@nodes.1"/>
    <edges source="//@elements.2/@nodes.5" target="//@elements.2/@nodes.6"/>
    <edges source="//@elements.2/@nodes.3" target="//@elements.2/@nodes.4"/>
  </elements>
  <elements xsi:type="processes:Activity" name="Revision Phase" icon="">
    <nodes xsi:type="processes:FinalNode" in="//@elements.3/@edges.1"/>
    <nodes xsi:type="processes:Action" name="Write" in="//@elements.3/@edges.4" out="//@elements.3/@edges.2" performedBy="//@subpackages.1/@elements.0"/>
    <nodes xsi:type="processes:Action" name="Review" in="//@elements.3/@edges.2" out="//@elements.3/@edges.3" performedBy="//@subpackages.1/@elements.2"/>
    <nodes xsi:type="processes:DecisionNode" name="Approve_Revise" in="//@elements.3/@edges.3" out="//@elements.3/@edges.0 //@elements.3/@edges.1"/>
    <nodes xsi:type="processes:ActivityLinkNode" name="Repeat Revision" in="//@elements.3/@edges.0"/>
    <nodes xsi:type="processes:InitialNode" out="//@elements.3/@edges.4"/>
    <edges source="//@elements.3/@nodes.3" target="//@elements.3/@nodes.4">
      <guard name="Revise" textualdescription="Approve_Revise.Revise" shortdescription=""/>
    </edges>
    <edges source="//@elements.3/@nodes.3" target="//@elements.3/@nodes.0">
      <guard name="Approve" textualdescription="Approve_Revise.Approve"/>
    </edges>
    <edges source="//@elements.3/@nodes.1" target="//@elements.3/@nodes.2"/>
    <edges source="//@elements.3/@nodes.2" target="//@elements.3/@nodes.3"/>
    <edges source="//@elements.3/@nodes.5" target="//@elements.3/@nodes.1"/>
  </elements>
</core:Model>
