<?xml version="1.0" encoding="UTF-8"?>
<core:Model xmi:version="2.0" xmlns:xmi="http://www.omg.org/XMI" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:application="org.eclipse.jwt/application" xmlns:core="org.eclipse.jwt/core" xmlns:data="org.eclipse.jwt/data" xmlns:organisations="org.eclipse.jwt/organisations" xmlns:processes="org.eclipse.jwt/processes" name="Workflow" author="" version="" fileversion="1.0.0">
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
  <elements xsi:type="processes:Activity" name="Overview">
    <ownedComment text="This is a basic activity"/>
    <nodes xsi:type="processes:Action" name="Define workflow &amp; export XPDL" performedBy="//@elements.3" executedBy="//@elements.2"/>
    <nodes xsi:type="processes:Action" name="Upload XPDL to Django App" performedBy="//@elements.3" executedBy="//@elements.5"/>
    <nodes xsi:type="processes:Action" name="Upload XPDL to Scarbo" performedBy="//@elements.3" executedBy="//@elements.1"/>
  </elements>
  <elements xsi:type="application:Application" name="Scarbo Task Engine"/>
  <elements xsi:type="application:Application" name="Java Workflow Toolkit"/>
  <elements xsi:type="organisations:Role" name="Buisness Architect" icon=""/>
  <elements xsi:type="organisations:Role" name="Customer"/>
  <elements xsi:type="application:Application" name="Django Facebook App"/>
  <elements xsi:type="processes:Activity" name="Django - Scarbo Interface">
    <nodes xsi:type="processes:Action" name="Import XPDL "/>
    <nodes xsi:type="processes:Action" name="Import Workflow ID"/>
  </elements>
</core:Model>
