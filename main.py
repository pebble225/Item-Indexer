class ItemIndexer:
	def __init__(self, capacity = 100):
		self.capacity = capacity
		self.availableExternIds = [] # external ids will not change and are used to reference the same object until it's removed from the list
		self.internIds = [None] * capacity # internal ids will change if the objects in the list change their location to keep data together
		self.nextFreeSpace = 0 # this is used to add the next element to the end of the list. There should never be a gap in the list or this won't work
		self.items = [None] * capacity # this is where the objects are stored

		for i in range(0, capacity, 1):
			self.availableExternIds.append(i)
			self.internIds[i] = -1
	

	def AddItem(self, obj) -> int:
		if len(self.availableExternIds) == 0:
			print(f"ERROR Item Indexer {self} at full capacity. Unable to allocate new object.")
			return -1


		# get the next avaiable id from the list of avaiable ids and remove it from the list
		externID = self.availableExternIds[0]
		self.availableExternIds.pop(0)

		# the space this external id points to is free to use as a rule, so now this space is givin a value pointing to the next empty space at the bottom of all of the objects
		self.internIds[externID] = self.nextFreeSpace
		self.nextFreeSpace += 1

		# with all of this information the object is added to the new slot
		self.items[self.internIds[externID]] = obj

		# the externID is used to address and access this object under any context and this object shouldn't be accessed directly
		return externID

	def GetRemainingCapacity(self):
		return len(self.availableExternIds)

	def ViewItems(self, count):
		for i in range(0, count, 1):
			externID = ""
			freeSpace = ""

			if i >= len(self.availableExternIds):
				externID = "NULL"
			else:
				externID = self.availableExternIds[i]
			
			if i == self.nextFreeSpace:
				freeSpace = "  <<< Next Free Space"

			print("Index {0}:\tAvailableExtern: {1}\t\tInternID: {2}\t\tItem: {3}{4}".format(i, externID, self.internIds[i], self.items[i], freeSpace))
	

	def GetItem(self, id):
		return self.items[self.internIds[id]]


	def RemoveItem(self, id):
		lastObjectAddress = self.nextFreeSpace - 1 # the last object in the list might need to be swapped out. The internal id is extracted this way but not the external

		if id == lastObjectAddress:	# removing the last element is very simple so a unique case is made
			self.items[self.internIds[id]] = None # destroy the data stored there
			self.internIds[id] = -1 # destroy the internal id
		elif id < lastObjectAddress: # for other members of the list the object at the end of the list has to be swapped with the space being emptied
			targetID = -1 # target ID is the external id of the last object which is unknown. It is only known that it happens to be the last member of the item list

			for i in range(0, self.capacity, 1): # search each address until the external id matches and then store it
				if self.internIds[i] == lastObjectAddress:
					targetID = i
					i = self.capacity
			
			self.items[self.internIds[id]] = self.items[self.internIds[targetID]] # first the object is copied to the emptying location and the end of the list is cleared
			self.items[self.internIds[targetID]] = None

			self.internIds[targetID] = self.internIds[id] # second the internal ids are transferred and then reset
			self.internIds[id] = -1
		
		self.nextFreeSpace -= 1 # the sorted object has moved, so the space before is now cleared
		self.availableExternIds.append(id) # in either case mentioned above the external id is now ready to be used for a new object


def main():
	pass

if __name__ == "__main__":
	main()
