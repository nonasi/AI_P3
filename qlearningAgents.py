# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math
          
class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent
    
    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update
      
    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha   (learning rate)
      - self.gamma   (discount rate)
    
    Functions you should use
      - self.getLegalActions(state) 
        returns legal actions
        for a state
  """
  def __init__(self, **args):
    "You can initialize Q-values here..."
    ReinforcementAgent.__init__(self, **args)

    "*** YOUR CODE HERE ***"
    self.qValues = util.Counter() #q values are initialized here.
    #self.seenqv = util.Counter() #seenqv[sa] = 1 iff qValues[sa] seen, 0 otherwise
    
    self.freq=util.Counter()
    
    self.r=0
        
    
  
  def getQValue(self, state, action):
    """
      Returns Q(state,action)    
      Should return 0.0 if we never seen
      a state or (state,action) tuple 
    """
    "*** YOUR CODE HERE ***"
    sa = (state, action)
    #print "Qvalue: state ", state,         "action      ", action
    #print "last state:   ", self.lastState, "last action ", self.lastAction
    #print "self.qValues before " , self.qValues[sa], " and self.seenqv ", self.seenqv[sa]
    
    """
    if self.seenqv[sa] == 0: #we have never seen sa before 
        self.seenqv[sa] = 1 #mark that we just saw it.
        self.qValues[sa] = 0; 
        #print "self.qValues 1st time" , self.qValues[sa]
        return self.qValues[sa]
    
    elif self.seenqv[sa] != 0: 
        #print "self.qValues more than 2 times" , self.qValues[sa]
        return self.qValues[sa]
    """
    return self.qValues[sa]
  
    
  def getValue(self, state):
    """
      Returns max_action Q(state,action)        
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
      My Notes: we should return the VALUE of the action which 
      has the greatest Q-value
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    print "getValue start "
    legalActions = self.getLegalActions(state)
    if len(legalActions)<1:
        return 0.0
    
    else: 
        maxAction = -sys.maxint -1 #"-infinity"
        #get the greatest qValue among the possible state-action pairs
        for curAction in legalActions:
            sa = (state, curAction)
            if maxAction <= self.getQValue(state, curAction):
                maxAction = self.getQValue(state, curAction)
        
        print "getValue end - MaxAction = ", maxAction    
        return maxAction
    
  def getPolicy(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    "*** YOUR CODE HERE ***"
    print"getPolicy"
    legalActions = self.getLegalActions(state)
    bestAction = None
    maxQvalue = -sys.maxint -1
    for a in legalActions:
        
        if maxQvalue <=  self.getQValue(state, a):
            maxQvalue = self.getQValue(state, a)
            bestAction = a
    return bestAction
    
  def getAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.
    
      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """  
    # Pick Action
    legalActions = self.getLegalActions(state)
    action = None
    "*** YOUR CODE HERE ***"
    if len(legalActions) < 1: 
        return None
    else:
        randomAction = util.flipCoin(self.epsilon) #epsilon = prob of true; 1-epsilon = prob false
        if randomAction: 
            action = random.choice(legalActions)
        else:
            action = self.getPolicy(state)
            print "epsilon: ", self.epsilon, "coin flip: ", randomAction
        return action
    #util.raiseNotDefined()
  
  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a 
      state = action => nextState and reward transition.
      You should do your Q-Value update here
      
      NOTE: You should never call this function,
      it will be called on your behalf
    """
    "*** YOUR CODE HERE ***"
    print "update"
    print "reward: ", reward
    stateActions=self.getLegalActions(state)
    
    sa=(state,action)
    
    if stateActions[0]=="exit":
        self.qValues[sa] = reward
    else:
    #if stateActions[0]!="exit":
        self.freq[sa]=self.freq[sa]+1
        self.qValues[sa]=self.qValues[sa]+self.alpha*(self.r+self.gamma*self.getValue(nextState) - self.qValues[sa])
        #(self.freq[sa])*
    action = self.getAction(nextState)
    self.r=reward
    
    return action
    #util.raiseNotDefined()
    
class PacmanQAgent(QLearningAgent):
  "Exactly the same as QLearningAgent, but with different default parameters"
  
  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1
    
    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action

    
class ApproximateQAgent(PacmanQAgent):
  """
     ApproximateQLearningAgent
     
     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)

    # You might want to initialize weights here.
    "*** YOUR CODE HERE ***"
    
  def getQValue(self, state, action):
    """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
    
  def update(self, state, action, nextState, reward):
    """
       Should update your weights based on transition  
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
    
  def final(self, state):
    "Called at the end of each game."
    # call the super-class final method
    PacmanQAgent.final(self, state)
    
    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      # you might want to print your weights here for debugging
      "*** YOUR CODE HERE ***"
      pass
