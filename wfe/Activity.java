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




public class Activity extends mxCell implements Serializable
{
   static final long serialVersionUID = 4665261573913958775L;

   private Document doc = mxUtils.createDocument();

   private String name = null;

   private Set<String> attributes = new HashSet<String> () ; 
   
   private Set<String> skills = new HashSet<String> () ; 

   private Set<String> permissions = new HashSet<String> () ; 

	public Activity(String name)
	{
      super(name); 
      setName(name) ; 
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
                 /* 
            for( String attr : attributes ) 
               if( ! Activity.this.attributes.contains(attr) ) 
                  addAttribute(attr); 
            for( String s : skills ) 
               Activity.this.skills.add( s ) ; 
            for( String s : permissions ) 
               Activity.this.permissions.add( s ) ;             
                 */  
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




/* 
   public void addAttribute(String attrib, Set<String> permitted_roles) {
      if ( attributes.contains( attrib ) ) 
         return ; 
      Element ta =  doc.createElement( "TaskAttibute" ) ;    
      ta.setAttribute( "AttributeName" , attrib ) ; 
      attributes.add( attrib ) ; 
      if ( permitted_roles != null ) {
         ta.setAttribute( "Permissions" , permitted_roles.toString()  ) ; 
         accessors.put( attrib, new HashSet<String> (permitted_roles) ) ; 
      }
   }

 */

// http://www.jgraph.org/forum/viewtopic.php?f=13&t=4123 
