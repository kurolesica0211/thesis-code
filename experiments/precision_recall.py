

DIRECT_SYNONYMS = [
	("hasParent", "hasMother"),
	("hasParent", "hasFather"),
	("hasParent", "isDaughterOf"),
	("hasParent", "isSonOf"),
	("hasParent", "isChildOf"),

	("hasChild", "hasDaughter"),
	("hasChild", "hasSon"),
	("hasChild", "isFatherOf"),
	("hasChild", "isMotherOf"),
	("hasChild", "isParentOf"),
	
	("isSiblingOf", "isBrotherOf"),
	("isSiblingOf", "isSisterOf"),
	("isSiblingOf", "hasBrother"),
	("isSiblingOf", "hasSister"),
]

INVERSE_SYNONYMS = [
	("hasParent", "isParentOf"), ("isSiblingOf", "isSiblingOf")
]