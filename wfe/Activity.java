import java.util.EventObject;
import java.util.Map; 
import java.util.HashMap;
import java.util.Set;
import java.util.HashSet;
import java.io.Serializable;


import java.awt.Container; 
import java.awt.BorderLayout;
import java.awt.GridLayout;
import javax.swing.JDialog;
import javax.swing.JTabbedPane; 
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.JComponent;
import javax.swing.JPanel;
import javax.swing.JButton;
import javax.swing.JFrame;
import java.awt.Window; 
import java.awt.event.ActionListener; 
import java.awt.event.ActionEvent; 
import javax.swing.BoxLayout ;
import javax.swing.JScrollPane;
import java.awt.Dimension;
  
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;

import com.mxgraph.model.mxCell;
import com.mxgraph.swing.mxGraphComponent;
import com.mxgraph.util.mxUtils;
import com.mxgraph.view.mxGraph;

import java.io.* ;



public class Activity extends mxCell implements Serializable
{
   static final long serialVersionUID = 4665261573913958775L;

   private Document doc = mxUtils.createDocument();

   private String name = null;

   private Set<String> attributes = new HashSet<String> () ; 
   
   private Set<String> skills = new HashSet<String> () ; 

   private Set<String> permissions = new HashSet<String> () ; 

   final int MIN_HEIGHT = 3; 
   
   final int MIN_WIDTH = 9; 

   int height = MIN_HEIGHT ;  
   
   int width = MIN_WIDTH; 

   public int getWidth() { 
           //System.out.println( "width is " + width ) ; 
      return 8 * width + 4; 
   }

   public int getHeight() { 
           //System.out.println( "height is " + height ) ; 
      return 13 * height + 4; 
   }

   public Activity(String name)
   {
      super(name); 
      setName(name) ; 
   }

   
   public String getHTMLListFragment(String nameoflist, Set<String> list) { 
      if( list.size() == 0 ) 
         return "" ; 

      StringBuffer b = new StringBuffer() ;
      b.append( "<P align=\"left\"><I>");
      b.append( nameoflist ) ; 
      b.append( ":</I><BR></P>" ) ; 
      height++ ;

      for( String attr : list ) { 
         b.append( attr ) ; 
         b.append( "<BR>" ) ;
         width = Math.max( width, attr.length() ) ;
         height++ ; 
      }

      return b.toString() ; 
   }
      

   public String getHTML( ) { 
           // calculate height and width in number of chars for 
           // resize 
      height = MIN_HEIGHT ;     
      width = MIN_WIDTH; 

           // html code for formatted task info
      StringBuffer b = new StringBuffer( ) ; 
      b.append( "<P><B>" ) ; 
      b.append( name ) ; 
      width = Math.max( width, name.length() ) ; 
      b.append( "</B></P><HR width=100%>" ) ; 
      height ++ ; 

      b.append( getHTMLListFragment( "Data" , attributes ) ) ; 
      b.append( getHTMLListFragment( "Skills" , skills ) ) ; 
      b.append( getHTMLListFragment( "Permissions" , permissions ) ) ;         
           //System.out.println( "Got the string:" + b.toString() ) ;
           //System.out.println( "Got dimensions : " + width + " , " + height ) ; 
      return b.toString() ; 
   }




   public String getName() { 
      return name;
   } 

   public void setName(String _name) { 
      name = _name; 
   }

   public void addAttribute(String attrib) {
      if ( attributes.contains( attrib ) ) 
         return ; 
      Element ta =  doc.createElement( "TaskAttibute" ) ;    
      ta.setAttribute( "AttributeName" , attrib ) ; 
      attributes.add( attrib ) ; 
   }

   Set<String> getAttibutes() { 
      return attributes; 
   }

   Set<String> getSkills() { 
      return skills; 
   }

   public String getToolTip() { 
      String t = "" ; 
      for ( String s: attributes) {
         if (t.length() > 0 ) 
            t += ";"  ; 
         t += s ; 
      }
      return t; 
   }

   public JDialog getEditDialog() { 
      JDialog d = new ActivityDialog() ; 
      d.setVisible(true);
      return d; 
   }

   private class ActivityDialog extends JDialog implements ActionListener { 

      static final long serialVersionUID = -1697344298580538640L;

      private Set<String> attributes ; 

      private Set<String> skills ; 

      private Set<String> permissions ; 

      private JPanel attributesPanel ;    
      
      private JPanel skillsPanel; 

      private JPanel permissionPanel ; 
      
      private JButton save ;

      private JButton cancel;

      public void actionPerformed(ActionEvent event){
         Object source = event.getSource();
         if (source == save ) { 
            Activity.this.attributes = attributes ; 
            Activity.this.skills = skills ; 
            Activity.this.permissions = permissions ; 
                 //System.out.println( "Save clicked" ) ; 
                 
            dispose(); 
         }
         else { 
                 //System.out.println( "Cancel clicked" ) ; 
            dispose(); 
         }
      }

      public ActivityDialog() { 
         setName("Edit activity " + name) ; 

         setMinimumSize( new Dimension(50, 200) ) ; 

         attributes = new HashSet<String> (Activity.this.attributes) ; 
         skills = new HashSet<String> (Activity.this.skills); 
         permissions = new HashSet<String> (Activity.this.permissions); 

         Container contentPane  = getContentPane() ;
         contentPane.setLayout( new BorderLayout() );
              //JLabel label = new JLabel ("Edit Activity " + name);
              //contentPane.add(label, BorderLayout.NORTH);
         
         JTabbedPane tabbedPane = new JTabbedPane();
         attributesPanel = new ActivityPanel( "Data", attributes, this ) ; 
         tabbedPane.addTab("Data", attributesPanel);

         skillsPanel = new ActivityPanel( "Skills", skills, this ) ;  
         tabbedPane.addTab("Skills", skillsPanel );

         permissionPanel = new ActivityPanel("Authorizations", permissions, this) ; 
         tabbedPane.addTab("Authorizations", permissionPanel );
         contentPane.add(tabbedPane, BorderLayout.CENTER);

         JPanel buttonpanel = new JPanel();
         save = new JButton("Save") ;
         cancel = new JButton("Cancel") ;
         save.addActionListener(this);
         cancel.addActionListener(this);
         buttonpanel.add(save) ; 
         buttonpanel.add(cancel) ; 
         contentPane.add(buttonpanel, BorderLayout.SOUTH);
         pack();
      }
   } 


   private class ActivityPanel extends JPanel implements ActionListener { 
      
      static final long serialVersionUID = 2467737479287536337L;

      private static final int DEFAULT_NAME_LENGTH = 20; 

      private String name ; 
      
      private Set<String> attributes; 

      private JDialog parent; 

      private JButton addbutton ; 

      private JTextField additem; 

      private JPanel attribspanel ; 

      public void actionPerformed (ActionEvent event) {
         Object source = event.getSource();
         if (source == addbutton ) { 
            if ( attributes.contains( additem.getText() ) ) 
               return ; 
            attributes.add( additem.getText() ) ; 
            JLabel label = new JLabel(additem.getText());
            attribspanel.add(label);
            parent.pack(); 
               // clear text box for next time around
	    additem.setText(""); 
         }
      }

      public ActivityPanel(String _name,  Set<String> _attributes, JDialog _p) {
         name = _name; 
         attributes = _attributes;
         parent = _p; 
         setLayout(new GridLayout(0, 1));

         JLabel label = new JLabel(name);
         label.setHorizontalAlignment(JLabel.CENTER);
         add(label);

         attribspanel = new JPanel(); 
         attribspanel.setLayout(new BoxLayout(attribspanel, BoxLayout.PAGE_AXIS));
         add(attribspanel); 

         for( String s: attributes ) {
            JLabel l = new JLabel(s);
            attribspanel.add(l);
         }

         JPanel addpanel = new JPanel();
         addbutton = new JButton ("Add to " + name );
         addbutton.addActionListener(this) ; 
         addpanel.add(addbutton);

         additem = new JTextField(DEFAULT_NAME_LENGTH);
         addpanel.add(additem);
         add(addpanel);
      }
   }


}



// TODO image on vertex : 
// http://www.jgraph.org/forum/viewtopic.php?f=13&t=4123 


// misc 
      //StringWriter sw = new StringWriter();
      //new Throwable("").printStackTrace();
      //System.out.println(  sw.toString() ) ; 
      //return getHTMLTask() ; 