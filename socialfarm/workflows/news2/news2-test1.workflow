<?xml version="1.0" encoding="UTF-8"?>
<core:Model xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:core="org.eclipse.jwt/core" xmlns:data="org.eclipse.jwt/data" xmlns:organisations="org.eclipse.jwt/organisations" xmlns:processes="org.eclipse.jwt/processes" name="news2-test1" author="" version="" fileversion="1.0.0">
  <subpackages name="Applications">
    <ownedComment text="The standard package for applications"/>
  </subpackages>
  <subpackages name="Roles">
    <ownedComment text="The standard package for roles"/>
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
  </subpackages>
  <elements xsi:type="processes:Activity" name="test1">
    <ownedComment text="This is a basic activity"/>
    <nodes xsi:type="processes:Action" name="AcceptArticle" in="//@elements.0/@edges.3" out="//@elements.0/@edges.0" performedBy="//@elements.1"/>
    <nodes xsi:type="processes:Action" name="ResearchInput" in="//@elements.0/@edges.0" out="//@elements.0/@edges.1" performedBy="//@elements.2"/>
    <nodes xsi:type="processes:Action" name="WriteArticle" in="//@elements.0/@edges.1" out="//@elements.0/@edges.2" performedBy="//@elements.1"/>
    <nodes xsi:type="processes:Action" name="ApproveReject" in="//@elements.0/@edges.2" out="//@elements.0/@edges.4" performedBy="//@elements.3"/>
    <nodes xsi:type="processes:InitialNode" out="//@elements.0/@edges.3"/>
    <nodes xsi:type="processes:FinalNode" in="//@elements.0/@edges.4"/>
    <edges source="//@elements.0/@nodes.0" target="//@elements.0/@nodes.1"/>
    <edges source="//@elements.0/@nodes.1" target="//@elements.0/@nodes.2"/>
    <edges source="//@elements.0/@nodes.2" target="//@elements.0/@nodes.3"/>
    <edges source="//@elements.0/@nodes.4" target="//@elements.0/@nodes.0"/>
    <edges source="//@elements.0/@nodes.3" target="//@elements.0/@nodes.5"/>
  </elements>
  <elements xsi:type="organisations:Role" name="Author"/>
  <elements xsi:type="organisations:Role" name="Researcher"/>
  <elements xsi:type="organisations:Role" name="Editor"/>
</core:Model>
