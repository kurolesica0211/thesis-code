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
Georg Friedrich Prinz von Preussen (born 10 June 1976, as Georg Friedrich Ferdinand Prinz von Preußen) is a German heir who is the current head of the Prussian branch of the House of Hohenzollern, a dynasty that ruled over the German Empire and the Kingdom of Prussia until near the end of World War I.
He is the great-great-grandson of Wilhelm II, the last German Emperor and last King of Prussia, who abdicated and went into exile upon Germany's defeat in World War I in 1918.
Education and career

Georg Friedrich is the only son and eldest child of Louis Ferdinand Prinz von Preussen (1944–1977) and Countess Donata of Castell-Rüdenhausen (1950–2015).
Born into a mediatised princely family, his mother later became Duchess Donata of Oldenburg when she married secondly Duke Friedrich August of Oldenburg, who had previously been married to her sister-in-law Princess Marie Cécile of Prussia.
Georg Friedrich earned his degree in business economics at the Freiberg University of Mining and Technology.
Georg Friedrich works for a company specialising in helping universities to bring their innovations to market.
He also administered the Princess Kira of Prussia Foundation, founded by his grandmother Grand Duchess Kira of Russia in 1952, now administered by his wife.
Until 30 December 2025, Georg Friedrich owned a two-thirds share of his family's original seat, Hohenzollern Castle, with the head of the Swabian branch, Karl Friedrich, Prince of Hohenzollern, owning the remaining third.
In an agreement taking effect on 31 December 2025, Karl Friedrich transferred his share to Georg Friedrich, giving the latter full responsibility for the operation, maintenance and cultural development of the castle.
Georg Friedrich continues to claim compensation for land and palaces in Berlin expropriated from his family, a claim begun in March 1991 by his grandfather Prince Louis Ferdinand of Prussia under the Compensation Act (EALG).
House of Hohenzollern

Georg Friedrich succeeded his grandfather, Louis Ferdinand, as Head of the Royal House of Prussia, a branch of the House of Hohenzollern, on 26 September 1994.
His position as sole heir to the estate of his grandfather was challenged by his uncles, Friedrich Wilhelm and Michael, who filed a lawsuit claiming that, despite their renunciations as dynasts at the time of their marriages, the loss of their inheritance rights based on their selection of spouse was discriminatory and unconstitutional.
However, the Federal Court of Justice of Germany overturned the original rulings in favour of Georg Friedrich's uncles, the case being remanded to the courts at Hechingen and Stuttgart.
This time both courts ruled in favour of Georg Friedrich.
His uncles then took their case to the Federal Constitutional Court of Germany which overruled the previous court rulings in Georg Friedrich's favour, on 22 March 2004.
On 19 October 2005, a German regional court ruled that Georg Friedrich was indeed the principal heir of his grandfather, Louis Ferdinand (who was the primary beneficiary of the trust set up for the estate of Wilhelm II), but also concluded that each of the children of Louis Ferdinand was entitled to a portion of the Prussian inheritance.
Family

In 2011, Georg Friedrich married Princess Sophie of Isenburg.
On 20 January 2013, Georg Friedrich's wife, Sophie, gave birth to twin sons in Bremen, Carl Friedrich Franz Alexander and Louis Ferdinand Christian Albrecht.
Carl Friedrich, the elder of the two, is his father's heir apparent.
On 17 November 2016, Sophie gave birth to Heinrich Albert Johann Georg, their fourth child.
Property claims

In 2014, Georg Friedrich filed a claim on the property of the Huis Doorn, where Kaiser Wilhelm II spent his last years after abdication, but this was rejected by Minister of Education, Culture and Science Jet Bussemaker.
In mid-2019 it was revealed that, since 2014, Georg Friedrich had filed claims for permanent right of residency for his family in Cecilienhof, or one of two other former Hohenzollern palaces in Potsdam, as well as return of the family library, 266 paintings, an imperial crown and sceptre, and the letters of Empress Augusta Victoria.
This sparked a public debate about the legitimacy of these claims and the role of the Hohenzollern during and before the Nazi regime in Germany, specifically Crown Prince Wilhelm's involvement.
On 9 March 2023, Georg Friedrich dropped the suit, hoping that doing so would "open the way for an unencumbered historical debate on the role of my family in the 20th Century following the end of the monarchy.
"


In June 2019, a claim made by Georg Friedrich that Rheinfels Castle be returned to the Hohenzollern family was dismissed by a court.
}} Media related to Georg Friedrich, Prince of Prussia at Wikimedia Commons



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
  AssignClass (fc0e0599-7380-498b-b5a2-4d254f34b1bf)
 Call ID: fc0e0599-7380-498b-b5a2-4d254f34b1bf
  Args:
    source: :Georg_Friedrich_Prinz_von_Preussen
    type: :Man
  AssignClass (b2d4a6ea-4865-4745-9d83-85a0d56610c7)
 Call ID: b2d4a6ea-4865-4745-9d83-85a0d56610c7
  Args:
    type: :Person
    source: :Georg_Friedrich_Prinz_von_Preussen
  AddLiteral (1a514b27-8db4-43bb-947c-c2c478db942d)
 Call ID: 1a514b27-8db4-43bb-947c-c2c478db942d
  Args:
    literal_value: 1976
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Georg_Friedrich_Prinz_von_Preussen
  AssignClass (3b7eefdf-17ff-4815-9947-784befe0588b)
 Call ID: 3b7eefdf-17ff-4815-9947-784befe0588b
  Args:
    type: :Man
    source: :Wilhelm_II
  AssignClass (96e61542-b020-4981-99ec-371848eedba5)
 Call ID: 96e61542-b020-4981-99ec-371848eedba5
  Args:
    source: :Wilhelm_II
    type: :Person
  AssignClass (978b3d5a-104e-478d-a8a0-157f55bfa912)
 Call ID: 978b3d5a-104e-478d-a8a0-157f55bfa912
  Args:
    type: :Man
    source: :Louis_Ferdinand_Prinz_von_Preussen
  AssignClass (cfe5b45c-b7e8-481c-8a83-9ce12fa1aef8)
 Call ID: cfe5b45c-b7e8-481c-8a83-9ce12fa1aef8
  Args:
    type: :Person
    source: :Louis_Ferdinand_Prinz_von_Preussen
  AddLiteral (cd986972-4e4d-4e3c-8a4e-1c3d36c4d763)
 Call ID: cd986972-4e4d-4e3c-8a4e-1c3d36c4d763
  Args:
    literal_value: 1944
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :Louis_Ferdinand_Prinz_von_Preussen
  AddLiteral (89fbfa3c-ecb6-406c-837c-63ef7a09a62a)
 Call ID: 89fbfa3c-ecb6-406c-837c-63ef7a09a62a
  Args:
    source: :Louis_Ferdinand_Prinz_von_Preussen
    literal_type: xsd:integer
    literal_value: 1977
    relation: :hasDeathYear
  AssignClass (54a78158-28eb-47b4-87da-4b34800bc30a)
 Call ID: 54a78158-28eb-47b4-87da-4b34800bc30a
  Args:
    source: :Donata_of_Castell-Rüdenhausen
    type: :Woman
  AssignClass (e3e08b89-1536-4762-a39a-08baf0b33e73)
 Call ID: e3e08b89-1536-4762-a39a-08baf0b33e73
  Args:
    source: :Donata_of_Castell-Rüdenhausen
    type: :Person
  AddLiteral (e1a3d018-692e-4010-a465-0677025947e9)
 Call ID: e1a3d018-692e-4010-a465-0677025947e9
  Args:
    relation: :hasBirthYear
    literal_value: 1950
    literal_type: xsd:integer
    source: :Donata_of_Castell-Rüdenhausen
  AddLiteral (134f5019-6385-4e00-82fb-8ff1a5a63e8b)
 Call ID: 134f5019-6385-4e00-82fb-8ff1a5a63e8b
  Args:
    source: :Donata_of_Castell-Rüdenhausen
    literal_type: xsd:integer
    literal_value: 2015
    relation: :hasDeathYear
  AddTriple (31ba1982-b8b1-41d1-bbaf-4cbfdda000ef)
 Call ID: 31ba1982-b8b1-41d1-bbaf-4cbfdda000ef
  Args:
    relation: :hasFather
    target: :Louis_Ferdinand_Prinz_von_Preussen
    source: :Georg_Friedrich_Prinz_von_Preussen
  AddTriple (115cecc7-9a98-4e78-860c-d4dc6f600da0)
 Call ID: 115cecc7-9a98-4e78-860c-d4dc6f600da0
  Args:
    source: :Georg_Friedrich_Prinz_von_Preussen
    relation: :hasMother
    target: :Donata_of_Castell-Rüdenhausen
  AddTriple (a94a5b43-b253-44d5-906e-d4201ab525e5)
 Call ID: a94a5b43-b253-44d5-906e-d4201ab525e5
  Args:
    source: :Louis_Ferdinand_Prinz_von_Preussen
    target: :Prince_Louis_Ferdinand_of_Prussia
    relation: :hasFather
  AssignClass (85b7e7ec-a643-40d8-b20c-74668ed33165)
 Call ID: 85b7e7ec-a643-40d8-b20c-74668ed33165
  Args:
    type: :Man
    source: :Prince_Louis_Ferdinand_of_Prussia
  AssignClass (3478da94-627f-4263-9115-6a12c26df9c0)
 Call ID: 3478da94-627f-4263-9115-6a12c26df9c0
  Args:
    source: :Prince_Louis_Ferdinand_of_Prussia
    type: :Person
  AssignClass (3e25a4cc-3852-4917-8346-86ed12320c44)
 Call ID: 3e25a4cc-3852-4917-8346-86ed12320c44
  Args:
    source: :Princess_Sophie_of_Isenburg
    type: :Woman
  AssignClass (689ec290-cf10-4fb4-b46e-abd368c85f5d)
 Call ID: 689ec290-cf10-4fb4-b46e-abd368c85f5d
  Args:
    type: :Person
    source: :Princess_Sophie_of_Isenburg
  AddTriple (589ab9f9-0491-4b94-97c6-b617d569c290)
 Call ID: 589ab9f9-0491-4b94-97c6-b617d569c290
  Args:
    target: :Princess_Sophie_of_Isenburg
    relation: :hasRelation
    source: :Georg_Friedrich_Prinz_von_Preussen
  AssignClass (af0ddc12-e31f-47bf-895e-a6db31669b74)
 Call ID: af0ddc12-e31f-47bf-895e-a6db31669b74
  Args:
    type: :Man
    source: :Carl_Friedrich_Franz_Alexander
  AssignClass (e472ecaa-fc52-489a-9ba4-ea3a10ba5a07)
 Call ID: e472ecaa-fc52-489a-9ba4-ea3a10ba5a07
  Args:
    source: :Carl_Friedrich_Franz_Alexander
    type: :Person
  AddTriple (17bc19a0-5d43-4d54-83a4-9d7f0c111a96)
 Call ID: 17bc19a0-5d43-4d54-83a4-9d7f0c111a96
  Args:
    source: :Carl_Friedrich_Franz_Alexander
    target: :Georg_Friedrich_Prinz_von_Preussen
    relation: :hasFather
  AddTriple (c41fffca-b85f-4b8d-8bda-d255c3acb33e)
 Call ID: c41fffca-b85f-4b8d-8bda-d255c3acb33e
  Args:
    source: :Carl_Friedrich_Franz_Alexander
    relation: :hasMother
    target: :Princess_Sophie_of_Isenburg
  AssignClass (ae5a5d7c-926c-49fe-acda-c846f9eb9a19)
 Call ID: ae5a5d7c-926c-49fe-acda-c846f9eb9a19
  Args:
    type: :Man
    source: :Louis_Ferdinand_Christian_Albrecht
  AssignClass (097946e5-fbab-4320-899f-a92c2ec3a051)
 Call ID: 097946e5-fbab-4320-899f-a92c2ec3a051
  Args:
    type: :Person
    source: :Louis_Ferdinand_Christian_Albrecht
  AddTriple (a564812f-30da-484f-9464-2acc97eb526b)
 Call ID: a564812f-30da-484f-9464-2acc97eb526b
  Args:
    relation: :hasFather
    target: :Georg_Friedrich_Prinz_von_Preussen
    source: :Louis_Ferdinand_Christian_Albrecht
  AddTriple (a75e4612-77b5-4386-8e87-5fcdd7eeb39f)
 Call ID: a75e4612-77b5-4386-8e87-5fcdd7eeb39f
  Args:
    source: :Louis_Ferdinand_Christian_Albrecht
    relation: :hasMother
    target: :Princess_Sophie_of_Isenburg
  AssignClass (b2146a7b-465c-44fd-8294-ef5ab1a50ac2)
 Call ID: b2146a7b-465c-44fd-8294-ef5ab1a50ac2
  Args:
    type: :Man
    source: :Heinrich_Albert_Johann_Georg
  AssignClass (df1b3dd0-98e1-4006-b583-a5e3e4194d19)
 Call ID: df1b3dd0-98e1-4006-b583-a5e3e4194d19
  Args:
    source: :Heinrich_Albert_Johann_Georg
    type: :Person
  AddTriple (c4f4310f-44ce-49c1-823b-9df6ddd7c6ed)
 Call ID: c4f4310f-44ce-49c1-823b-9df6ddd7c6ed
  Args:
    target: :Georg_Friedrich_Prinz_von_Preussen
    relation: :hasFather
    source: :Heinrich_Albert_Johann_Georg
  AddTriple (d8db5c6f-4d54-4d90-b0c6-5e4b80c5cd5e)
 Call ID: d8db5c6f-4d54-4d90-b0c6-5e4b80c5cd5e
  Args:
    source: :Heinrich_Albert_Johann_Georg
    relation: :hasMother
    target: :Princess_Sophie_of_Isenburg
  AssignClass (82a310f1-c586-40d7-80a5-ffeac6c13dfe)
 Call ID: 82a310f1-c586-40d7-80a5-ffeac6c13dfe
  Args:
    source: :Friedrich_Wilhelm
    type: :Man
  AssignClass (563ea073-72a1-4829-b8d1-7673d363752e)
 Call ID: 563ea073-72a1-4829-b8d1-7673d363752e
  Args:
    type: :Person
    source: :Friedrich_Wilhelm
  AssignClass (951f3725-768c-42b8-abc2-ad6d807c88cc)
 Call ID: 951f3725-768c-42b8-abc2-ad6d807c88cc
  Args:
    type: :Man
    source: :Michael
  AssignClass (b3dad4ec-3fed-44ea-826f-46e870c00b0d)
 Call ID: b3dad4ec-3fed-44ea-826f-46e870c00b0d
  Args:
    source: :Michael
    type: :Person
  AddTriple (c3df6bfe-41ec-4634-b284-5c27e41c2922)
 Call ID: c3df6bfe-41ec-4634-b284-5c27e41c2922
  Args:
    relation: :hasParent
    target: :Prince_Louis_Ferdinand_of_Prussia
    source: :Friedrich_Wilhelm
  AddTriple (cae11324-4cf2-495f-a787-879a45b47910)
 Call ID: cae11324-4cf2-495f-a787-879a45b47910
  Args:
    source: :Michael
    relation: :hasParent
    target: :Prince_Louis_Ferdinand_of_Prussia
  AddTriple (4fba3ad7-6f51-4573-94b6-5abb1ebbf394)
 Call ID: 4fba3ad7-6f51-4573-94b6-5abb1ebbf394
  Args:
    target: :Prince_Louis_Ferdinand_of_Prussia
    relation: :hasParent
    source: :Louis_Ferdinand_Prinz_von_Preussen
  Finish (398a7a63-24a0-4fb1-b5ae-736401490695)
 Call ID: 398a7a63-24a0-4fb1-b5ae-736401490695
  Args: