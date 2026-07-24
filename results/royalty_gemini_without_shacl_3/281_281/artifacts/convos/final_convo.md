================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Princess María de las Mercedes of Bavaria, Infanta of Spain (3 October 1911 – 11 September 1953) was a German-Spanish princess.
She was the third wife of Georgian Prince Irakli Bagration of Mukhrani.
Through her father, Prince Ferdinand of Bavaria, she was a member of the Bavarian House of Wittelsbach.
Through her mother, Infanta María Teresa of Spain, she was a granddaughter of Alfonso XII and niece of Alfonso XIII.
Early life

Princess María de las Mercedes of Bavaria, Infanta of Spain, was born on 3 October 1911 at the Palace of the Cuesta de la Vega, Madrid, to Prince Ferdinand of Bavaria and Infanta María Teresa of Spain.
Her parents were first cousins, both grandchildren of Isabella II of Spain.
Prior to her birth, her uncle, King Alfonso XIII, declared that any children born of her parents' marriage would be Infantes or Infantas of Spain.
She was christened María de las Mercedes Teresa María de la
Her godparents were Infanta María de la Paz of Spain (her paternal grandmother) and Prince Adalbert of Bavaria (her paternal uncle, for whom Prince Carlos of Bourbon-Two Sicilies stood proxy).
She had two elder brothers, Luis Alfonso (1906–1983) and José Eugenio (1909–1966), and one younger sister, María del Pilar (1912–1918).
Marriage and issue

On 29 August 1946, Infanta María de las Mercedes married Prince Irakli Bagration of Mukhrani at the Miramar Palace in San Sebastián.
In 1948, Irakli's sister Leonida married Grand Duke Vladimir.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (fe4c86b7-afb0-4dbe-8f80-75a26640682b)
 Call ID: fe4c86b7-afb0-4dbe-8f80-75a26640682b
  Args:
    type: :Woman
    source: :Maria_de_las_Mercedes_of_Bavaria
  AssignClass (1b1647f0-4b42-4ae5-8ddc-a74ed2624953)
 Call ID: 1b1647f0-4b42-4ae5-8ddc-a74ed2624953
  Args:
    type: :Person
    source: :Maria_de_las_Mercedes_of_Bavaria
  AddLiteral (d3a1632c-18be-41d1-a6fe-19dc3f5326b1)
 Call ID: d3a1632c-18be-41d1-a6fe-19dc3f5326b1
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1911
    source: :Maria_de_las_Mercedes_of_Bavaria
  AddLiteral (f48d4825-2d97-4974-a8de-6e2fcee4f21a)
 Call ID: f48d4825-2d97-4974-a8de-6e2fcee4f21a
  Args:
    source: :Maria_de_las_Mercedes_of_Bavaria
    literal_value: 1953
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (3da1d3d7-99e4-4b9f-8426-5a9d901d4c83)
 Call ID: 3da1d3d7-99e4-4b9f-8426-5a9d901d4c83
  Args:
    source: :Irakli_Bagration_of_Mukhrani
    type: :Man
  AssignClass (80af22a3-df3b-4d6b-87f2-a3d186de6fe2)
 Call ID: 80af22a3-df3b-4d6b-87f2-a3d186de6fe2
  Args:
    type: :Person
    source: :Irakli_Bagration_of_Mukhrani
  AddLiteral (ead08933-4960-46d3-ba03-9594fa4b4559)
 Call ID: ead08933-4960-46d3-ba03-9594fa4b4559
  Args:
    relation: :hasMarriageYear
    literal_value: 1946
    source: :Maria_de_las_Mercedes_of_Bavaria
    literal_type: xsd:integer
  AddTriple (35423bca-bac2-4321-b039-78ec9b8ba302)
 Call ID: 35423bca-bac2-4321-b039-78ec9b8ba302
  Args:
    target: :Irakli_Bagration_of_Mukhrani
    relation: :hasRelation
    source: :Maria_de_las_Mercedes_of_Bavaria
  AssignClass (d406d0c1-20a3-438a-8116-48498a106cda)
 Call ID: d406d0c1-20a3-438a-8116-48498a106cda
  Args:
    type: :Man
    source: :Prince_Ferdinand_of_Bavaria
  AssignClass (176dc645-72f7-40bc-81e4-b314279c3c8b)
 Call ID: 176dc645-72f7-40bc-81e4-b314279c3c8b
  Args:
    source: :Prince_Ferdinand_of_Bavaria
    type: :Person
  AssignClass (f8f44889-83c3-47bf-9d44-b4ea019e1444)
 Call ID: f8f44889-83c3-47bf-9d44-b4ea019e1444
  Args:
    source: :Infanta_Maria_Teresa_of_Spain
    type: :Woman
  AssignClass (630554d7-60fc-4113-a2c0-01175ff9718c)
 Call ID: 630554d7-60fc-4113-a2c0-01175ff9718c
  Args:
    source: :Infanta_Maria_Teresa_of_Spain
    type: :Person
  AddTriple (fdd62b32-d6ae-457d-bfa1-f08eff871b4d)
 Call ID: fdd62b32-d6ae-457d-bfa1-f08eff871b4d
  Args:
    source: :Maria_de_las_Mercedes_of_Bavaria
    relation: :hasFather
    target: :Prince_Ferdinand_of_Bavaria
  AddTriple (3b175453-d5e1-4439-9af0-0e0ede542e61)
 Call ID: 3b175453-d5e1-4439-9af0-0e0ede542e61
  Args:
    source: :Maria_de_las_Mercedes_of_Bavaria
    relation: :hasMother
    target: :Infanta_Maria_Teresa_of_Spain
  AssignClass (9b5a395b-b160-44a8-8881-f8577cd586ba)
 Call ID: 9b5a395b-b160-44a8-8881-f8577cd586ba
  Args:
    source: :Alfonso_XII
    type: :Man
  AssignClass (b778fb35-683b-475d-a665-caa3b21115b4)
 Call ID: b778fb35-683b-475d-a665-caa3b21115b4
  Args:
    type: :Person
    source: :Alfonso_XII
  AssignClass (44028ee0-a913-4258-b048-5a7cffed5c29)
 Call ID: 44028ee0-a913-4258-b048-5a7cffed5c29
  Args:
    type: :Man
    source: :Alfonso_XIII
  AssignClass (f09d50c5-bf3e-42f2-a4cf-d20aa7a8fe7e)
 Call ID: f09d50c5-bf3e-42f2-a4cf-d20aa7a8fe7e
  Args:
    source: :Alfonso_XIII
    type: :Person
  AssignClass (c7e81e25-f73f-4ce7-8325-3309de5b7a1d)
 Call ID: c7e81e25-f73f-4ce7-8325-3309de5b7a1d
  Args:
    source: :Isabella_II_of_Spain
    type: :Woman
  AssignClass (8aa43baf-c619-4a88-b27f-e944f5dfc386)
 Call ID: 8aa43baf-c619-4a88-b27f-e944f5dfc386
  Args:
    source: :Isabella_II_of_Spain
    type: :Person
  AssignClass (40ab255f-d6bd-4dce-9aeb-0e150a449782)
 Call ID: 40ab255f-d6bd-4dce-9aeb-0e150a449782
  Args:
    type: :Woman
    source: :Infanta_Maria_de_la_Paz_of_Spain
  AssignClass (1a062b77-51d5-4bd6-bd8d-8e86cf27ce30)
 Call ID: 1a062b77-51d5-4bd6-bd8d-8e86cf27ce30
  Args:
    type: :Person
    source: :Infanta_Maria_de_la_Paz_of_Spain
  AssignClass (3de92a9f-ab4e-4b20-875c-88f9ac2f0277)
 Call ID: 3de92a9f-ab4e-4b20-875c-88f9ac2f0277
  Args:
    type: :Man
    source: :Prince_Adalbert_of_Bavaria
  AssignClass (19f007a6-144a-4a23-b61c-67e7d206529a)
 Call ID: 19f007a6-144a-4a23-b61c-67e7d206529a
  Args:
    type: :Person
    source: :Prince_Adalbert_of_Bavaria
  AssignClass (6585ae35-e8a0-4276-8b8d-68b81b7aaca8)
 Call ID: 6585ae35-e8a0-4276-8b8d-68b81b7aaca8
  Args:
    source: :Prince_Carlos_of_Bourbon_Two_Sicilies
    type: :Man
  AssignClass (7a150d0b-0eea-4559-9f99-fe01a8fe40f8)
 Call ID: 7a150d0b-0eea-4559-9f99-fe01a8fe40f8
  Args:
    type: :Person
    source: :Prince_Carlos_of_Bourbon_Two_Sicilies
  AssignClass (5eb48566-945c-423d-897e-fa2c58faaa63)
 Call ID: 5eb48566-945c-423d-897e-fa2c58faaa63
  Args:
    source: :Luis_Alfonso
    type: :Man
  AssignClass (b44cd6cb-16d8-47b4-a45a-b046b70330d9)
 Call ID: b44cd6cb-16d8-47b4-a45a-b046b70330d9
  Args:
    source: :Luis_Alfonso
    type: :Person
  AddLiteral (3a2cd4f2-4dec-4345-a03f-082dfaf9e0de)
 Call ID: 3a2cd4f2-4dec-4345-a03f-082dfaf9e0de
  Args:
    literal_type: xsd:integer
    source: :Luis_Alfonso
    literal_value: 1906
    relation: :hasBirthYear
  AddLiteral (efb9b02c-8904-4add-a789-cbeccb817f87)
 Call ID: efb9b02c-8904-4add-a789-cbeccb817f87
  Args:
    literal_type: xsd:integer
    literal_value: 1983
    source: :Luis_Alfonso
    relation: :hasDeathYear
  AssignClass (e7d47331-2121-4280-8252-dd2f7fd5adb8)
 Call ID: e7d47331-2121-4280-8252-dd2f7fd5adb8
  Args:
    source: :Jose_Eugenio
    type: :Man
  AssignClass (dee4eb55-eaec-4181-bfb7-7c36102c3a21)
 Call ID: dee4eb55-eaec-4181-bfb7-7c36102c3a21
  Args:
    type: :Person
    source: :Jose_Eugenio
  AddLiteral (fe21f438-91ce-43c5-a2c9-455963e0f512)
 Call ID: fe21f438-91ce-43c5-a2c9-455963e0f512
  Args:
    literal_type: xsd:integer
    source: :Jose_Eugenio
    literal_value: 1909
    relation: :hasBirthYear
  AddLiteral (8b083d05-fe5c-4378-9713-450a04df4e39)
 Call ID: 8b083d05-fe5c-4378-9713-450a04df4e39
  Args:
    literal_type: xsd:integer
    literal_value: 1966
    source: :Jose_Eugenio
    relation: :hasDeathYear
  AssignClass (ae945399-60ec-4710-96b1-33d77ec8b576)
 Call ID: ae945399-60ec-4710-96b1-33d77ec8b576
  Args:
    source: :Maria_del_Pilar
    type: :Woman
  AssignClass (c4edad96-75bd-4fe5-b312-3568befcd04b)
 Call ID: c4edad96-75bd-4fe5-b312-3568befcd04b
  Args:
    source: :Maria_del_Pilar
    type: :Person
  AddLiteral (751352cf-6888-44fc-bb90-d482cf95d657)
 Call ID: 751352cf-6888-44fc-bb90-d482cf95d657
  Args:
    relation: :hasBirthYear
    source: :Maria_del_Pilar
    literal_value: 1912
    literal_type: xsd:integer
  AddLiteral (1939b450-2116-47bf-9a84-b01f97577579)
 Call ID: 1939b450-2116-47bf-9a84-b01f97577579
  Args:
    source: :Maria_del_Pilar
    literal_value: 1918
    literal_type: xsd:integer
    relation: :hasDeathYear
  AddTriple (46821a7e-ae8e-40a8-bcca-3a4c284b4b36)
 Call ID: 46821a7e-ae8e-40a8-bcca-3a4c284b4b36
  Args:
    relation: :isSiblingOf
    target: :Luis_Alfonso
    source: :Maria_de_las_Mercedes_of_Bavaria
  AddTriple (de1e3ff6-308a-4205-8e46-4646cd42281c)
 Call ID: de1e3ff6-308a-4205-8e46-4646cd42281c
  Args:
    source: :Maria_de_las_Mercedes_of_Bavaria
    relation: :isSiblingOf
    target: :Jose_Eugenio
  AddTriple (ec62d379-2682-4c78-ab35-e4ef689bc5c6)
 Call ID: ec62d379-2682-4c78-ab35-e4ef689bc5c6
  Args:
    source: :Maria_de_las_Mercedes_of_Bavaria
    target: :Maria_del_Pilar
    relation: :isSiblingOf
  AssignClass (afeb7bf5-e7a2-4a2b-8420-b98c84132925)
 Call ID: afeb7bf5-e7a2-4a2b-8420-b98c84132925
  Args:
    source: :Leonida
    type: :Woman
  AssignClass (fe252fe1-9af1-4a69-aadf-7db88359aa92)
 Call ID: fe252fe1-9af1-4a69-aadf-7db88359aa92
  Args:
    source: :Leonida
    type: :Person
  AssignClass (fd1d6f15-3a10-4865-b3b7-d20213ad37d2)
 Call ID: fd1d6f15-3a10-4865-b3b7-d20213ad37d2
  Args:
    source: :Grand_Duke_Vladimir
    type: :Man
  AssignClass (b61d643f-3a29-4dd3-837d-cf18839b2c8a)
 Call ID: b61d643f-3a29-4dd3-837d-cf18839b2c8a
  Args:
    type: :Person
    source: :Grand_Duke_Vladimir
  AddTriple (a285687c-bc66-4b6c-96e6-594805fcf6a1)
 Call ID: a285687c-bc66-4b6c-96e6-594805fcf6a1
  Args:
    relation: :isSiblingOf
    target: :Leonida
    source: :Irakli_Bagration_of_Mukhrani
  AddTriple (1fd8783d-44e3-4a91-982d-f663431f3c21)
 Call ID: 1fd8783d-44e3-4a91-982d-f663431f3c21
  Args:
    source: :Leonida
    relation: :hasRelation
    target: :Grand_Duke_Vladimir
  Finish (6e90dbf9-30c6-455f-9279-84e6557b4057)
 Call ID: 6e90dbf9-30c6-455f-9279-84e6557b4057
  Args: