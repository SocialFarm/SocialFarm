import net.sf.json.*; 
import net.sf.json.JSONArray; 
import net.sf.json.JSONObject; 
import net.sf.json.JSONSerializer;
import net.sf.json.util.CycleDetectionStrategy; 

import java.util.HashMap;
import java.util.Map; 
import java.util.ArrayList; 
import java.util.List;

class WorkFlowTranslator {

   public static String toJSON( Map<String, ? extends List<String>> input ) { 
      JSONObject obj = JSONObject.fromObject( input );  
      return obj.toString(); 
   }

   public static void main(String [] args) {
      List<String> list = new ArrayList<String> () ; 
      list.add( "www" ) ; 
      list.add( "aaa" ) ; 
      JSONArray jsonArray = JSONArray.fromObject( list );  
      System.out.println( jsonArray );  

      Map<String, List<String>> map = new HashMap<String, List<String>> (); 
      map.put( "taskA" , list ) ;
      System.out.println( toJSON(map) ) ;
   }

} 
