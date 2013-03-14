# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
     
    "*** YOUR CODE HERE ***"
    
    
    #my code
    allStates = mdp.getStates()
    vPrimes = util.Counter() #  A Counter is a dict with default 0
    for s in allStates:
        self.values[s]=0
 
    i = 0
    while i < iterations:
        for s in allStates:
            if self.mdp.isTerminal(s):
                #self.values[s]=-self.mdp.getReward(s,None,None)
                vPrimes[s] = mdp.getReward(s, None, s)
                
                """
            elif s==self.mdp.getStartState():
                #self.values[s]=self.mdp.getReward(s,None,None)
                vPrimes[s] = mdp.getReward(s, None, s)
                """
            
            else:
                allActions=self.mdp.getPossibleActions(s)
                
                bestUtility=-999999
                for action in allActions:
                    statesReachable=self.mdp.getTransitionStatesAndProbs(s,action) #list of (nextState,prob) tuples
                    expectedUtility=0
                    for nsAndP in statesReachable:
                        expectedUtility=expectedUtility+nsAndP[1]*self.getValue(nsAndP[0])
                        
                    if expectedUtility>=bestUtility:
                        bestUtility=expectedUtility
                #self.values[s]=self.mdp.getReward(s,None,None)+discount*bestUtility
                vPrimes[s] = self.mdp.getReward(s,None,None)+discount*bestUtility
                
        for s in allStates:
            self.values[s] = vPrimes[s]
        i +=1
    
    
    """
    #nona's code
    allStates = mdp.getStates() 
    vPrimes = util.Counter() #  A Counter is a dict with default 0
    print "this is one of the states: ", allStates[1]
 
    rs = mdp.livingReward #living reward
    iteration = 0
    
    while iteration < iterations:
        
        #for s in allStates:
        #    self.values[s] = vPrimes[s]
        
        for s in allStates:
           print "this is current state: ", s 
           if mdp.isTerminal(s):
               vPrimes[s] = mdp.getReward(s, None, s);
           else: 
               sreward = mdp.getReward(s, None, s)
               vPrimes[s] = sreward + discount * self.utilOfBestAction(mdp, s )
               
        for s in allStates:
            self.values[s] = vPrimes[s]
            
        iteration +=1
    """

  def utilOfBestAction (self, mdp, s):
    possibleActions =  mdp.getPossibleActions(s) 
    import sys
    maxUtility = -sys.maxint-1 # equivalent to "-infinity"
    
    
    for action in possibleActions :
            
        transitionStatesAndProbs = mdp.getTransitionStatesAndProbs(s, action)
        
        utilityOfAction = self.getPUsumForGivenAction (mdp, transitionStatesAndProbs, s, action)
        print "utiliti of action: ", utilityOfAction
        if utilityOfAction >= maxUtility:
           maxUtility = utilityOfAction 
  
    return maxUtility
  
  """ transitionStatesAndProbs a list of (nextState, prob) pairs for a given state
  returns the sum of the probabilities and utilities of each action
  """
  def getPUsumForGivenAction (self, mdp, transitionStatesAndProbs,s, action):
    utilityOfAction = 0 
    for tsAndP in transitionStatesAndProbs:
        nextState = tsAndP[0]
        transitionProbability = tsAndP[1]
        print "this is next state: ", nextState 
        print "next state value:   ", self.values[nextState]
        print "transition prob: ", transitionProbability
        utilityOfAction += (transitionProbability * self.values[nextState]) # 
                
    return utilityOfAction
  
  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"
    #this method looks at all the neighboring states, 
    #then returns the action that attempts to goto the state with the highest utility
    
    if self.mdp.isTerminal(state):
        return None

    
    legalActions=self.mdp.getPossibleActions(state)
    
    maxValue=-999999999999
    bestAction = None
    for action in legalActions:
        statesReachable=self.mdp.getTransitionStatesAndProbs(state,action)
        
        expectedUtility=0
        for newstate in statesReachable:
            expectedUtility=expectedUtility+newstate[1]*self.getValue(newstate[0])
            """
            if newstate[1]>=1-self.mdp.noise:
                value=self.getValue(newstate[0])
                if value>maxValue:
                    maxValue=value
                    bestAction=action
            """
        if expectedUtility>maxValue:
            maxValue=expectedUtility
            bestAction=action
    
    return bestAction

    #util.raiseNotDefined()


  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
