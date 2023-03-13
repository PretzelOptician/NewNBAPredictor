
public class leagueMain {
	
	static String[] teamNames = new String[30]; 
	public static void main(String[] args) {
		setLeague(); 
	}
	
	public static double getTeamPace(String teamName) {
		double pace = 0.0; 
		for(int k=0; k<30; k++) {
			if(teamNames[k].equalsIgnoreCase(teamName)) {
				pace = ReadExcelFileDemo.returnDouble(2+k, 13, "league");
				break; 
			}
		}
		return pace; 
	}
	
	public static double getTeamDRTG(String teamName) {
		double drtg = 0.0; 
		for(int k=0; k<30; k++) {
			if(teamNames[k].equalsIgnoreCase(teamName)) {
				drtg = ReadExcelFileDemo.returnDouble(2+k, 11, "league");
				break; 
			}
		}
		return drtg; 
	}
	
	public static void setLeague() {
		String theTeamName; 
		for(int k=0; k<30; k++) {
			theTeamName = ReadExcelFileDemo.returnString(2+k, 1, "league"); 
			String[] array1 = theTeamName.split(" "); 
			teamNames[k] = array1[array1.length-1]; 
			teamNames[k] = teamNames[k].replace("*", ""); 
		}
	}
}
