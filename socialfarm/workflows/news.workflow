<?xml version="1.0" encoding="UTF-8"?>
<core:Model xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:application="org.eclipse.jwt/application" xmlns:core="org.eclipse.jwt/core" xmlns:data="org.eclipse.jwt/data" xmlns:organisations="org.eclipse.jwt/organisations" xmlns:processes="org.eclipse.jwt/processes" name="Workflow" author="" version="" fileversion="1.0.0">
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
    <nodes xsi:type="processes:InitialNode" name="start"/>
    <nodes xsi:type="processes:FinalNode" name="stop"/>
    <nodes xsi:type="processes:Action" name="research article" performedBy="//@subpackages.1/@elements.1" inputs="//@elements.1" outputs="//@elements.1"/>
    <nodes xsi:type="processes:Action" name="write article" performedBy="//@subpackages.1/@elements.0" inputs="//@elements.1" outputs="//@elements.1"/>
    <nodes xsi:type="processes:Action" name="edit article" performedBy="//@subpackages.1/@elements.2" inputs="//@elements.1" outputs="//@elements.1"/>
    <nodes xsi:type="processes:Action" name="request article" performedBy="//@subpackages.1/@elements.3" executedBy="//@subpackages.0/@elements.0" inputs="//@elements.1" outputs="//@elements.1"/>
    <nodes xsi:type="processes:Action" name="approve/revise" performedBy="//@subpackages.1/@elements.2" inputs="//@elements.1" outputs="//@elements.1"/>
  </elements>
  <elements xsi:type="data:Data" name="article " value=""/>
</core:Model>
