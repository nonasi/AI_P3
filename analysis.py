# analysis.py
# -----------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

######################
# ANALYSIS QUESTIONS #
######################

# Change these default values to obtain the specified policies through
# value iteration.

def question2():
  answerDiscount = 0.9
  answerNoise = 0.0
  return answerDiscount, answerNoise

def question3a():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = 0.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3b(): #make living reward sufficiently negative, then agent "prefers" closts exit.  COME BACK TO THIS
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = -3.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3c(): #default values
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = 0.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3d(): #raise the noise by a bit.  COME BACK TO THIS
  answerDiscount = 0.9
  answerNoise = 0.4
  answerLivingReward = 0.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3e(): #make the living reward 2 or greater, and agent will avoid exits
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = 2.0
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question6():
  answerEpsilon = None
  answerLearningRate = None
  return answerEpsilon, answerLearningRate
  # If not possible, return 'NOT POSSIBLE'
  
if __name__ == '__main__':
  print 'Answers to analysis questions:'
  import analysis
  for q in [q for q in dir(analysis) if q.startswith('question')]:
    response = getattr(analysis, q)()
    print '  Question %s:\t%s' % (q, str(response))
