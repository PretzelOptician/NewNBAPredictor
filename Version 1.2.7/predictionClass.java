import java.util.Scanner;

public class predictionClass {
	
	static double leaguePace = 98.1; 
	static double leagueFGA = 88.8;
	static double DRTGaverage = 0.0; 
	static double dConstant = 0.008; 
    static int homeScoreTotal = 0; 
    static int awayScoreTotal = 0;
	public static void main(String[] args) {
		double DRTGtotal = 0.0;
		double DRTGmax = 0; 
		for (int i=0; i<30; i++) {
		    double DRating = ReadExcelFileDemo.returnDouble(2+i, 11, "league"); 
			DRTGtotal += DRating;
			if(DRating > DRTGmax) {DRTGmax = DRating; }
		}
		DRTGaverage = DRTGtotal/30;
		//changing defensive rating average to be max: this should make defense more impactful; 
		//DRTGaverage = (DRTGmax+DRTGaverage)/2; 
		DRTGaverage = 0.67*DRTGaverage+0.33*DRTGmax; 
		leagueMain.setLeague(); 
		String team_home; 
		String team_away; 
		Scanner myObj = new Scanner(System.in); 
		System.out.println("Enter home team name: ");
		team_home = myObj.nextLine(); 
		System.out.println("Enter away team name: ");
		team_away = myObj.nextLine(); 
		//the main argument runs the possession method all of the times necessary. 
		//after this, make sure to run the games 4-7 times to get a series result. 
		//run that series 10,000 times to get the percentages
		//INCLUDE SOMETHING FOR OVERTIME
		//INCLUDE DEFENSIVE CONSTANT
		//this is the number of times the simulation runs
		int simulationNumber = 100000; 
		//int[] homeScores = new int[simulationNumber];
		//int[] awayScores = new int[simulationNumber];
		int homeWinTimes = 0;
		int awayWinTimes = 0; 
		String gameWinner = null;
		//this builds the home and away teams. 
        homeTeam.setName(team_home); 
        awayTeam.setName(team_away); 
        awayTeam.buildTeam(); 
        homeTeam.buildTeam(); 
        //check for injuries. 
        System.out.println("Are there any injured players? (y/n)"); 
        String response = myObj.nextLine(); 
        if(response == "y") {
            System.out.println("List the Rk on the spreadsheet of each injured HOME player. Type '$' when done. ");
            while(response != "$") {
                response = myObj.nextLine(); 
                //int injuredPlayer = (int) response;               can't cast this for some reason but just find a conversion method online. 
                //append to arraylist
            }
            /*
            for(x : injuredPlayers) {
                homeTeam.totalHomePlayers[x].setAvgMins(0.0); 
                System.out.println(homeTeam.totalHomePlayers[x].getName() + " has been taken out of the game!"); 
            }
            */
            System.out.println("List the Rk on the spreadsheet of each injured AWAY player. Type '$' when done. "); 
            //CLEAR THE ARRAYLIST
            while(response != "$") {
                response = myObj.nextLine(); 
                //int injuredPlayer = (int) response;               can't cast this for some reason but just find a conversion method online. 
                //append to arraylist
            }
            /*
            for(x : injuredPlayers) {
                awayTeam.totalHomePlayers[x].setAvgMins(0.0); 
                System.out.println(awayTeam.totalAwayPlayers[x].getName() + " has been taken out of the game!"); 
            }
            */
        }
		for(int k=0; k<simulationNumber; k++) {
			gameWinner = game(team_home, team_away);
			if (gameWinner.equalsIgnoreCase(team_home)) {
				homeWinTimes += 1; 
			}
			else if (gameWinner.equalsIgnoreCase(team_away)) {
				awayWinTimes += 1; 
			}
			System.out.println(", Game #" + Integer.toString(k));
		} 
		/*homeTeam.buildTeam(); 
		awayTeam.buildTeam(); 		for(int k=0; k<simulationNumber; k++) {
			int homeScore = 0; 
			int awayScore = 0; 
			for(int i=0; i<homePace; i++) {
				homeScore += homeTeam.possession(); 
			}
			for(int i=0; i<awayPace; i++) {
				awayScore += awayTeam.possession(); 
			}
			System.out.println("The home team has scored a total of " + Integer.toString(homeScore) + " points this game! Wow!");
			homeScores[k] = homeScore; 
			System.out.println("The away team has scored a total of " + Integer.toString(awayScore) + " points this game! Wow!"); 
			awayScores[k] = awayScore; 
		}
		int totalHomeScore = 0; 
		int totalAwayScore = 0; 
		for(int x=0; x<simulationNumber; x++) {
			totalHomeScore += homeScores[x];
			totalAwayScore += awayScores[x]; 
		}
		System.out.println("\nThe home team scored an average of " + Double.toString(totalHomeScore/simulationNumber) + " points!");
		System.out.println("The away team scored an average of " + Double.toString(totalAwayScore/simulationNumber) + " points!"); 
		for(int x=0; x<simulationNumber; x++) {
			if(homeScores[x] > awayScores[x]) {
				homeWinTimes += 1;  
			}
			else if(awayScores[x] > homeScores[x]) {
				awayWinTimes += 1;  
			}
		}*/
		System.out.println("The home team won the game " + Double.toString(100*homeWinTimes/(homeWinTimes+awayWinTimes))); 
		double homeAverage = homeScoreTotal/simulationNumber; 
		double awayAverage = awayScoreTotal/simulationNumber; 
		System.out.println("Spread is " + Double.toString((awayAverage-homeAverage)) + " to the home team.");
		System.out.println("The home team scored an average of " + homeAverage + " points and the away team scored an average of " + awayAverage + " points.");
		System.out.println("The predicted total is " + (homeAverage+awayAverage) + " points.");
	}
	
	public static double getLeaguePace() {
		return leaguePace; 
	}
	
	public static double getLeagueFGA() {
		return leagueFGA; 
	}
	
	public static double getLeagueDRTG() {
		return DRTGaverage; 
	}
	
	public static String game(String team_home, String team_away) {
		double homePace = homeTeam.getPace(); 
		double awayPace = awayTeam.getPace(); 
		int homeScore = 0; 
		int awayScore = 0; 
		for(int i=0; i<homePace; i++) {
		    int possessionScoreHome = homeTeam.possession();
			homeScore += possessionScoreHome; 
			homeScoreTotal += possessionScoreHome; 
		}
		for(int i=0; i<awayPace; i++) {
            int possessionScoreAway = awayTeam.possession();
            awayScore += possessionScoreAway; 
            awayScoreTotal += possessionScoreAway; 
		}
		//System.out.println("The home team has scored a total of " + Integer.toString(homeScore) + " points this game! Wow!");
		//System.out.println("The away team has scored a total of " + Integer.toString(awayScore) + " points this game! Wow!"); 
		System.out.print(team_home + " " + Integer.toString(homeScore) + " - " + Integer.toString(awayScore) + " " + team_away);
		if(homeScore>awayScore) {
			return team_home; 
		}
		else if (awayScore>homeScore) {
			return team_away;
		}
		else {
			return "Draw";
		}
	}
	}
