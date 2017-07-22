class SplitNode:
   'The object representing each split node'

   def __init__(self, data, usedSet, attributeToSplit, obtainedWithAttributeIndex, nodeName):
       # if we have a node obtained by splitting its parent with attribute on index i,
       # the we save "i" in 'obtainedWithAttributeIndex'. The node would then have
       # data containing one identical information across all entries; that piece of
       # information would then be the 'nodeName'.
      self.data = data
      self.usedSet = usedSet
      self.attributeToSplit = attributeToSplit
      self.obtainedWithAttributeIndex = obtainedWithAttributeIndex
      self.nodeName = nodeName
   