public class homeTeam{
	public static void main(String[] args) {
		leagueMain.setLeague(); 
		awayTeam.buildTeam(); 
		homeTeam.buildTeam(); 
		for(int k=0; k<5; k++) {
			System.out.println("This possession produced " + Integer.toString(possession()) + " points! \n"); 
		}
		
	}
	static double pace = 101.7; 
	static String teamName;
	static double teamDRTG; 
	static homePlayer[] totalHomePlayers = new homePlayer[13];
	static homePlayer[] homePlayersOnCourt = new homePlayer[5]; 

	public static void setName(String name) {
		teamName = name; 
	}
	
	static void buildTeam() {
		pace = leagueMain.getTeamPace(teamName); 
		teamDRTG = -predictionClass.dConstant*(leagueMain.getTeamDRTG(teamName) - predictionClass.DRTGaverage);
		//if the defense is bad, it shouldn't affect as much 
		//if(teamDRTG < 0) {
		    //teamDRTG /= 2.5; 
		//}
		//if the defense is TOO GOOD, make it a bit less impactful
		//if(teamDRTG > 0 && leagueMain.getTeamDRTG(teamName) - predictionClass.DRTGaverage < -2.5) {
		    //teamDRTG = -predictionClass.dConstant*(-2.5) + predictionClass.dConstant*(leagueMain.getTeamDRTG(teamName) - predictionClass.DRTGaverage + 2.5)/3;
		//}
		for(int k=0; k<13; k++) {
			totalHomePlayers[k] = new homePlayer(k, teamName); 
		}
	}
	
	static double getPace() {
		return pace; 
	}

	public static void buildTeamOnFloor(Object[] homePlayersOnCourt) {
		double totalMinutes = 0; 
		//decide which players are on the court: 
		for(int i=0; i<13; i++) {
			totalMinutes += totalHomePlayers[i].getAvgMins();
		}
		int n = 0; 
		while(n<5) {
			for(int k=0; k<13; k++) {
				if((n<5) && (java.util.Arrays.asList(homePlayersOnCourt).contains(totalHomePlayers[k])) == false) {
					double playTimeShare = (totalHomePlayers[k].getAvgMins())/(totalMinutes); 
					if (playTimeShare>Math.random()) {
						homePlayersOnCourt[n] = totalHomePlayers[k]; 
						n+=1; 
					}
				}
			} 
		}
		//System.out.println("\n");
		for(int k=0; k<5; k++) {
			//System.out.println(((homePlayer) homePlayersOnCourt[k]).getName());
		}
	}
	
	public static int takeShot(int startingPoints) {
	//run a possession: 
		awayPlayer[] defensivePlayersOnCourt = new awayPlayer[5]; 
		awayTeam.buildTeamOnFloor(defensivePlayersOnCourt);
		//simulate potential turnover:
		for(int i=0; i<5; i++) {
			if(homePlayersOnCourt[i].getTurnoverRate()>(homeTeam.getPace()*Math.random())) {
			    //System.out.println(homePlayersOnCourt[i].getName() + " has turned over the ball!"); 
			    return 0;}
		}
		//simulate potential steal: 
		for(int i=0; i<5; i++) {
			if(defensivePlayersOnCourt[i].getstealRate()>Math.random()*predictionClass.getLeaguePace()) {
			    //System.out.println(defensivePlayersOnCourt[i].getName() + " has stolen the ball!"); 
			    return 0;}
		}
		//decide who takes the shot: 
			//find total fgA
		double totalfgA = 0; 
		for(int i=0; i<5; i++) {
			totalfgA += homePlayersOnCourt[i].getfgA(); 
		}
			//decide who takes shot
		int shotTakerID = -1; 
		while(shotTakerID == -1) {
			for(int i=0; i<5; i++) {
				if((shotTakerID == -1) && ((homePlayersOnCourt[i].getfgA()/totalfgA)>Math.random())) {
					shotTakerID = i; 
				}
			}
		}
			//announces player who took shot
		//System.out.println("\n" + homePlayersOnCourt[shotTakerID].getName() + " takes the shot!"); 
		//decides what type of shot it is
		int shotType = 0; 
			//shot type of 1 is a free throw, shot type of 2 is a two point attempt, shot type of 3 is a three point attempt. 
			//need to take 2.2ish free throw attempts per ft possession to account for and 1s.
		double shotAttemptDenominator = (homePlayersOnCourt[shotTakerID].ftA/2.2) + homePlayersOnCourt[shotTakerID].twoPA + homePlayersOnCourt[shotTakerID].threePA;
		//System.out.println("He has total shot attempts of " + Double.toString(shotAttemptDenominator) + " per game.");
			//uses probability to figure out what shot will be taken
		while(shotType == 0) {
			if(shotType==0 && (homePlayersOnCourt[shotTakerID].getftA()/2.2)/shotAttemptDenominator > Math.random()) {shotType = 1;}
			if(shotType==0 && (homePlayersOnCourt[shotTakerID].getTwoPA())/shotAttemptDenominator > Math.random()) {shotType = 2;}
			if(shotType==0 && (homePlayersOnCourt[shotTakerID].getThreePA())/shotAttemptDenominator > Math.random()) {shotType = 3;} 
		}
		//figures out the probability of hitting the shot
		double shotProbability = 0; 
		//creates variable for points scored on this possession
		int pointsScored = startingPoints; 
		//creates variable for if last free throw was missed
		boolean missedLastFreeThrow = false; 
		//for free throws
		if(shotType==1) {
			//takes the player's free throw percentage
			shotProbability = homePlayersOnCourt[shotTakerID].getftPercent(); 
			//this for loop ensures that two free throws are taken
			for(int i=0; i<2; i++) {
				//they make the shot
				if(shotProbability>Math.random()) {pointsScored += 1;}
				//if they miss the shot and its the second free throw, then the ball is reboundable
				else if(i==1) {missedLastFreeThrow = true;}
				//this is for the first missed free throw. it has no effect other than not earning a point for the team. 
				else {}
			}
			//there is a 20% chance that the possession will award a third free throw. in terms of accurate prediction models, this makes no sense. but i needed some way to account for and ones, which slightly raise the average free throws taken per possession, so i included this. i could include and ones in other possessions like expected, but there's no statistic for and ones per game, so i'll have to kind of BS it. 
			if(0.2>Math.random()) {
				//this makes it so that the second free throw, even if it missed, wasn't the last free throw and the ball was not reboundable
				missedLastFreeThrow = false; 
				//System.out.println("There is an extra free throw because of an and one!");
				//this is for make
				if(shotProbability>Math.random()) {pointsScored += 1;}
				//this is for miss
				else {missedLastFreeThrow = true;}	
			}
		}
		boolean canRebound = false;
		boolean blockedShot = false; 
		//blocked shot
		for(int i=0; i<5; i++) {
			if(blockedShot==false && defensivePlayersOnCourt[i].getblockRate()>Math.random()*predictionClass.getLeagueFGA()) {
				//System.out.println("The shot has been blocked by " + defensivePlayersOnCourt[i].getName() + "!");
				canRebound = true; 
				blockedShot = true; 
				//System.out.println("This ball is reboundable!\n");
			}
		}
		if(blockedShot == false) {
			//this part determines assist. 
			boolean assist = false; 
			for(int k=0; k<5; k++) {
				if((assist==false) && (k != shotTakerID) && (homePlayersOnCourt[k].getassistRate()/totalfgA > Math.random())  && (k!=shotTakerID)) {
					assist = true; 
					//System.out.println(homePlayersOnCourt[k].getName() + " is assisting on this shot!"); 
				}
			}
			if(shotType==2) {
				//get shooting percentage
				shotProbability = homePlayersOnCourt[shotTakerID].getTwoScorePercent();
				//adjust base percentage to be lower if not assisted. 
				shotProbability -= 0.0571; 
				//account for assist
				if(assist == true) {
					shotProbability += 0.0957; 
					//on average, this will produce the average shot % for the player, since the average assist rate is about 59.7%.
				}
				//account for opposing drtg
				shotProbability -= awayTeam.teamDRTG; 
				//System.out.println("After accounting for defense, the new shot probability is " + shotProbability);
				//make
				if(shotProbability>Math.random()) {pointsScored += 2;}
				//miss
				else {}
			}
			//for three pointers
			if(shotType==3) {
				//get shooting percentage
				shotProbability = homePlayersOnCourt[shotTakerID].getThreeScorePercent();
				//adjust base percentage to be lower if not assisted. 
                shotProbability -= 0.0299; 
				//account for assist
				if(assist == true) {
					shotProbability += 0.05; 
					//System.out.println("5% added for assist!");
				}
				//account for opposing drtg
				shotProbability -= awayTeam.teamDRTG; 
				//System.out.println("After accounting for defense, the new shot probability is " + shotProbability);
				//make
				if(shotProbability>Math.random()) {pointsScored += 3;}
				//miss
				else {}
			}
		}
		//System.out.println(homePlayersOnCourt[shotTakerID].getName() + " has scored " + Integer.toString(pointsScored) + " this possession!");  
		//note: need to separate parameter from variable. the way it is now, if points were scored earlier in the possession and there was a rebound, it is impossible to have a second rebound. 
		if(pointsScored==0 || missedLastFreeThrow) {
			canRebound = true; 
			//System.out.println("This ball is reboundable!\n");
		}
		if(canRebound) {
			//include calculation for seeing whether a team gets on offensive rebound or not. if they do, run and return pointsScored from takeShot(pointsScored).
			boolean offensiveRebound = false; 
			double totalReboundingOnFloor = 0;
			for(int i=0; i<5; i++) {
				totalReboundingOnFloor += defensivePlayersOnCourt[i].getDREB(); 
				totalReboundingOnFloor += homePlayersOnCourt[i].getDREB(); 
			}
			//System.out.println("Total rebounding on floor: " + Double.toString(totalReboundingOnFloor)); 
			boolean reboundDecided = false; 
			while(reboundDecided == false) {
				for(int i=0; i<5; i++) {
					if((reboundDecided == false) && ((defensivePlayersOnCourt[i].getDREB()/totalReboundingOnFloor)>Math.random())) {reboundDecided = true; offensiveRebound = false; break;}
					if((reboundDecided == false) && ((homePlayersOnCourt[i].getOREB()/totalReboundingOnFloor)>Math.random())) {reboundDecided = true; offensiveRebound = true; break;}
				}
			}
			if(offensiveRebound) {pointsScored += takeShot(pointsScored);}
		}
		return pointsScored; 
	}
	
	//this method runs one possession
	public static int possession() {
		//builds the lineup actually on the floor
		homeTeam.buildTeamOnFloor(homePlayersOnCourt); 
		//runs the method to take one shot and returns the points scored
		int pointsScored = homeTeam.takeShot(0); 
		//returns pointsscored to the main function
		return pointsScored; 
	}
}
