<?xml version="1.0" encoding="UTF-8"?>
<core:Model xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:core="org.eclipse.jwt/core" xmlns:data="org.eclipse.jwt/data" xmlns:organisations="org.eclipse.jwt/organisations" xmlns:processes="org.eclipse.jwt/processes" name="Test" author="Orie Steel" version="" fileversion="1.1.0">
  <subpackages name="Applications">
    <ownedComment text="The standard package for applications"/>
  </subpackages>
  <subpackages name="Roles">
    <ownedComment text="The standard package for roles"/>
    <elements xsi:type="organisations:Role" name="Author" icon=""/>
    <elements xsi:type="organisations:Role" name="Researcher" icon=""/>
    <elements xsi:type="organisations:Role" name="Editor" icon=""/>
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
  <elements xsi:type="processes:Activity" name="Test">
    <ownedComment text="This is a basic activity"/>
    <nodes xsi:type="processes:InitialNode" name="Initial Node" out="//@elements.0/@edges.0"/>
    <nodes xsi:type="processes:FinalNode" name="Final Node" in="//@elements.0/@edges.3"/>
    <nodes xsi:type="processes:Action" name="research" in="//@elements.0/@edges.0" out="//@elements.0/@edges.1" performedBy="//@subpackages.1/@elements.1"/>
    <nodes xsi:type="processes:Action" name="write" in="//@elements.0/@edges.1" out="//@elements.0/@edges.2" performedBy="//@subpackages.1/@elements.0"/>
    <nodes xsi:type="processes:Action" name="edit" in="//@elements.0/@edges.2" out="//@elements.0/@edges.3" performedBy="//@subpackages.1/@elements.2"/>
    <edges source="//@elements.0/@nodes.0" target="//@elements.0/@nodes.2"/>
    <edges source="//@elements.0/@nodes.2" target="//@elements.0/@nodes.3"/>
    <edges source="//@elements.0/@nodes.3" target="//@elements.0/@nodes.4"/>
    <edges source="//@elements.0/@nodes.4" target="//@elements.0/@nodes.1"/>
  </elements>
</core:Model>
