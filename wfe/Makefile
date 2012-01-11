CLASSPATH=lib/commons-beanutils-1.8.3.jar:lib/commons-logging-1.1.1.jar:lib/commons-collections-3.2.1.jar:lib/ezmorph-1.0.5.jar:lib/commons-lang-2.4.jar:lib/json-lib-2.4-jdk15.jar:lib/jgraphx-1.7.1.3.jar:.

wfe : 
	javac -g -classpath $(CLASSPATH)  WorkFlowEditor.java WorkFlowGraph.java Activity.java 
	jar cvf wfe.jar *.class 

lint : 
	javac -Xlint -g -classpath $(CLASSPATH)  WorkFlowEditor.java WorkFlowGraph.java Activity.java 

translator: 
	javac -g -classpath $(CLASSPATH)  WorkFlowTranslator.java  
	java -classpath $(CLASSPATH)  WorkFlowTranslator

test : wfe
	java -classpath $(CLASSPATH) WorkFlowEditor&

debug : wfe
	ddd --jdb -J-Duser.home=. -launch -classpath $(CLASSPATH)  WorkFlowEditor&
	#ddd --debugger "jdb -classpath $(CLASSPATH) WorkFlowEditor"  --command=jdb.cmd
	#ddd --jdb -classpath $(CLASSPATH) -command=jdb.cmd WorkFlowEditor&

clean : 
	rm -f *.class *~ wfe.jar 

tar : 
	cd .. ; tar --exclude='.svn' -czvf wfe.tgz wfe

