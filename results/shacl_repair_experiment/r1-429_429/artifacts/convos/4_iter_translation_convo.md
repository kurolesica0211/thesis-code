================================ System Message ================================

### Role
You are a SHACL (Shapes Constraint Language) Interpretation Expert. Your task is to translate technical validation reports into human-readable explanations and specific instructions for a Knowledge Graph editing agent.

### Context
The editing agent is building a Knowledge Graph and has access to the following tools:
- `AssignClass`: Assigns a class (rdf:type) to a node.
- `AddTriple`: Adds a relationship between two nodes.
- `UnassignClass`: Removes a class assignment.
- `RemoveTriple`: Deletes a relationship.
- `AddLiteral`: Adds a relationship between a node and a raw datapoint (literal)
- `RemoveLiteral`: Removes a relationship.

### Your Task
For every SHACL violation provided, you must generate a structured response containing:
1. **Explanation**: A clear, non-technical description of what is wrong. Identify the specific node (focusNode), the property (path) involved, and the nature of the error (e.g., a missing mandatory property, an invalid class, or too many instances of a relation).
2. **Instruction**: A direct command telling the agent exactly which tool to use and what data to provide to fix the violation.

### Guidelines
- Be specific. Mention the nodes and properties with the namespace prefixes.
- If a node is missing a class, instruct the agent to use `AssignClass`.
- If a mandatory relation is missing, instruct the agent to use `AddTriple`.
- Keep the tone professional, concise, and helpful.

================================ Human Message =================================

The SHACL validation process has identified the following violations in the current data graph:

---
### Violations:
VALIDATION RESULTS
Total violations:9
Violations:

  Violation [1]:
    Severity: Violation
    Focus node: Princess_Margarita_of_Greece_and_Denmark
    Path: hasSister
    Value: Prince_Philip_Duke_of_Edinburgh
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSister a sh:PropertyShape ;
          sh:class :Woman ;
          sh:disjoint :hasDaughter,
              :hasFather,
              :hasMother,
              :hasParent,
              :hasSon,
              :isChildOf,
              :isDaughterOf,
              :isFatherOf,
              :isMotherOf,
              :isParentOf,
              :isSonOf ;
          sh:path :hasSister .
    SHACL message: Value does not have class :Woman
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSister a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Woman ;
          rdfs:subPropertyOf :isSiblingOf ;
          owl:inverseOf :isSisterOf ;
          owl:propertyDisjointWith :isChildOf,
              :isParentOf .
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [2]:
    Severity: Violation
    Focus node: Kraft
    Path: hasFather
    Value: Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Man']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .



  Violation [3]:
    Severity: Violation
    Focus node: Kraft
    Path: hasMother
    Value: Princess_Margarita_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Man']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .



  Violation [4]:
    Severity: Violation
    Focus node: Kraft
    Path: hasFather
    Value: Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Man']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .



  Violation [5]:
    Severity: Violation
    Focus node: Kraft
    Path: hasMother
    Value: Princess_Margarita_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Man']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .



  Violation [6]:
    Severity: Violation
    Focus node: Princess_Margarita_of_Greece_and_Denmark
    Path: hasSister
    Value: Prince_Philip_Duke_of_Edinburgh
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSister a sh:PropertyShape ;
          sh:class :Woman ;
          sh:disjoint :hasDaughter,
              :hasFather,
              :hasMother,
              :hasParent,
              :hasSon,
              :isChildOf,
              :isDaughterOf,
              :isFatherOf,
              :isMotherOf,
              :isParentOf,
              :isSonOf ;
          sh:path :hasSister .
    SHACL message: Value does not have class :Woman
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSister a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Woman ;
          rdfs:subPropertyOf :isSiblingOf ;
          owl:inverseOf :isSisterOf ;
          owl:propertyDisjointWith :isChildOf,
              :isParentOf .
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .



  Violation [7]:
    Severity: Violation
    Focus node: Kraft
    Path: hasFather
    Value: Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasFather a sh:PropertyShape ;
          sh:class :Ancestor,
              :Man ;
          sh:maxCount 1 ;
          sh:path :hasFather .
    SHACL message: Value class is not in classes (:Ancestor, :Man)
    Classes assigned to the focus node: [':Man']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .

    Definition of the path:
      :hasFather a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Man ;
          rdfs:subPropertyOf :hasParent ;
          owl:inverseOf :isFatherOf .
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .



  Violation [8]:
    Severity: Violation
    Focus node: Kraft
    Path: hasMother
    Value: Princess_Margarita_of_Greece_and_Denmark
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasMother a sh:PropertyShape ;
          sh:class :Ancestor,
              :Woman ;
          sh:maxCount 1 ;
          sh:path :hasMother .
    SHACL message: Value class is not in classes (:Ancestor, :Woman)
    Classes assigned to the focus node: [':Man']
    Definitions of the classes assigned to the focus node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .

    Definition of the path:
      :hasMother a owl:FunctionalProperty,
              owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Ancestor,
              :Woman ;
          rdfs:subPropertyOf :hasParent,
              :isChildOf ;
          owl:inverseOf :isMotherOf .
    Classes assigned to the value node: [':Woman']
    Definitions of the classes assigned to the value node:
      Class :Man:
        :Man a owl:Class ;
            owl:disjointWith :Sex,
                :Woman ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Male ] ) ] .



  Violation [9]:
    Severity: Violation
    Focus node: Princess_Margarita_of_Greece_and_Denmark
    Path: hasSister
    Value: Prince_Philip_Duke_of_Edinburgh
    Constraint: ClassConstraintComponent
    Source shape:
      :Person-hasSister a sh:PropertyShape ;
          sh:class :Woman ;
          sh:disjoint :hasDaughter,
              :hasFather,
              :hasMother,
              :hasParent,
              :hasSon,
              :isChildOf,
              :isDaughterOf,
              :isFatherOf,
              :isMotherOf,
              :isParentOf,
              :isSonOf ;
          sh:path :hasSister .
    SHACL message: Value does not have class :Woman
    Classes assigned to the focus node: [':Woman']
    Definitions of the classes assigned to the focus node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .

    Definition of the path:
      :hasSister a owl:ObjectProperty ;
          rdfs:domain :Person ;
          rdfs:range :Woman ;
          rdfs:subPropertyOf :isSiblingOf ;
          owl:inverseOf :isSisterOf ;
          owl:propertyDisjointWith :isChildOf,
              :isParentOf .
    Classes assigned to the value node: [':Man']
    Definitions of the classes assigned to the value node:
      Class :Woman:
        :Woman a owl:Class ;
            owl:equivalentClass [ a owl:Class ;
                    owl:intersectionOf ( :Person [ a owl:Restriction ;
                                owl:onProperty :hasSex ;
                                owl:someValuesFrom :Female ] ) ] .




---

Please analyze each violation and provide the corresponding explanation and fix instructions. Ensure your output matches the required structured format exactly. Crucially, provide the explanations and instructions in the same order as in which violations come: first explanation-instruction block should correspond to the first violation, etc.

================================== Ai Message ==================================

[{'type': 'text', 'text': '{\n  "translations": [\n    {\n      "explanation": "The node Princess_Margarita_of_Greece_and_Denmark has a \'hasSister\' relationship pointing to Prince_Philip_Duke_of_Edinburgh, who is classified as a :Man, while the \'hasSister\' property requires the target to be a :Woman.",\n      "instruction": "RemoveTriple(Princess_Margarita_of_Greece_and_Denmark, :hasSister, Prince_Philip_Duke_of_Edinburgh)"\n    },\n    {\n      "explanation": "The node Kraft has a \'hasFather\' relationship pointing to Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg, who is missing the required :Ancestor class.",\n      "instruction": "AssignClass(Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg, :Ancestor)"\n    },\n    {\n      "explanation": "The node Kraft has a \'hasMother\' relationship pointing to Princess_Margarita_of_Greece_and_Denmark, who is missing the required :Ancestor class.",\n      "instruction": "AssignClass(Princess_Margarita_of_Greece_and_Denmark, :Ancestor)"\n    },\n    {\n      "explanation": "The node Kraft has a \'hasFather\' relationship pointing to Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg, who is missing the required :Ancestor class.",\n      "instruction": "AssignClass(Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg, :Ancestor)"\n    },\n    {\n      "explanation": "The node Kraft has a \'hasMother\' relationship pointing to Princess_Margarita_of_Greece_and_Denmark, who is missing the required :Ancestor class.",\n      "instruction": "AssignClass(Princess_Margarita_of_Greece_and_Denmark, :Ancestor)"\n    },\n    {\n      "explanation": "The node Princess_Margarita_of_Greece_and_Denmark has a \'hasSister\' relationship pointing to Prince_Philip_Duke_of_Edinburgh, who is classified as a :Man, while the \'hasSister\' property requires the target to be a :Woman.",\n      "instruction": "RemoveTriple(Princess_Margarita_of_Greece_and_Denmark, :hasSister, Prince_Philip_Duke_of_Edinburgh)"\n    },\n    {\n      "explanation": "The node Kraft has a \'hasFather\' relationship pointing to Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg, who is missing the required :Ancestor class.",\n      "instruction": "AssignClass(Gottfried_Hereditary_Prince_of_Hohenlohe-Langenburg, :Ancestor)"\n    },\n    {\n      "explanation": "The node Kraft has a \'hasMother\' relationship pointing to Princess_Margarita_of_Greece_and_Denmark, who is missing the required :Ancestor class.",\n      "instruction": "AssignClass(Princess_Margarita_of_Greece_and_Denmark, :Ancestor)"\n    },\n    {\n      "explanation": "The node Princess_Margarita_of_Greece_and_Denmark has a \'hasSister\' relationship pointing to Prince_Philip_Duke_of_Edinburgh, who is classified as a :Man, while the \'hasSister\' property requires the target to be a :Woman.",\n      "instruction": "RemoveTriple(Princess_Margarita_of_Greece_and_Denmark, :hasSister, Prince_Philip_Duke_of_Edinburgh)"\n    }\n  ]\n}', 'extras': {'signature': 'EjQKMgERTTIPSXUlroH+NK1Efsgyw3vzYoXOpQWICtznU+kNPyLXBFoA8YSuq+mp4ZlNezU9'}}]