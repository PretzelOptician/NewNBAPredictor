public class awayTeam {
	public static void main(String[] args) {
		awayTeam.buildTeam(); 
		for(int k=0; k<5; k++) {
			System.out.println("This possession produced " + Integer.toString(possession()) + " points! \n"); 
		}
		
	}
	
	static double pace = 0; 
	static String teamName;
	static double teamDRTG = 0; 
	static awayPlayer[] totalAwayPlayers = new awayPlayer[13];
	static awayPlayer[] awayPlayersOnCourt = new awayPlayer[5]; 

	public static void setName(String name) {
		teamName = name; 
	}
	
	static void buildTeam() {
		pace = leagueMain.getTeamPace(teamName); 
		teamDRTG = -predictionClass.dConstant*(leagueMain.getTeamDRTG(teamName) - predictionClass.DRTGaverage);
		//if the defense is bad, it shouldn't affect as much 
        if(teamDRTG < 0) {
            teamDRTG /= 2.5; 
        }
        //if the defense is TOO GOOD, make it a bit less impactful
        if(teamDRTG > 0 && leagueMain.getTeamDRTG(teamName) - predictionClass.DRTGaverage < -2.5) {
            teamDRTG = -predictionClass.dConstant*(-2.5) + predictionClass.dConstant*(leagueMain.getTeamDRTG(teamName) - predictionClass.DRTGaverage + 2.5)/3;
        }
		for(int k=0; k<13; k++) {
			totalAwayPlayers[k] = new awayPlayer(k, teamName.toLowerCase()); 
		}
	}
	
	static double getPace() {
		return pace; 
	}

	public static void buildTeamOnFloor(Object[] awayPlayersOnCourt) {
		double totalMinutes = 0; 
		//decide which players are on the court: 
		for(int i=0; i<13; i++) {
			totalMinutes += totalAwayPlayers[i].getAvgMins();
		}
		int n = 0; 
		while(n<5) {
			for(int k=0; k<13; k++) {
				if((n<5) && (java.util.Arrays.asList(awayPlayersOnCourt).contains(totalAwayPlayers[k])) == false) {
					double playTimeShare = (totalAwayPlayers[k].getAvgMins())/(totalMinutes); 
					if (playTimeShare>Math.random()) {
						awayPlayersOnCourt[n] = totalAwayPlayers[k]; 
						n+=1; 
					}
				}
			} 
		}
		
	}
	
	public static int takeShot(int startingPoints) {
	//run a possession: 
		homePlayer[] defensivePlayersOnCourt = new homePlayer[5]; 
		homeTeam.buildTeamOnFloor(defensivePlayersOnCourt);
		//simulate potential turnover:
		for(int i=0; i<5; i++) {
			if(awayPlayersOnCourt[i].getTurnoverRate()>(awayTeam.getPace()*Math.random())) {return 0;}
		}
		//simulate potential steal: 
		for(int i=0; i<5; i++) {
			if(defensivePlayersOnCourt[i].getstealRate()>Math.random()*predictionClass.getLeaguePace()) {return 0;}
		}
		//decide who takes the shot: 
			//find total fgA
		double totalfgA = 0; 
		for(int i=0; i<5; i++) {
			totalfgA += awayPlayersOnCourt[i].getfgA(); 
		}
			//decide who takes shot
		int shotTakerID = -1; 
		while(shotTakerID == -1) {
			for(int i=0; i<5; i++) {
				if((shotTakerID == -1) && ((awayPlayersOnCourt[i].getfgA()/totalfgA)>Math.random())) {
					shotTakerID = i; 
				}
			}
		}
			//announces player who took shot
		//("\n" + awayPlayersOnCourt[shotTakerID].getName() + " takes the shot!"); 
		//decides what type of shot it is
		int shotType = 0; 
			//shot type of 1 is a free throw, shot type of 2 is a two point attempt, shot type of 3 is a three point attempt. 
			//need to take 2.2ish free throw attempts per ft possession to account for and 1s.
		double shotAttemptDenominator = (awayPlayersOnCourt[shotTakerID].ftA/2.2) + awayPlayersOnCourt[shotTakerID].twoPA + awayPlayersOnCourt[shotTakerID].threePA;
		//System.out.println("He has total shot attempts of " + Double.toString(shotAttemptDenominator) + " per game.");
			//uses probability to figure out what shot will be taken
		while(shotType == 0) {
			if(shotType==0 && (awayPlayersOnCourt[shotTakerID].getftA()/2.2)/shotAttemptDenominator > Math.random()) {shotType = 1;}
			if(shotType==0 && (awayPlayersOnCourt[shotTakerID].getTwoPA())/shotAttemptDenominator > Math.random()) {shotType = 2;}
			if(shotType==0 && (awayPlayersOnCourt[shotTakerID].getThreePA())/shotAttemptDenominator > Math.random()) {shotType = 3;} 
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
			shotProbability = awayPlayersOnCourt[shotTakerID].getftPercent(); 
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
				if((assist==false) && (awayPlayersOnCourt[k].getassistRate()/totalfgA > Math.random()) && (k!=shotTakerID)) {
					assist = true; 
					//System.out.println(awayPlayersOnCourt[k].getName() + " is assisting on this shot!"); 
				}
			}
			if(shotType==2) {
				//get shooting percentage
				shotProbability = awayPlayersOnCourt[shotTakerID].getTwoScorePercent();
				//adjust base percentage to be lower if not assisted. 
                shotProbability -= 0.0571; 
				//account for assist
				if(assist == true) {
					shotProbability += 0.0957; 
				}
				//account for opposing drtg
				shotProbability -= homeTeam.teamDRTG; 
				//System.out.println("A percentage of " + homeTeam.teamDRTG + " was removed for the opposing team's defense!");
				//make
				if(shotProbability>Math.random()) {pointsScored += 2;}
				//miss
				else {}
			}
			//for three pointers
			if(shotType==3) {
				//get shooting percentage
				shotProbability = awayPlayersOnCourt[shotTakerID].getThreeScorePercent();
				//adjust base percentage to be lower if not assisted. 
                shotProbability -= 0.0299; 
				//account for assist
				if(assist == true) {
					shotProbability += 0.05; 
				}
				//account for opposing drtg
				shotProbability -= homeTeam.teamDRTG; 
				//System.out.println("A percentage of " + homeTeam.teamDRTG + " was removed for the opposing team's defense!");
				//make
				if(shotProbability>Math.random()) {pointsScored += 3;}
				//miss
				//else {System.out.println(awayPlayersOnCourt[shotTakerID].getName() + " has missed the three pointer with a probability of " + Double.toString(100*shotProbability) + "%!");}
			}
		}
		//System.out.println(awayPlayersOnCourt[shotTakerID].getName() + " has scored " + Integer.toString(pointsScored) + " this possession!");  
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
				totalReboundingOnFloor += awayPlayersOnCourt[i].getDREB(); 
			}
			//System.out.println("Total rebounding on floor: " + Double.toString(totalReboundingOnFloor)); 
			boolean reboundDecided = false; 
			while(reboundDecided == false) {
				for(int i=0; i<5; i++) {
					if((reboundDecided == false) && ((defensivePlayersOnCourt[i].getDREB()/totalReboundingOnFloor)>Math.random())) {reboundDecided = true; offensiveRebound = false; break;}
					if((reboundDecided == false) && ((awayPlayersOnCourt[i].getOREB()/totalReboundingOnFloor)>Math.random())) {reboundDecided = true; offensiveRebound = true; break;}
				}
			}
			if(offensiveRebound) {pointsScored += takeShot(pointsScored);}
		}
		return pointsScored; 
	}
	
	//this method runs one possession
	public static int possession() {
		//builds the lineup actually on the floor
		awayTeam.buildTeamOnFloor(awayPlayersOnCourt); 
		//runs the method to take one shot and returns the points scored
		int pointsScored = awayTeam.takeShot(0); 
		//returns pointsscored to the main function
		return pointsScored; 
	}
}
