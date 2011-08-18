import javax.swing.JFrame;
import javax.swing.JOptionPane; 
import java.util.Hashtable; 
import java.awt.event.MouseAdapter; 
import java.awt.event.MouseEvent;
import javax.swing.ToolTipManager;
import java.awt.GraphicsEnvironment; 
import java.awt.Rectangle; 


import java.awt.Point; 
import java.util.HashSet; 
import java.util.Collection;  


import java.io.Serializable;
import java.io.ObjectOutputStream;
import java.io.FileOutputStream;
import java.io.ObjectInputStream;
import java.io.FileInputStream;
import java.io.IOException;


import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.AbstractAction;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.SwingUtilities;
import javax.swing.TransferHandler;
import javax.swing.UIManager;
import javax.swing.KeyStroke; 
import java.awt.event.KeyEvent; 
import javax.swing.JFileChooser; 
import javax.swing.filechooser.FileNameExtensionFilter; 
import java.io.File; 



import com.mxgraph.swing.mxGraphComponent;
import com.mxgraph.view.mxGraph;
import com.mxgraph.util.mxConstants;
import com.mxgraph.view.mxStylesheet;
import com.mxgraph.model.*;
import com.mxgraph.layout.*; 
import com.mxgraph.layout.hierarchical.* ; 





public class WorkFlowEditor extends JFrame implements ActionListener 
{
   private static final String appname = "SocialFarm Work Flow Editor" ; 

   private final WorkFlowGraph graph = new WorkFlowGraph(this) ;

   private Object parent ; 

   private final mxGraphComponent graphComponent = new mxGraphComponent(graph);

   private final JMenuBar menuBar = new JMenuBar(); 

        // file menu items 
   private final JMenu fileMenu = new JMenu("File");
   private JMenuItem saveMenuItem;
   private JMenuItem restoreMenuItem;
   private JMenuItem pushMenuItem;   // todo 
   private JMenuItem pullMenuItem;   // todo 
   private JMenuItem quitMenuItem;

        // view menu items 
   private JMenu viewMenu; 
   private JMenuItem zoomInMenuItem;
   private JMenuItem zoomOutMenuItem;
   private JMenuItem reLayoutMenuItem;

        // workflow menu items 
   private JMenu workflowMenu; 
   private JMenuItem addTaskMenuItem; 
   private JMenuItem editTaskMenuItem; 
   private JMenuItem delMenuItem; 

        // help menu items 
   private JMenu helpMenu; 
   private JMenuItem helpMenuItem; 
   private JMenuItem aboutMenuItem; 




	public WorkFlowEditor()
	{
		super(appname);

      graphComponent.setToolTips(true); 

		parent = graph.getDefaultParent();

		getContentPane().add(graphComponent);

      graphComponent.getGraphControl().addMouseListener( 
         new MouseAdapter() {
            public void mouseReleased(MouseEvent e)
            {
               mxCell cell = (mxCell) graphComponent.getCellAt(e.getX(), e.getY());
               if (cell != null && e.getButton() == MouseEvent.BUTTON3 &&  cell.isVertex() ) 
                  ((Activity) cell.getValue()) . getEditDialog( WorkFlowEditor.this ) ; 
               else if (cell == null && e.getButton() == MouseEvent.BUTTON3) 
                  addVertex( e.getX(), e.getY() ) ; 
            }
         } ) ; 


          // file menu 
      fileMenu.setMnemonic(KeyEvent.VK_F);
      fileMenu.getAccessibleContext().setAccessibleDescription("Menu handling save/restore/export of Workflows");
      saveMenuItem = new JMenuItem( "Save", KeyEvent.VK_S );
      saveMenuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_S, ActionEvent.ALT_MASK));
      saveMenuItem.getAccessibleContext().setAccessibleDescription("Save your workflow to a file");
      saveMenuItem.addActionListener(this);
      fileMenu.add(saveMenuItem);

      restoreMenuItem = new JMenuItem( "Restore", KeyEvent.VK_R );
      restoreMenuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_R, ActionEvent.ALT_MASK));
      restoreMenuItem.getAccessibleContext().setAccessibleDescription("Restore your workflow saved in a file");
      restoreMenuItem.addActionListener(this);
      fileMenu.add(restoreMenuItem);

      fileMenu.addSeparator();

      pushMenuItem = new JMenuItem( "Push" , KeyEvent.VK_U ) ; 
      pushMenuItem.setAccelerator( KeyStroke.getKeyStroke(KeyEvent.VK_U,  ActionEvent.ALT_MASK)); 
      pushMenuItem.getAccessibleContext().setAccessibleDescription("Push your workflow to socialfarm" ) ; 
      pushMenuItem.addActionListener(this) ; 
      fileMenu.add(pushMenuItem) ; 

      pullMenuItem = new JMenuItem( "Pull" , KeyEvent.VK_D ) ; 
      pullMenuItem.setAccelerator( KeyStroke.getKeyStroke(KeyEvent.VK_D,  ActionEvent.ALT_MASK)); 
      pullMenuItem.getAccessibleContext().setAccessibleDescription("Pull the workflow from socialfarm" ) ; 
      pullMenuItem.addActionListener(this) ;
      fileMenu.add( pullMenuItem ) ; 

      fileMenu.addSeparator();
      quitMenuItem = new JMenuItem( "Quit" , KeyEvent.VK_Q ) ; 
      quitMenuItem.setAccelerator( KeyStroke.getKeyStroke(KeyEvent.VK_Q,  ActionEvent.ALT_MASK)); 
      quitMenuItem.getAccessibleContext().setAccessibleDescription("Quit the workflow editor" ) ; 
      quitMenuItem.addActionListener(this) ;
      fileMenu.add( quitMenuItem ) ; 

      menuBar.add(fileMenu);

           // view menu 
      viewMenu = new JMenu("View");
      viewMenu.setMnemonic(KeyEvent.VK_V);
      viewMenu.getAccessibleContext().setAccessibleDescription("Views for Workflow Editor");
      zoomInMenuItem = new JMenuItem( "Zoom +", KeyEvent.VK_I );
      zoomInMenuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_I, ActionEvent.ALT_MASK));
      zoomInMenuItem.getAccessibleContext().setAccessibleDescription("Zoom into workflow");
      zoomInMenuItem.addActionListener(this);
      viewMenu.add(zoomInMenuItem);

      zoomOutMenuItem = new JMenuItem( "Zoom -", KeyEvent.VK_O );
      zoomOutMenuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_O, ActionEvent.ALT_MASK));
      zoomOutMenuItem.getAccessibleContext().setAccessibleDescription("Zoom into workflow");
      zoomOutMenuItem.addActionListener(this);
      viewMenu.add(zoomOutMenuItem);
      viewMenu.addSeparator(); 

      reLayoutMenuItem = new JMenuItem( "Layout", KeyEvent.VK_L );
      reLayoutMenuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_L, ActionEvent.ALT_MASK));
      reLayoutMenuItem.getAccessibleContext().setAccessibleDescription("Layout");
      reLayoutMenuItem.addActionListener(this);
      viewMenu.add(reLayoutMenuItem);
           
      menuBar.add(viewMenu);
      

          // Workflow menu 
      workflowMenu = new JMenu("Workflow");
      workflowMenu.setMnemonic(KeyEvent.VK_W);
      workflowMenu.getAccessibleContext().setAccessibleDescription("Workflow Actions");

      addTaskMenuItem = new JMenuItem( "Add Task", KeyEvent.VK_A );
      addTaskMenuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_A, ActionEvent.ALT_MASK));
      addTaskMenuItem.getAccessibleContext().setAccessibleDescription("Add task in workflow");
      addTaskMenuItem.addActionListener(this);
      workflowMenu.add(addTaskMenuItem);
      editTaskMenuItem = new JMenuItem( "Edit Task", KeyEvent.VK_E );
      editTaskMenuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_E, ActionEvent.ALT_MASK));
      editTaskMenuItem.getAccessibleContext().setAccessibleDescription("Edit task in workflow");
      editTaskMenuItem.addActionListener(this);
      workflowMenu.add(editTaskMenuItem);
      delMenuItem = new JMenuItem( "Delete", KeyEvent.VK_D );
      delMenuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_D, ActionEvent.ALT_MASK));
      delMenuItem.getAccessibleContext().setAccessibleDescription("Delete task or transition from workflow");
      delMenuItem.addActionListener(this);
      workflowMenu.add(delMenuItem);
      menuBar.add(workflowMenu);


           // Help menu 
      helpMenu = new JMenu("Help");
      helpMenu.setMnemonic(KeyEvent.VK_H);
      helpMenu.getAccessibleContext().setAccessibleDescription("Help for Workflow Editor");
      helpMenuItem = new JMenuItem( "Help", KeyEvent.VK_H );
      helpMenuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_H, ActionEvent.ALT_MASK));
      helpMenuItem.getAccessibleContext().setAccessibleDescription("Help on workflow editor");
      helpMenuItem.addActionListener(this);
      helpMenu.add(helpMenuItem);
      aboutMenuItem = new JMenuItem( "About", KeyEvent.VK_A );
      aboutMenuItem.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_A, ActionEvent.ALT_MASK));
      aboutMenuItem.getAccessibleContext().setAccessibleDescription("Help on workflow editor");
      aboutMenuItem.addActionListener(this);
      helpMenu.add(aboutMenuItem);
      menuBar.add(helpMenu);
      
      setJMenuBar(menuBar);


           // temp demo code, to go 
		graph.getModel().beginUpdate();
		try
		{
			Object v1 = graph.insertVertex(parent, null, new Activity("Hello"), 20, 20, 80, 30 );
			Object v2 = graph.insertVertex(parent, null, new Activity("World!"), 240, 150,  80, 30 );
			graph.insertEdge(parent, null, "Edge", v1, v2);
		}
		finally
		{
			graph.getModel().endUpdate();
		}

      Object v3 = graph.insertVertex(parent, null, new Activity("Test"), 100, 150,  80, 30 );
           //graph.refresh() ; 
	}




   Object getCellAt( int x, int y) { 
      return graphComponent.getCellAt(x, y);
   }




   private void doOrganicGraphLayout() { 
      for( int i = 0; i < 3; i++ ) { 
         mxOrganicLayout layout = 
            new mxOrganicLayout(graph, 
                                graph.getView().getGraphBounds().getRectangle() );
              //System.out.println( graph.getView().getGraphBounds() ) ; 

         layout.setOptimizeBorderLine(true); 
         layout.setOptimizeEdgeCrossing(true); 
         layout.setOptimizeEdgeDistance(true);  
         layout.setOptimizeEdgeLength(true); 
         layout.setOptimizeNodeDistribution(true); 
         layout.setApproxNodeDimensions(true); 

              //System.out.println( layout.getRadiusScaleFactor() ) ; 
              //System.out.println( layout.getRadiusScaleFactor() ) ; 
              //System.out.println( layout.getNodeDistributionCostFactor() ) ; 
              //System.out.println( layout.getEdgeDistanceCostFactor() ) ; 
              //System.out.println( layout.getEdgeLengthCostFactor() ) ; 
         layout.setInitialMoveRadius(15); 
         layout.setRadiusScaleFactor(0.75);
         layout.setBorderLineCostFactor(0.50); 
         layout.setMaxDistanceLimit(50.0); 
         layout.setNodeDistributionCostFactor(layout.getNodeDistributionCostFactor() * 3);
         layout.setEdgeCrossingCostFactor(0.1);
         layout.setEdgeLengthCostFactor( layout.getEdgeLengthCostFactor() / 4 ) ;
         
         layout.execute(parent) ;
      }
   }


   private void doGraphLayout() { 
      Rectangle initialrect = graph.getView().getGraphBounds().getRectangle() ; 
      doOrganicGraphLayout(); 
      Rectangle finalrect = graph.getView().getGraphBounds().getRectangle() ; 
      System.out.println( initialrect.toString() ) ; 
      System.out.println( finalrect.toString() ) ; 

      double scalex = initialrect.getWidth() / finalrect.getWidth() ; 
      double scaley = initialrect.getHeight() / finalrect.getHeight() ; 
      graph.getView().scaleAndTranslate( scalex > scaley ? scaley : scalex, 
                                         initialrect.getX() - finalrect.getX() , 
                                         initialrect.getY() - finalrect.getY() ) ; 
           //mxGraphLayout l = new mxCircleLayout(graph); 
           //l.execute(graph.getDefaultParent());
           //doOrganicGraphLayout(); 
      finalrect = graph.getView().getGraphBounds().getRectangle() ; 
      System.out.println( finalrect.toString() ) ; 
   }

   private void addVertex() 
   {    
      addVertex(0,0) ; 
      doGraphLayout() ; 
   } 



   private void addVertex(int x, int y) { 
      String cellname = JOptionPane.showInputDialog( this, "Enter activity name" ) ; 
      if ( cellname == null || cellname.length() == 0 ) 
         return ; 
      try { 
         graph.getModel().beginUpdate();      
         graph.insertVertex( parent, null, new Activity(cellname), x, y, 80, 30 );
      }
      finally {
         graph.getModel().endUpdate();
      }
   }




   public void actionPerformed(ActionEvent e) {
      if ( e.getSource() == saveMenuItem ) { 
         JFileChooser chooser = new JFileChooser();
         FileNameExtensionFilter filter = new FileNameExtensionFilter( "Java Serialized File", "ser" );
         chooser.setFileFilter(filter);
         int returnVal = chooser.showSaveDialog(saveMenuItem);
         if(returnVal == JFileChooser.APPROVE_OPTION) {            
            String savefilename = chooser.getSelectedFile().getName() ; 
            File curDir = chooser.getCurrentDirectory();
            if( savefilename.lastIndexOf(".ser") < 0 && savefilename.lastIndexOf(".SER") < 0 )  
               savefilename += ".ser" ; 
            savefilename = curDir.toString() + "/" + savefilename ; 
            saveGraph( savefilename ) ; 
                 //System.out.println("saved file: " + savefilename );
         }
      }
      else if ( e.getSource() == restoreMenuItem ) { 
         JFileChooser chooser = new JFileChooser();
         FileNameExtensionFilter filter = new FileNameExtensionFilter( "Java Serialized File", "ser" );
         chooser.setFileFilter(filter);
         int returnVal = chooser.showOpenDialog(restoreMenuItem);
         if(returnVal == JFileChooser.APPROVE_OPTION) {            
            File f = chooser.getSelectedFile() ; 
                 //System.out.println("restoring saved file: " + f.toString() );
            restoreGraph(f) ; 
         }
      }
      else if( e.getSource() == quitMenuItem ) { 
         super.dispose() ; 
      }
      else if( e.getSource() == zoomInMenuItem ) { 
         graphComponent.zoomIn() ; 
      }
      else if( e.getSource() == zoomOutMenuItem ) { 
         graphComponent.zoomOut() ; 
      }    
      else if( e.getSource() == reLayoutMenuItem ) {
         doGraphLayout();
      }    

      else if (e.getSource() == addTaskMenuItem) { 
         addVertex() ; 
      }
      else if(e.getSource() == editTaskMenuItem) { 
         mxGraph graph = graphComponent.getGraph();
         for( Object _cell : graph.getSelectionCells() ) { 
            mxCell cell = (mxCell) _cell ; 
            if( cell.isVertex() ) 
               ((Activity) cell.getValue()).getEditDialog( WorkFlowEditor.this ) ; 
         }
      }
      else if( e.getSource() == delMenuItem ) { 
         graph.removeCells( graph.getSelectionCells() ) ;
      }

      else if (e.getSource() == aboutMenuItem) { 
         JOptionPane.showMessageDialog(
            this, "Socialfarm workflow editor.\n" + 
            "Tool for visually designing workflows" + 
            " that run on the socialfarm infrastructure.\n" + 
            "More information available at socialfarm.org\n" + 
            "Authors :\n" + 
            "   Vivek Pathak" );
      }
      else if (e.getSource() == helpMenuItem) { 
           // download.java.net/javadesktop/javahelp/jhug.pdf
      }
   }


   private void restoreGraph(File f) {
      try {
         FileInputStream fis = new FileInputStream(f);
         ObjectInputStream in = new ObjectInputStream(fis);
         mxIGraphModel model = (mxIGraphModel) in.readObject();
         graph.setModel(model) ; 
         in.close();
         fis.close();
      } catch(IOException ex) {
         ex.printStackTrace();
         return;
      } catch(java.lang.ClassNotFoundException ex) { 
         ex.printStackTrace();
         return ;
      }
   }

   private void saveGraph(String filename) { 
      mxIGraphModel model = graph.getModel() ; 
      FileOutputStream fos = null;
      ObjectOutputStream out = null;
      try {
         fos = new FileOutputStream(filename);
         out = new ObjectOutputStream(fos);
         out.writeObject(model);
         out.close();
      }
      catch(IOException ex) { 
         ex.printStackTrace();
      }
   }


	public static void main(String[] args)
	{
		WorkFlowEditor frame = new WorkFlowEditor();
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.setSize(400, 320);
		frame.setVisible(true);
	}
}
