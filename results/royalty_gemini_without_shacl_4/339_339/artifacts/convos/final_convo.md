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
  AssignClass (e98282dc-30d9-4ed3-8a50-9087d500ec4c)
 Call ID: e98282dc-30d9-4ed3-8a50-9087d500ec4c
  Args:
    type: :Man
    source: Georg_Friedrich_Prinz_von_Preussen
  AssignClass (aa3ab384-f62b-481e-ab5d-06a02c9120ef)
 Call ID: aa3ab384-f62b-481e-ab5d-06a02c9120ef
  Args:
    type: :Person
    source: Georg_Friedrich_Prinz_von_Preussen
  AddLiteral (4d6c7077-cc0f-4c48-aa15-00e3030a78c2)
 Call ID: 4d6c7077-cc0f-4c48-aa15-00e3030a78c2
  Args:
    source: Georg_Friedrich_Prinz_von_Preussen
    literal_value: 1976
    literal_type: xsd:integer
    relation: :hasBirthYear
  AssignClass (0fdb0336-cd67-476a-9e7b-a4299cb4112f)
 Call ID: 0fdb0336-cd67-476a-9e7b-a4299cb4112f
  Args:
    type: :Man
    source: Louis_Ferdinand_Prinz_von_Preussen
  AssignClass (251f63cd-0277-4f09-9856-f0674aed387b)
 Call ID: 251f63cd-0277-4f09-9856-f0674aed387b
  Args:
    type: :Person
    source: Louis_Ferdinand_Prinz_von_Preussen
  AddLiteral (bae95612-3645-442d-8e67-921a045a76b9)
 Call ID: bae95612-3645-442d-8e67-921a045a76b9
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Louis_Ferdinand_Prinz_von_Preussen
    literal_value: 1944
  AddLiteral (80653217-0e6f-4d51-9ebc-3fa2fffa7bf2)
 Call ID: 80653217-0e6f-4d51-9ebc-3fa2fffa7bf2
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    literal_value: 1977
    source: Louis_Ferdinand_Prinz_von_Preussen
  AssignClass (ff324706-8e70-4629-9102-dd7aef7e2335)
 Call ID: ff324706-8e70-4629-9102-dd7aef7e2335
  Args:
    type: :Woman
    source: Donata_of_Castell-Rüdenhausen
  AssignClass (89cde00d-353f-44a6-ab03-e0a5668674f0)
 Call ID: 89cde00d-353f-44a6-ab03-e0a5668674f0
  Args:
    type: :Person
    source: Donata_of_Castell-Rüdenhausen
  AddLiteral (a4285a4e-e02c-41f6-9a45-463a96b6c83f)
 Call ID: a4285a4e-e02c-41f6-9a45-463a96b6c83f
  Args:
    source: Donata_of_Castell-Rüdenhausen
    literal_value: 1950
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddLiteral (c0635be7-c440-4d42-9d54-4f35b2e3d336)
 Call ID: c0635be7-c440-4d42-9d54-4f35b2e3d336
  Args:
    literal_value: 2015
    source: Donata_of_Castell-Rüdenhausen
    relation: :hasDeathYear
    literal_type: xsd:integer
  AddTriple (ba785013-4766-412e-89f0-39f3eb2eb13e)
 Call ID: ba785013-4766-412e-89f0-39f3eb2eb13e
  Args:
    target: Louis_Ferdinand_Prinz_von_Preussen
    source: Georg_Friedrich_Prinz_von_Preussen
    relation: :hasFather
  AddTriple (0ad90b5d-423c-47b5-8a9a-ae84c5944e44)
 Call ID: 0ad90b5d-423c-47b5-8a9a-ae84c5944e44
  Args:
    relation: :hasMother
    target: Donata_of_Castell-Rüdenhausen
    source: Georg_Friedrich_Prinz_von_Preussen
  AssignClass (545eb47f-1810-4136-af5f-297535ed012d)
 Call ID: 545eb47f-1810-4136-af5f-297535ed012d
  Args:
    type: :Man
    source: Wilhelm_II
  AssignClass (cfb5ee26-8d98-480d-aef5-9c534396e321)
 Call ID: cfb5ee26-8d98-480d-aef5-9c534396e321
  Args:
    type: :Person
    source: Wilhelm_II
  AddTriple (7be35291-2a98-4347-80eb-05e85f0dde1d)
 Call ID: 7be35291-2a98-4347-80eb-05e85f0dde1d
  Args:
    relation: :hasAncestor
    target: Wilhelm_II
    source: Georg_Friedrich_Prinz_von_Preussen
  AssignClass (57ee648f-f920-4467-ac3e-9f6c780056f0)
 Call ID: 57ee648f-f920-4467-ac3e-9f6c780056f0
  Args:
    type: :Man
    source: Friedrich_August_of_Oldenburg
  AssignClass (1261cf97-90ef-4b4c-8cc4-27b8d2f8c229)
 Call ID: 1261cf97-90ef-4b4c-8cc4-27b8d2f8c229
  Args:
    type: :Person
    source: Friedrich_August_of_Oldenburg
  AddTriple (2ad40728-b882-40b3-8c5c-87a2089f5712)
 Call ID: 2ad40728-b882-40b3-8c5c-87a2089f5712
  Args:
    source: Donata_of_Castell-Rüdenhausen
    target: Friedrich_August_of_Oldenburg
    relation: :hasRelation
  AssignClass (b4aebece-db3c-4fce-b933-acee57805144)
 Call ID: b4aebece-db3c-4fce-b933-acee57805144
  Args:
    type: :Woman
    source: Marie_Cécile_of_Prussia
  AssignClass (7a501e6b-aa74-441e-9a54-e12397223f81)
 Call ID: 7a501e6b-aa74-441e-9a54-e12397223f81
  Args:
    type: :Person
    source: Marie_Cécile_of_Prussia
  AddTriple (b81c3ebf-6aad-4f35-b6c2-e97f36cbdc2f)
 Call ID: b81c3ebf-6aad-4f35-b6c2-e97f36cbdc2f
  Args:
    relation: :hasRelation
    source: Friedrich_August_of_Oldenburg
    target: Marie_Cécile_of_Prussia
  AssignClass (e755d0fd-4b3c-4659-8a5a-3369144948a8)
 Call ID: e755d0fd-4b3c-4659-8a5a-3369144948a8
  Args:
    type: :Woman
    source: Kira_of_Russia
  AssignClass (3ae5e92e-38f7-4784-8538-a6f4ee3064cc)
 Call ID: 3ae5e92e-38f7-4784-8538-a6f4ee3064cc
  Args:
    type: :Person
    source: Kira_of_Russia
  AddTriple (1dccefc2-cb95-4d81-8f17-a3b8b30bf4f0)
 Call ID: 1dccefc2-cb95-4d81-8f17-a3b8b30bf4f0
  Args:
    target: Kira_of_Russia
    source: Georg_Friedrich_Prinz_von_Preussen
    relation: :hasAncestor
  AssignClass (dc892da8-084a-41ed-8d6f-757ac4f84684)
 Call ID: dc892da8-084a-41ed-8d6f-757ac4f84684
  Args:
    type: :Man
    source: Karl_Friedrich_Prince_of_Hohenzollern
  AssignClass (4b1c3b90-821f-4efe-8d1b-5f5395473977)
 Call ID: 4b1c3b90-821f-4efe-8d1b-5f5395473977
  Args:
    type: :Person
    source: Karl_Friedrich_Prince_of_Hohenzollern
  AssignClass (c41ec703-d3c1-4386-b9ac-2a7c2bc8ace9)
 Call ID: c41ec703-d3c1-4386-b9ac-2a7c2bc8ace9
  Args:
    type: :Man
    source: Louis_Ferdinand_of_Prussia_Grandfather
  AssignClass (7c3e298b-3f67-4e48-9d33-8dae2292bc29)
 Call ID: 7c3e298b-3f67-4e48-9d33-8dae2292bc29
  Args:
    type: :Person
    source: Louis_Ferdinand_of_Prussia_Grandfather
  AddTriple (f7bbd742-1af3-4f4d-9429-b24ee3231b3b)
 Call ID: f7bbd742-1af3-4f4d-9429-b24ee3231b3b
  Args:
    source: Louis_Ferdinand_Prinz_von_Preussen
    target: Louis_Ferdinand_of_Prussia_Grandfather
    relation: :hasFather
  AssignClass (8b0c3768-8931-4e4e-8777-29ab459cdf49)
 Call ID: 8b0c3768-8931-4e4e-8777-29ab459cdf49
  Args:
    type: :Man
    source: Friedrich_Wilhelm_Uncle
  AssignClass (0aaa40c2-d6c6-48dd-9407-fe4d3b30e74b)
 Call ID: 0aaa40c2-d6c6-48dd-9407-fe4d3b30e74b
  Args:
    type: :Person
    source: Friedrich_Wilhelm_Uncle
  AddTriple (73c149fd-f9d5-4330-8637-093a80f97c14)
 Call ID: 73c149fd-f9d5-4330-8637-093a80f97c14
  Args:
    relation: :hasFather
    target: Louis_Ferdinand_of_Prussia_Grandfather
    source: Friedrich_Wilhelm_Uncle
  AssignClass (c980a5b8-421a-4bb4-844e-fdef4981dd13)
 Call ID: c980a5b8-421a-4bb4-844e-fdef4981dd13
  Args:
    type: :Man
    source: Michael_Uncle
  AssignClass (576ef7ec-16b4-4585-ab8b-f8cae02f165f)
 Call ID: 576ef7ec-16b4-4585-ab8b-f8cae02f165f
  Args:
    type: :Person
    source: Michael_Uncle
  AddTriple (444714e9-d078-43c8-af34-99ebe75e58a7)
 Call ID: 444714e9-d078-43c8-af34-99ebe75e58a7
  Args:
    source: Michael_Uncle
    target: Louis_Ferdinand_of_Prussia_Grandfather
    relation: :hasFather
  AssignClass (04292b64-103d-4cd0-b02f-b1453b31ee48)
 Call ID: 04292b64-103d-4cd0-b02f-b1453b31ee48
  Args:
    type: :Woman
    source: Sophie_of_Isenburg
  AssignClass (4ce5ca7a-f255-415f-8441-6667066b51f5)
 Call ID: 4ce5ca7a-f255-415f-8441-6667066b51f5
  Args:
    type: :Person
    source: Sophie_of_Isenburg
  AddLiteral (4d5c7508-892b-4788-93b1-0df6373fd43b)
 Call ID: 4d5c7508-892b-4788-93b1-0df6373fd43b
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Georg_Friedrich_Prinz_von_Preussen
    literal_value: 2011
  AddTriple (d3dd5358-562f-4983-8298-4a5c8fb3370f)
 Call ID: d3dd5358-562f-4983-8298-4a5c8fb3370f
  Args:
    relation: :hasRelation
    target: Sophie_of_Isenburg
    source: Georg_Friedrich_Prinz_von_Preussen
  AssignClass (b529c773-fdce-4705-9304-b44ab04d8b5e)
 Call ID: b529c773-fdce-4705-9304-b44ab04d8b5e
  Args:
    type: :Man
    source: Carl_Friedrich_Franz_Alexander
  AssignClass (dd6ce392-228e-4a08-a88f-43bca3d601cd)
 Call ID: dd6ce392-228e-4a08-a88f-43bca3d601cd
  Args:
    type: :Person
    source: Carl_Friedrich_Franz_Alexander
  AssignClass (486c20cb-07dd-4d39-b215-ffa934b7d1c7)
 Call ID: 486c20cb-07dd-4d39-b215-ffa934b7d1c7
  Args:
    type: :Man
    source: Louis_Ferdinand_Christian_Albrecht
  AssignClass (596507ba-c0a0-490e-b2a0-4fddfe6cf765)
 Call ID: 596507ba-c0a0-490e-b2a0-4fddfe6cf765
  Args:
    type: :Person
    source: Louis_Ferdinand_Christian_Albrecht
  AddTriple (61913531-8de1-4229-b36f-7c2ddc0b0059)
 Call ID: 61913531-8de1-4229-b36f-7c2ddc0b0059
  Args:
    relation: :hasFather
    source: Carl_Friedrich_Franz_Alexander
    target: Georg_Friedrich_Prinz_von_Preussen
  AddTriple (62cddcc6-52c3-4415-a616-aabef93c8379)
 Call ID: 62cddcc6-52c3-4415-a616-aabef93c8379
  Args:
    relation: :hasMother
    source: Carl_Friedrich_Franz_Alexander
    target: Sophie_of_Isenburg
  AddTriple (9ee538ac-4cfa-4624-91b1-d2f64394d353)
 Call ID: 9ee538ac-4cfa-4624-91b1-d2f64394d353
  Args:
    relation: :hasFather
    target: Georg_Friedrich_Prinz_von_Preussen
    source: Louis_Ferdinand_Christian_Albrecht
  AddTriple (d7fbb916-c1b7-42e4-b683-ee4430de4355)
 Call ID: d7fbb916-c1b7-42e4-b683-ee4430de4355
  Args:
    relation: :hasMother
    source: Louis_Ferdinand_Christian_Albrecht
    target: Sophie_of_Isenburg
  AssignClass (91409fea-bd0f-4f32-a43f-96c569564f2b)
 Call ID: 91409fea-bd0f-4f32-a43f-96c569564f2b
  Args:
    type: :Man
    source: Heinrich_Albert_Johann_Georg
  AssignClass (7773a2d6-6c7b-48de-a952-107d5ce1e79e)
 Call ID: 7773a2d6-6c7b-48de-a952-107d5ce1e79e
  Args:
    type: :Person
    source: Heinrich_Albert_Johann_Georg
  AddTriple (57a8a1cc-2f68-4398-84f5-a8127c87d44e)
 Call ID: 57a8a1cc-2f68-4398-84f5-a8127c87d44e
  Args:
    source: Heinrich_Albert_Johann_Georg
    target: Georg_Friedrich_Prinz_von_Preussen
    relation: :hasFather
  AddTriple (e8724878-6360-4442-8415-4fc8d98b8573)
 Call ID: e8724878-6360-4442-8415-4fc8d98b8573
  Args:
    relation: :hasMother
    source: Heinrich_Albert_Johann_Georg
    target: Sophie_of_Isenburg
  Finish (1938ebdf-3e8e-4289-a3e9-6399c3e13574)
 Call ID: 1938ebdf-3e8e-4289-a3e9-6399c3e13574
  Args: