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
Wilhelm Herzog von Württemberg (born Wilhelm Friedrich Carl Philipp Albert Nikolaus Erich Maria; 13 August 1994) is the head of the House of Württemberg and a German businessman.
He is Chair of the Hofkammer des Hauses Württemberg, the company which manages the forests, farms, wineries, and housing estates of the former royal family of the Kingdom of Württemberg.
Life

Wilhelm is the eldest child of Friedrich, Hereditary Duke of Württemberg (1961–2018) and Princess Marie Wilhelmine of Wied (born 1973).
He was baptised in September 1994,  with his uncles Erich, Prince of Waldburg zu Zeil und Trauchburg, and Prince Wilhelm of Wied, as his godfathers.
On 9 May 2018, Wilhelm's father died in a car accident while driving on his way home to Friedrichshafen.
Upon the death of his father, Wilhelm became the heir apparent to his grandfather, Carl, Duke of Württemberg as Head of the House of Württemberg.
In July 2019, it was also announced that Wilhelm would be the future head of the Württemberg Hofkammer, the administrative offices of the family business.
On 7 June 2022, Wilhelm succeeded as Head of the House of Württemberg upon the death of his grandfather, Carl, Duke of Württemberg.
Wilhelm is unmarried.
With the headship of the house passing through the male line, the heir presumptive of the House of Württemberg is Wilhelm's paternal uncle Duke Eberhard of Württemberg, who married Gaby Maier on 15 July 2023.



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
  AssignClass (44bbd350-fff6-4088-bc21-232048aa4b39)
 Call ID: 44bbd350-fff6-4088-bc21-232048aa4b39
  Args:
    type: :Man
    source: Wilhelm_Herzog_von_Württemberg
  AssignClass (a03577b2-6d92-41ef-bc42-474716871984)
 Call ID: a03577b2-6d92-41ef-bc42-474716871984
  Args:
    source: Wilhelm_Herzog_von_Württemberg
    type: :Person
  AddLiteral (2df277c5-bd88-4f15-a95d-ccae619672f3)
 Call ID: 2df277c5-bd88-4f15-a95d-ccae619672f3
  Args:
    source: Wilhelm_Herzog_von_Württemberg
    literal_type: xsd:integer
    literal_value: 1994
    relation: :hasBirthYear
  AssignClass (32f54d01-5892-4d66-93e2-4ff74f4817ba)
 Call ID: 32f54d01-5892-4d66-93e2-4ff74f4817ba
  Args:
    type: :Man
    source: Friedrich_Hereditary_Duke_of_Württemberg
  AssignClass (7701e895-5024-4250-ac94-6a6b45a07292)
 Call ID: 7701e895-5024-4250-ac94-6a6b45a07292
  Args:
    type: :Person
    source: Friedrich_Hereditary_Duke_of_Württemberg
  AddLiteral (dfb24c52-841e-45f1-86a6-341a49d590cb)
 Call ID: dfb24c52-841e-45f1-86a6-341a49d590cb
  Args:
    source: Friedrich_Hereditary_Duke_of_Württemberg
    literal_type: xsd:integer
    literal_value: 1961
    relation: :hasBirthYear
  AddLiteral (6ac3d636-af60-4caa-b9af-77654d098f6d)
 Call ID: 6ac3d636-af60-4caa-b9af-77654d098f6d
  Args:
    relation: :hasDeathYear
    literal_value: 2018
    literal_type: xsd:integer
    source: Friedrich_Hereditary_Duke_of_Württemberg
  AssignClass (b75d6c98-3bd9-4ff1-9ae5-30bc198e2033)
 Call ID: b75d6c98-3bd9-4ff1-9ae5-30bc198e2033
  Args:
    type: :Woman
    source: Princess_Marie_Wilhelmine_of_Wied
  AssignClass (ced4dc9d-08a5-4847-9de4-20f1e92541e7)
 Call ID: ced4dc9d-08a5-4847-9de4-20f1e92541e7
  Args:
    source: Princess_Marie_Wilhelmine_of_Wied
    type: :Person
  AddLiteral (235f30ab-0840-4a75-98f1-8410e4254fa9)
 Call ID: 235f30ab-0840-4a75-98f1-8410e4254fa9
  Args:
    source: Princess_Marie_Wilhelmine_of_Wied
    literal_type: xsd:integer
    literal_value: 1973
    relation: :hasBirthYear
  AddTriple (0cca3e83-d348-4f62-b8e4-0c3caa770545)
 Call ID: 0cca3e83-d348-4f62-b8e4-0c3caa770545
  Args:
    target: Friedrich_Hereditary_Duke_of_Württemberg
    source: Wilhelm_Herzog_von_Württemberg
    relation: :hasFather
  AddTriple (510c350b-5ee0-4222-ae5d-e525a2dbb3dd)
 Call ID: 510c350b-5ee0-4222-ae5d-e525a2dbb3dd
  Args:
    relation: :hasMother
    target: Princess_Marie_Wilhelmine_of_Wied
    source: Wilhelm_Herzog_von_Württemberg
  AssignClass (1ac8eb72-3775-4f76-8069-6b8ddb2a804f)
 Call ID: 1ac8eb72-3775-4f76-8069-6b8ddb2a804f
  Args:
    type: :Man
    source: Carl_Duke_of_Württemberg
  AssignClass (c441db36-5d13-4933-9ce4-eae32410755f)
 Call ID: c441db36-5d13-4933-9ce4-eae32410755f
  Args:
    source: Carl_Duke_of_Württemberg
    type: :Person
  AddTriple (e3c5595a-6ae4-428b-acc3-7a2a00d3892d)
 Call ID: e3c5595a-6ae4-428b-acc3-7a2a00d3892d
  Args:
    relation: :hasFather
    target: Carl_Duke_of_Württemberg
    source: Friedrich_Hereditary_Duke_of_Württemberg
  AddLiteral (0944784c-c572-469b-9375-64f9f3fc6d0e)
 Call ID: 0944784c-c572-469b-9375-64f9f3fc6d0e
  Args:
    literal_value: 2022
    source: Carl_Duke_of_Württemberg
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (c0c6166b-a8a0-40b7-99f1-e8550d425d8e)
 Call ID: c0c6166b-a8a0-40b7-99f1-e8550d425d8e
  Args:
    source: Erich_Prince_of_Waldburg_zu_Zeil_und_Trauchburg
    type: :Man
  AssignClass (a14cb4dc-bb24-49de-8622-56c6f938484c)
 Call ID: a14cb4dc-bb24-49de-8622-56c6f938484c
  Args:
    source: Erich_Prince_of_Waldburg_zu_Zeil_und_Trauchburg
    type: :Person
  AssignClass (11c1842c-a3f5-4f8b-9b71-77e683f6e968)
 Call ID: 11c1842c-a3f5-4f8b-9b71-77e683f6e968
  Args:
    type: :Man
    source: Prince_Wilhelm_of_Wied
  AssignClass (e259000d-9fcc-4d5e-9c95-55360a6adbbc)
 Call ID: e259000d-9fcc-4d5e-9c95-55360a6adbbc
  Args:
    type: :Person
    source: Prince_Wilhelm_of_Wied
  AssignClass (1c6e0955-8a67-4d07-bf69-eae9b63fb1fd)
 Call ID: 1c6e0955-8a67-4d07-bf69-eae9b63fb1fd
  Args:
    source: Duke_Eberhard_of_Württemberg
    type: :Man
  AssignClass (3e765be8-02ed-48b6-9e97-52802fd3aa76)
 Call ID: 3e765be8-02ed-48b6-9e97-52802fd3aa76
  Args:
    source: Duke_Eberhard_of_Württemberg
    type: :Person
  AssignClass (9502d282-69d7-4e1b-b082-655eb61e1970)
 Call ID: 9502d282-69d7-4e1b-b082-655eb61e1970
  Args:
    type: :Woman
    source: Gaby_Maier
  AssignClass (fe643fe8-d52b-4f06-b56c-22158fa4e4a1)
 Call ID: fe643fe8-d52b-4f06-b56c-22158fa4e4a1
  Args:
    source: Gaby_Maier
    type: :Person
  AddTriple (47bb85c1-8b3e-427e-9d59-1093ad97ad03)
 Call ID: 47bb85c1-8b3e-427e-9d59-1093ad97ad03
  Args:
    relation: :hasRelation
    source: Duke_Eberhard_of_Württemberg
    target: Gaby_Maier
  AddLiteral (cbd96740-8810-4526-9e31-6c454ad58b12)
 Call ID: cbd96740-8810-4526-9e31-6c454ad58b12
  Args:
    relation: :hasMarriageYear
    literal_value: 2023
    source: Duke_Eberhard_of_Württemberg
    literal_type: xsd:integer
  Finish (c1cac3e8-79b4-4245-8441-7936ffa62e5d)
 Call ID: c1cac3e8-79b4-4245-8441-7936ffa62e5d
  Args: