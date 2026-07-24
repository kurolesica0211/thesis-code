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
Duke John Albert of Mecklenburg (German: Herzog Johann Albrecht zu Mecklenburg; given names John Albert Ernest Constantine Frederick Henry; 8 December 1857 – 16 February 1920) was a member of the House of Mecklenburg-Schwerin who served as the regent of two states of the German Empire.
He was first regent of the Grand Duchy of Mecklenburg-Schwerin from 1897 to 1901 for his nephew Frederick Francis IV, Grand Duke of Mecklenburg, and thereafter regent of the Duchy of Brunswick from 1907 to 1913.
Birth and interests

Duke John Albert of Mecklenburg was born in Schwerin the fifth child of Frederick Francis II, Grand Duke of Mecklenburg and his first wife Princess Augusta Reuss of Köstritz (1822–1862).
Duke John Albert was educated in Dresden, pursued a career in the Prussian Army and was well known for his love of sports.
Regencies

Following the death of his brother Frederick Francis III, Grand Duke of Mecklenburg on 10 April 1897, Duke John Albert was appointed regent for his young nephew the new Grand Duke, Frederick Francis IV after his older brother Duke Paul Frederick had renounced his claim to the regency.
On 28 May 1907, Duke John Albert was elected regent of the Duchy of Brunswick following the death of Prince Albert of Prussia by the state's diet, accepting the offer he arrived in Brunswick on 5 June 1907.
The reason for the regency in Brunswick was that in 1884 when William, Duke of Brunswick died his distant cousin and heir Ernest Augustus, Crown Prince of Hanover was prevented from taking over the duchy because he refused to renounce his claim to the throne of the Kingdom of Hanover which had been annexed by Prussia in 1866.
Shortly after assuming the regency, Duke John Albert would walk Brunswick in civilian clothes visiting museums, libraries and other institutions in the duchy, asking questions of people to discover their living conditions.
Duke John Albert also cut down on the expenses of the royal household by cutting the number of servants and retainers to the minimum needed to run the household.
The regency came to an end on 1 November 1913 when Ernest Augustus, Crown Prince of Hanover's son Ernest Augustus was permitted to ascend to Duchy following his marriage to Princess Victoria Louise of Prussia, the only daughter of the German Emperor, William II, which helped heal the rift between the houses of Hanover and Hohenzollern.
War years

During the First World War, Duke John Albert was active with the German Colonial Society in defending Germany's colonial possessions from suggestions that they should be abandoned.
Duke John Albert died in 1920 in Wiligrad castle near Lübstorf aged 62.
Marriages

John Albert was married twice: firstly in Weimar on 6 November 1886 to Princess Elisabeth Sybille of Saxe-Weimar-Eisenach (28 February 1854–10 July 1908)
the daughter of Charles Alexander, Grand Duke of Saxe-Weimar-Eisenach; secondly in Brunswick on 15 December 1909 to Princess Elisabeth of Stolberg-Rossla (1885–1969), who following his death was to marry his half brother Duke Adolf Friedrich in 1924.
Ojimukoka

Ojimukoka, a small settlement, postoffice and railway station in Namibia, was renamed Johann - Albrechtshöhe, and then simply Albrechts in his honour.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (792f812e-b4ec-4469-8723-3ae1eec04b1c)
 Call ID: 792f812e-b4ec-4469-8723-3ae1eec04b1c
  Args:
    source: John_Albert_of_Mecklenburg
    type: :Man
  AssignClass (e25bb35b-6a00-4421-9f6c-0726ebd453e1)
 Call ID: e25bb35b-6a00-4421-9f6c-0726ebd453e1
  Args:
    type: :Person
    source: John_Albert_of_Mecklenburg
  AddLiteral (3a760fd1-3e56-4824-81f4-122d7cf3a16e)
 Call ID: 3a760fd1-3e56-4824-81f4-122d7cf3a16e
  Args:
    source: John_Albert_of_Mecklenburg
    literal_value: 1857
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (6292bf45-52fa-4048-963c-e1d9979d07b2)
 Call ID: 6292bf45-52fa-4048-963c-e1d9979d07b2
  Args:
    source: John_Albert_of_Mecklenburg
    literal_value: 1920
    literal_type: xsd:integer
    relation: :hasDeathYear
  AssignClass (630a6217-3e2a-485f-bea3-6b4632609dcc)
 Call ID: 630a6217-3e2a-485f-bea3-6b4632609dcc
  Args:
    type: :Man
    source: Frederick_Francis_II
  AssignClass (367d587b-1dba-4c14-ad50-859cf1112c99)
 Call ID: 367d587b-1dba-4c14-ad50-859cf1112c99
  Args:
    source: Frederick_Francis_II
    type: :Person
  AssignClass (8725f410-29d6-4ff8-a051-cabb5789283d)
 Call ID: 8725f410-29d6-4ff8-a051-cabb5789283d
  Args:
    source: Augusta_Reuss_of_Köstritz
    type: :Woman
  AssignClass (bce3c830-bc2c-4919-b1d6-220d0a306665)
 Call ID: bce3c830-bc2c-4919-b1d6-220d0a306665
  Args:
    type: :Person
    source: Augusta_Reuss_of_Köstritz
  AddTriple (e9a77d79-4131-4c85-bcd8-9ff0c53e9321)
 Call ID: e9a77d79-4131-4c85-bcd8-9ff0c53e9321
  Args:
    target: Frederick_Francis_II
    source: John_Albert_of_Mecklenburg
    relation: :hasFather
  AddTriple (53d743da-017d-4dca-b206-7eafbfe90697)
 Call ID: 53d743da-017d-4dca-b206-7eafbfe90697
  Args:
    source: John_Albert_of_Mecklenburg
    target: Augusta_Reuss_of_Köstritz
    relation: :hasMother
  AssignClass (44ac6b03-d8f7-456a-a24d-79553be88854)
 Call ID: 44ac6b03-d8f7-456a-a24d-79553be88854
  Args:
    type: :Man
    source: Frederick_Francis_III
  AssignClass (10f4ae14-fa36-4476-87a3-ebf9024965c2)
 Call ID: 10f4ae14-fa36-4476-87a3-ebf9024965c2
  Args:
    source: Frederick_Francis_III
    type: :Person
  AddTriple (66428f67-3b7f-48e4-9f3d-27bddbd0864e)
 Call ID: 66428f67-3b7f-48e4-9f3d-27bddbd0864e
  Args:
    relation: :isBrotherOf
    target: John_Albert_of_Mecklenburg
    source: Frederick_Francis_III
  AssignClass (17239d45-7d65-4c0c-87a9-61c891813197)
 Call ID: 17239d45-7d65-4c0c-87a9-61c891813197
  Args:
    type: :Man
    source: Frederick_Francis_IV
  AssignClass (7566598e-cac3-41b3-9a01-75fcc47a432c)
 Call ID: 7566598e-cac3-41b3-9a01-75fcc47a432c
  Args:
    source: Frederick_Francis_IV
    type: :Person
  AddTriple (182d985f-0dea-4b18-845c-f82743feb699)
 Call ID: 182d985f-0dea-4b18-845c-f82743feb699
  Args:
    target: Frederick_Francis_IV
    source: Frederick_Francis_III
    relation: :isParentOf
  AssignClass (3dc3654b-15f6-4fdf-b1e2-e53b3bee41a2)
 Call ID: 3dc3654b-15f6-4fdf-b1e2-e53b3bee41a2
  Args:
    source: Paul_Frederick
    type: :Man
  AssignClass (e1ace719-b91c-468a-aed8-423abb25d27b)
 Call ID: e1ace719-b91c-468a-aed8-423abb25d27b
  Args:
    source: Paul_Frederick
    type: :Person
  AddTriple (334b5925-5acb-4335-ae37-96f6a2027a9b)
 Call ID: 334b5925-5acb-4335-ae37-96f6a2027a9b
  Args:
    relation: :isBrotherOf
    source: Paul_Frederick
    target: John_Albert_of_Mecklenburg
  AssignClass (39cd3eba-d9c9-48dd-81ff-c0467bb56888)
 Call ID: 39cd3eba-d9c9-48dd-81ff-c0467bb56888
  Args:
    type: :Woman
    source: Elisabeth_Sybille_of_Saxe-Weimar-Eisenach
  AssignClass (39cccba6-038d-425a-98af-fd50476dac76)
 Call ID: 39cccba6-038d-425a-98af-fd50476dac76
  Args:
    type: :Person
    source: Elisabeth_Sybille_of_Saxe-Weimar-Eisenach
  AddLiteral (df385302-e7e6-46eb-b32e-87030f08cccb)
 Call ID: df385302-e7e6-46eb-b32e-87030f08cccb
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1886
    source: John_Albert_of_Mecklenburg
  AssignClass (cb110fe4-b420-459b-8d6a-03be1ea104a2)
 Call ID: cb110fe4-b420-459b-8d6a-03be1ea104a2
  Args:
    source: Elisabeth_of_Stolberg-Rossla
    type: :Woman
  AssignClass (739ab9ba-63ed-422a-aaea-209c285f3dc3)
 Call ID: 739ab9ba-63ed-422a-aaea-209c285f3dc3
  Args:
    source: Elisabeth_of_Stolberg-Rossla
    type: :Person
  AddLiteral (656249f3-4f44-4965-aaff-56283bf0c63c)
 Call ID: 656249f3-4f44-4965-aaff-56283bf0c63c
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1909
    source: John_Albert_of_Mecklenburg
  AssignClass (45236fa4-a4ac-4c27-8fe5-c443019a8469)
 Call ID: 45236fa4-a4ac-4c27-8fe5-c443019a8469
  Args:
    source: Adolf_Friedrich
    type: :Man
  AssignClass (7e20736b-1805-4eba-8262-b131aa104e56)
 Call ID: 7e20736b-1805-4eba-8262-b131aa104e56
  Args:
    type: :Person
    source: Adolf_Friedrich
  AddTriple (c1268bc8-a096-42a1-972b-e8b3d4236565)
 Call ID: c1268bc8-a096-42a1-972b-e8b3d4236565
  Args:
    relation: :isBrotherOf
    target: John_Albert_of_Mecklenburg
    source: Adolf_Friedrich
  AssignClass (da1d3b85-49ed-4c3e-9cb7-7abaaafc1288)
 Call ID: da1d3b85-49ed-4c3e-9cb7-7abaaafc1288
  Args:
    type: :Man
    source: Charles_Alexander_of_Saxe-Weimar-Eisenach
  AssignClass (dd3ba744-c730-4cd7-9eec-df0c9a4d0a9f)
 Call ID: dd3ba744-c730-4cd7-9eec-df0c9a4d0a9f
  Args:
    type: :Person
    source: Charles_Alexander_of_Saxe-Weimar-Eisenach
  AddTriple (93081ce5-7978-47fd-8031-f8414bca4505)
 Call ID: 93081ce5-7978-47fd-8031-f8414bca4505
  Args:
    source: Charles_Alexander_of_Saxe-Weimar-Eisenach
    target: Elisabeth_Sybille_of_Saxe-Weimar-Eisenach
    relation: :isFatherOf
  Finish (7bf92d86-6f25-45d4-ba48-56e7c3d2ffe4)
 Call ID: 7bf92d86-6f25-45d4-ba48-56e7c3d2ffe4
  Args: