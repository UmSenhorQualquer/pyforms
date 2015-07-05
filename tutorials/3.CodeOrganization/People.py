import pickle


class People(object):


	def __init__(self):
		self._people = []


	def addPerson(self, person):
		self._people.append(person)

	def removePerson(self, index):
		return self._people.pop(index)

	def save(self, filename):
		output = open(filename, 'wb')
		pickle.dump(self._people, output)

	def load(self, filename):
		pkl_file = open(filename, 'rb')
		self._people = pickle.load(pkl_file)




if __name__ == "__main__":
	from Person import Person

	people = People()
	person = Person('Jack', '', 'Barrow')
	people.addPerson(person)
	people.save('people.dat')