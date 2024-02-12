import json
import random

class LearningSystem(object):
	"""
	Set up a learning system class, i.e., the approach you will apply.
	Feel free to create any functions under the class.

	Two functions are REQUIRED:
	- LearningSystem.fit(train_set, train_labels)
	- LearningSystem.predict(instance)
	"""

	def __init__(self):
		"""
		You can have any other parameters here.
		"""
		self.model = Cobweb()


	def fit(self, train_set, train_labels):
		"""
		Train the system with this function.
		Do NOT set any local variable other than train_set and train_labels for this function.
		========
		train_data: training data without labels. It should be a list of dictionaries.
		train_labels: A list of labels of training data. Each label has the same index as its data in train_data.
					  All labels are binary (0, 1).
		"""
		for instance, label in zip(train_set, train_labels):
			self.model.train(instance, label)


	def predict(self, instance):
		"""
		Predict the label of an instance (a single dictionary) given.
		"""
		return self.model.classify(instance)


class Cobweb(object):
    def __init__(self):
        self.tree = None

    def train(self, instance, label):
        # Train the Cobweb model with an instance and its label
        if self.tree is None:
            self.tree = CobwebNode(instance, label)
        else:
            self.tree.train(instance, label)

    def classify(self, instance):
        # Classify an instance using the Cobweb model
        if self.tree is not None:
            return self.tree.classify(instance)
        else:
            return 0  # Default to edible if the model is not trained

class CobwebNode(object):
    def __init__(self, instance, label):
        self.instance = instance
        self.label = label
        self.children = {}

    def train(self, instance, label):
        # Train the Cobweb node with an instance and its label
        common_attrs = set(self.instance.keys()) & set(instance.keys())

        if not common_attrs:
            # No common attributes, create a new child node
            self.children[instance] = CobwebNode(instance, label)
        else:
            # Find the best attribute match
            best_match = max(common_attrs, key=lambda attr: self.similarity(instance[attr], self.instance[attr]))

            if instance[best_match] not in self.children:
                self.children[instance[best_match]] = CobwebNode(instance, label)
            else:
                self.children[instance[best_match]].train(instance, label)

    def classify(self, instance):
        if not self.children:
            return self.label

        common_attrs = set(self.instance.keys()) & set(instance.keys())

        if not common_attrs:
            # No common attributes, return the majority label among children
            child_labels = [child.label for child in self.children.values()]
            return max(set(child_labels), key=child_labels.count)
        else:
            # Find the best attribute match
            best_match = max(common_attrs, key=lambda attr: self.similarity(instance[attr], self.instance[attr]))

            if instance[best_match] in self.children:
                return self.children[instance[best_match]].classify(instance)
            else:
                # No matching child, return the majority label among children
                child_labels = [child.label for child in self.children.values()]
                return max(set(child_labels), key=child_labels.count)

    def similarity(self, value1, value2):
        return 1 if value1 == value2 else 0

# Then you need to make the separate define_model() function,
# so you can have any initialized parameter defined.
# Autograder will define the model object based on your define_model() function.
def define_model():
	return LearningSystem()


"""
The following codes are for testing with sample data only.
REMEMBER TO REMOVE THEM BEFORE SUBMISSION.
=============================================================================
In this homework, a sample collection of shuffled data is provided.
You might try with the data provided like in the following before submission:
"""

def test(model, test_set_data, test_labels):
	correct = 0
	for i in range(len(test_set_data)):
		pred = model.predict(test_set_data[i])
		if pred == test_labels[i]:
			correct += 1
	accuracy = correct / len(test_set_data)
	return accuracy

sample_set_data = json.load(open('hw3-sample_set_data.json'))
sample_set_labels = json.load(open('hw3-sample_set_labels.json'))

train_set = sample_set_data[:-500]
train_labels = sample_set_labels[:-500]
test_set = sample_set_data[-500:]
test_labels = sample_set_labels[-500:]

model = define_model()
model.fit(train_set, train_labels)
print("Accuracy:", test(model, test_set, test_labels))




