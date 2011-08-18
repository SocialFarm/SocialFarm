import java.util.Map; 
import java.util.Set; 
import java.util.List; 
import java.util.HashSet; 
import java.util.HashMap; 
import java.util.ArrayList; 
import javax.swing.JOptionPane; 
import javax.swing.JFrame;


import com.mxgraph.view.*;
import com.mxgraph.util.*;
import com.mxgraph.model.*;






public class WorkFlowGraph extends mxGraph  
{ 
   private final WorkFlowEditor wfe; 
   
   public WorkFlowGraph ( WorkFlowEditor editor ) 
   { 
      wfe = editor ;
      allowDanglingEdges = false; 
      stylesheet = getStylesheet() ; 
      Map<String,Object> style = stylesheet.getDefaultVertexStyle() ; 
      style.put(mxConstants.STYLE_ROUNDED, true ) ;
      style.put(mxConstants.STYLE_FONTCOLOR, "#ff4400");
      stylesheet.setDefaultVertexStyle(style) ;
           // TODO , key board events 
           // http://forum.jgraph.com/questions/986/how-to-start-a-chain-reaction-that-deletes-not-only-the-cell-the-user-wants-to-delete-but-all-the-cells-that-cell-is-pointing-to-as-well-and-the-cells-those-are-pointing-toand-so-on?page=1#1124 
   }




        // only the vertices are editable 
   public boolean isCellEditable(Object cell) {
      return !getModel().isEdge(cell);
   }


        // what value to show for cell name
   public String convertValueToString(Object _cell) {
      if (_cell instanceof mxCell ) {  
         mxCell cell = (mxCell ) _cell ; 
         if ( cell.isVertex() && cell.getValue() instanceof Activity ) 
            return ((Activity) cell.getValue()).getName() ; 
      }
      return super.convertValueToString(_cell);
   }

        // assign new name to activity 
   public void cellLabelChanged(Object _cell, Object newValue, boolean autoSize) { 
      mxCell cell = (mxCell) _cell; 
      if (cell.isVertex()) {
         if ( newValue == null || newValue.toString().length() == 0 ) 
            JOptionPane.showMessageDialog(wfe,
                                          "Empty activity name not allowed",
                                          "Error",
                                          JOptionPane.ERROR_MESSAGE);
         else
            ((Activity) cell).setName(newValue.toString()) ;
      } 
      else
         super.cellLabelChanged(cell, newValue, autoSize);
   }


        // tool tip for activity 
   public  String  getToolTipForCell(Object c) { 
      mxCell cell = (mxCell) c;
      if (cell.isVertex() ) {
         Activity act = (Activity) cell.getValue() ;
         return act.getToolTip() ;
      }
      return null;
   }

    
   private mxCell error(String message) { 
      JOptionPane.showMessageDialog( wfe, message ) ; 
      return null; 
   } 


   public boolean isDuplicateVertex(String name) { 
      for( mxCell u : getVertices() ) 
         if ( ((Activity) u.getValue()).getName().equals(name) ) 
            return true;
      return false; 
   }



   public mxCell insertVertex(Object parent, String id, Activity value, 
                              double x, double y, double width, double height) 
   {
      if( isDuplicateVertex( value.getName() ) ) 
         return error( "vertex " +  value.getName() + " already exists" ) ; 
      return (mxCell) super.insertVertex(parent, id, value, x, y, width, height) ;
   }
   


   public mxCell insertVertex(Object parent, String id, Activity value, 
                              double x, double y, double width, double height, String style) 
   { 
      if( isDuplicateVertex( value.getName() ) ) 
         return error( "vertex already exists" ) ; 
      return (mxCell) super.insertVertex(parent, id, value, x, y, width, height, style) ;
   }


   
   public String exportTaskGraph() { 
      Map<String, ArrayList<String>> result = new HashMap<String, ArrayList<String>> () ; 
      for( mxCell u : getVertices() ) { 
         String src = ((Activity) u.getValue()).getName() ; 
         ArrayList<String> dsts = new ArrayList<String> () ; 
         for( int i = 0; i < getModel().getEdgeCount(u); i++ ) {  
            Object edge = getModel().getEdgeAt(u, i) ; 
            mxCell v = (mxCell) getModel().getTerminal(edge, false) ;
                 // get both incoming and outgoing edges.  
                 // hence ignore the incoming ones 
            if( v == u ) 
               continue; 
            String dst = ((Activity ) v.getValue()).getName() ;
            dsts.add( dst ) ; 
         }
         result.put( src, dsts ) ; 
      }
      return WorkFlowTranslator.toJSON( result ) ; 
   }



   public mxCell[] getVertices() { 
      HashSet<mxCell> vertices = new HashSet<mxCell> () ; 
      for ( Object _c : getChildVertices(getDefaultParent()) )
         vertices.add( (mxCell) _c ) ; 
      return vertices.toArray(new mxCell [0]); 
   }



   public String exportDataItems() { 
      Map<String, ArrayList<String>> result = new HashMap<String, ArrayList<String>> () ; 
      for( mxCell u : getVertices() ) { 
         String src = ((Activity) u.getValue()).getName() ; 
         ArrayList<String> items = new ArrayList<String> () ;   
         for( String data : ((Activity) u.getValue()).getAttibutes() ) 
            items.add( data ) ; 
         result.put( src, items ) ; 
      }
      return WorkFlowTranslator.toJSON( result ) ; 
   }
        


   public String exportSkills()  { 
      Map<String, ArrayList<String>> result = new HashMap<String, ArrayList<String>> () ; 
      for( mxCell u : getVertices() ) { 
         String src = ((Activity) u.getValue()).getName() ; 
         ArrayList<String> items = new ArrayList<String> () ;   
         for( String data : ((Activity) u.getValue()).getSkills() ) 
            items.add( data ) ; 
         result.put( src, items ) ; 
      }
      return WorkFlowTranslator.toJSON( result ) ; 
   }
} 



