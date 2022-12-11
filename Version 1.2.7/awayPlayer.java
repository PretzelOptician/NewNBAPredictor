
public class awayPlayer {
	String name;
	double fgA; 
	double twoPA; 
	double threePA; 
	double twoScorePercent; 
	double threeScorePercent; 
	double avgMins; 
	double ftA; 
	double ftPercent; 
	double OREB; 
	double DREB; 
	double assistRate; 
	double stealRate; 
	double blockRate; 
	double turnoverRate; 
	double pf; 
	
	public awayPlayer(int rowNumber, String teamName) {
		setName(ReadExcelFileDemo.returnString(rowNumber+1, 1, teamName));
		setfgA(ReadExcelFileDemo.returnDouble(rowNumber+1, 7, teamName));  
		setTwoPA(ReadExcelFileDemo.returnDouble(rowNumber+1, 13, teamName));  
		setThreePA(ReadExcelFileDemo.returnDouble(rowNumber+1, 10, teamName)); 
		setTwoScorePercent(ReadExcelFileDemo.returnDouble(rowNumber+1, 14, teamName)); 
		setThreeScorePercent(ReadExcelFileDemo.returnDouble(rowNumber+1, 11, teamName)); 
		setAvgMins(ReadExcelFileDemo.returnDouble(rowNumber+1, 5, teamName)); 
		setftA(ReadExcelFileDemo.returnDouble(rowNumber+1, 17, teamName)); 
		setftPercent(ReadExcelFileDemo.returnDouble(rowNumber+1, 18, teamName)); 
		setOREB(ReadExcelFileDemo.returnDouble(rowNumber+1, 20, teamName)); 
		setDREB(ReadExcelFileDemo.returnDouble(rowNumber+1, 21, teamName)); 
		setassistRate(ReadExcelFileDemo.returnDouble(rowNumber+1, 22, teamName)); 
		setstealRate(ReadExcelFileDemo.returnDouble(rowNumber+1, 23, teamName)); 
		setblockRate(ReadExcelFileDemo.returnDouble(rowNumber+1, 24, teamName));
		setTurnoverRate(ReadExcelFileDemo.returnDouble(rowNumber+1, 25, teamName)); 
		setpf(ReadExcelFileDemo.returnDouble(rowNumber+1, 26, teamName)); 
	}
	
	public void setName(String name) {this.name = name;}
	public String getName() {return name;}
	public void setfgA(double fgA) {this.fgA = fgA;}
	public double getfgA() {return fgA;} 
	public double getTwoPA() {return twoPA;} 
	public void setTwoPA(double twoPA) {this.twoPA = twoPA;}
	public double getThreePA() {return threePA;} 
	public void setThreePA(double threePA) {this.threePA = threePA;}
	public double getTwoScorePercent() {return twoScorePercent;} 
	public void setTwoScorePercent(double twoScorePercent) {this.twoScorePercent = twoScorePercent;}
	public double getThreeScorePercent() {return threeScorePercent;}
	public void setThreeScorePercent(double threeScorePercent) {this.threeScorePercent = threeScorePercent;}
	public double getAvgMins() {return avgMins;}
	public void setAvgMins(double avgMins) {this.avgMins = avgMins;}
	public double getftA() {return ftA;}
	public void setftA(double ftA) {this.ftA = ftA;}
	public double getftPercent() {return ftPercent;}
	public void setftPercent(double ftPercent) {this.ftPercent = ftPercent;}
	public double getOREB() {return OREB;}
	public void setOREB(double OREB) {this.OREB = OREB;}
	public double getDREB() {return DREB;}
	public void setDREB(double DREB) {this.DREB = DREB;}
	public double getassistRate() {return assistRate;}
	public void setassistRate(double assistRate) {this.assistRate = assistRate;}
	public double getstealRate() {return stealRate;}
	public void setstealRate(double stealRate) {this.stealRate = stealRate;}
	public double getblockRate() {return blockRate;}
	public void setblockRate(double blockRate) {this.blockRate = blockRate;}
	public double getTurnoverRate() {return turnoverRate;}
	public void setTurnoverRate(double turnoverRate) {this.turnoverRate = turnoverRate;}
	public double getpf() {return pf;}
	public void setpf(double pf) {this.pf = pf;}
}
