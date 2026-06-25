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
  AssignClass (f4a233bd-c268-4c70-8723-6c7df716f545)
 Call ID: f4a233bd-c268-4c70-8723-6c7df716f545
  Args:
    type: :Man
    source: Georg_Friedrich_Prinz_von_Preussen
  AssignClass (aa427af7-f9ba-42b0-8fcc-444b387d6530)
 Call ID: aa427af7-f9ba-42b0-8fcc-444b387d6530
  Args:
    source: Georg_Friedrich_Prinz_von_Preussen
    type: :Person
  AddLiteral (be953b5a-54b7-49d6-acec-681a2947049c)
 Call ID: be953b5a-54b7-49d6-acec-681a2947049c
  Args:
    literal_value: 1976
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Georg_Friedrich_Prinz_von_Preussen
  AssignClass (5daa1a6b-4281-4aaa-9ce6-1da698fdbc21)
 Call ID: 5daa1a6b-4281-4aaa-9ce6-1da698fdbc21
  Args:
    source: Louis_Ferdinand_Prinz_von_Preussen
    type: :Man
  AssignClass (2fde62ae-fbe8-4040-92fc-29d794dca3df)
 Call ID: 2fde62ae-fbe8-4040-92fc-29d794dca3df
  Args:
    type: :Person
    source: Louis_Ferdinand_Prinz_von_Preussen
  AddLiteral (3f7499e8-63d0-4bbe-a3eb-891109f58a43)
 Call ID: 3f7499e8-63d0-4bbe-a3eb-891109f58a43
  Args:
    literal_value: 1944
    source: Louis_Ferdinand_Prinz_von_Preussen
    relation: :hasBirthYear
    literal_type: xsd:integer
  AddLiteral (065fe5b1-c1b2-42fe-995f-ec60b566b8aa)
 Call ID: 065fe5b1-c1b2-42fe-995f-ec60b566b8aa
  Args:
    literal_value: 1977
    source: Louis_Ferdinand_Prinz_von_Preussen
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (04b6c020-ef55-43ca-9f3d-f50d74178616)
 Call ID: 04b6c020-ef55-43ca-9f3d-f50d74178616
  Args:
    type: :Woman
    source: Donata_of_Castell_Rüdenhausen
  AssignClass (ad792e5c-3184-4caf-8b17-d06bb455d030)
 Call ID: ad792e5c-3184-4caf-8b17-d06bb455d030
  Args:
    source: Donata_of_Castell_Rüdenhausen
    type: :Person
  AddLiteral (d380d3ce-3c95-4e34-83fa-a33725273241)
 Call ID: d380d3ce-3c95-4e34-83fa-a33725273241
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: Donata_of_Castell_Rüdenhausen
    literal_value: 1950
  AddLiteral (2dc9ff4a-0abe-4253-9f98-3763c62871ad)
 Call ID: 2dc9ff4a-0abe-4253-9f98-3763c62871ad
  Args:
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Donata_of_Castell_Rüdenhausen
    literal_value: 2015
  AddTriple (3ea01b62-39c5-40c8-8279-01b2dc0ce047)
 Call ID: 3ea01b62-39c5-40c8-8279-01b2dc0ce047
  Args:
    source: Georg_Friedrich_Prinz_von_Preussen
    relation: :hasFather
    target: Louis_Ferdinand_Prinz_von_Preussen
  AddTriple (5150666a-5937-4562-9798-c4d18b1245e4)
 Call ID: 5150666a-5937-4562-9798-c4d18b1245e4
  Args:
    source: Georg_Friedrich_Prinz_von_Preussen
    relation: :hasMother
    target: Donata_of_Castell_Rüdenhausen
  AssignClass (9b1f004d-6d27-40a3-9b32-d82d5f4fe1b5)
 Call ID: 9b1f004d-6d27-40a3-9b32-d82d5f4fe1b5
  Args:
    source: Wilhelm_II
    type: :Man
  AssignClass (68602af0-e2b8-43ab-8a4d-962de4e6bb69)
 Call ID: 68602af0-e2b8-43ab-8a4d-962de4e6bb69
  Args:
    source: Wilhelm_II
    type: :Person
  AddTriple (8b8c4c7f-4f59-467a-bffe-6f21f9d44ae7)
 Call ID: 8b8c4c7f-4f59-467a-bffe-6f21f9d44ae7
  Args:
    source: Georg_Friedrich_Prinz_von_Preussen
    relation: :hasAncestor
    target: Wilhelm_II
  AssignClass (636269f4-f459-4b03-801b-043efc1bdbb1)
 Call ID: 636269f4-f459-4b03-801b-043efc1bdbb1
  Args:
    type: :Man
    source: Friedrich_August_of_Oldenburg
  AssignClass (52e8c631-1097-4c18-8d0f-c6d22ad422c5)
 Call ID: 52e8c631-1097-4c18-8d0f-c6d22ad422c5
  Args:
    source: Friedrich_August_of_Oldenburg
    type: :Person
  AddTriple (c328bc82-f7d4-474b-a701-0456c1b61366)
 Call ID: c328bc82-f7d4-474b-a701-0456c1b61366
  Args:
    target: Friedrich_August_of_Oldenburg
    source: Donata_of_Castell_Rüdenhausen
    relation: :hasRelation
  AssignClass (5358882b-f8e6-416f-af18-bfdeea26845b)
 Call ID: 5358882b-f8e6-416f-af18-bfdeea26845b
  Args:
    type: :Woman
    source: Marie_Cécile_of_Prussia
  AssignClass (8e3f8638-d5ba-4724-845d-57fe09fca8c7)
 Call ID: 8e3f8638-d5ba-4724-845d-57fe09fca8c7
  Args:
    source: Marie_Cécile_of_Prussia
    type: :Person
  AddTriple (fc5dddd9-4e9e-41fd-8f61-8f63ec3513f0)
 Call ID: fc5dddd9-4e9e-41fd-8f61-8f63ec3513f0
  Args:
    target: Marie_Cécile_of_Prussia
    relation: :hasRelation
    source: Friedrich_August_of_Oldenburg
  AssignClass (4a2a76c2-0054-438e-80cd-c78a73d95edf)
 Call ID: 4a2a76c2-0054-438e-80cd-c78a73d95edf
  Args:
    source: Kira_of_Russia
    type: :Woman
  AssignClass (da8ac4f8-6a10-445b-b267-4d529d212462)
 Call ID: da8ac4f8-6a10-445b-b267-4d529d212462
  Args:
    type: :Person
    source: Kira_of_Russia
  AddTriple (f8c9770f-095d-46d6-baf2-5561b69fda72)
 Call ID: f8c9770f-095d-46d6-baf2-5561b69fda72
  Args:
    relation: :hasMother
    source: Louis_Ferdinand_Prinz_von_Preussen
    target: Kira_of_Russia
  AssignClass (9bb94f1e-d97b-4e56-b59a-f50ddcf3c2e1)
 Call ID: 9bb94f1e-d97b-4e56-b59a-f50ddcf3c2e1
  Args:
    source: Sophie_of_Isenburg
    type: :Woman
  AssignClass (be06be69-b399-4451-82bc-de1e2191fb41)
 Call ID: be06be69-b399-4451-82bc-de1e2191fb41
  Args:
    type: :Person
    source: Sophie_of_Isenburg
  AddTriple (962fe2fe-5a99-4c2a-9057-60f517ba3aa7)
 Call ID: 962fe2fe-5a99-4c2a-9057-60f517ba3aa7
  Args:
    target: Sophie_of_Isenburg
    relation: :hasRelation
    source: Georg_Friedrich_Prinz_von_Preussen
  AddLiteral (6a96f5e3-50ec-4853-b4b3-da9d5e95ea06)
 Call ID: 6a96f5e3-50ec-4853-b4b3-da9d5e95ea06
  Args:
    literal_value: 2011
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: Georg_Friedrich_Prinz_von_Preussen
  AssignClass (0e19c44d-491c-4b87-b63e-0393d556e1cf)
 Call ID: 0e19c44d-491c-4b87-b63e-0393d556e1cf
  Args:
    source: Carl_Friedrich_Franz_Alexander
    type: :Man
  AssignClass (ae3ad17c-fc90-45dc-a428-3894ba7791fe)
 Call ID: ae3ad17c-fc90-45dc-a428-3894ba7791fe
  Args:
    type: :Person
    source: Carl_Friedrich_Franz_Alexander
  AssignClass (b2b2a9d8-fc18-4034-bc15-5a6fb5de9142)
 Call ID: b2b2a9d8-fc18-4034-bc15-5a6fb5de9142
  Args:
    type: :Man
    source: Louis_Ferdinand_Christian_Albrecht
  AssignClass (044b2ab7-8d15-474d-b72e-9bd9709b2943)
 Call ID: 044b2ab7-8d15-474d-b72e-9bd9709b2943
  Args:
    source: Louis_Ferdinand_Christian_Albrecht
    type: :Person
  AddTriple (2f0afb89-e331-4b06-be90-731b2eeb6cd2)
 Call ID: 2f0afb89-e331-4b06-be90-731b2eeb6cd2
  Args:
    target: Georg_Friedrich_Prinz_von_Preussen
    source: Carl_Friedrich_Franz_Alexander
    relation: :hasFather
  AddTriple (6e0e640c-fa81-468d-a71e-bfbc5a37454a)
 Call ID: 6e0e640c-fa81-468d-a71e-bfbc5a37454a
  Args:
    source: Carl_Friedrich_Franz_Alexander
    relation: :hasMother
    target: Sophie_of_Isenburg
  AddTriple (62f3c21f-d53d-4ba5-b1af-14c613069bd1)
 Call ID: 62f3c21f-d53d-4ba5-b1af-14c613069bd1
  Args:
    relation: :hasFather
    source: Louis_Ferdinand_Christian_Albrecht
    target: Georg_Friedrich_Prinz_von_Preussen
  AddTriple (7183cb9b-3de2-435e-baba-734d0759733f)
 Call ID: 7183cb9b-3de2-435e-baba-734d0759733f
  Args:
    relation: :hasMother
    source: Louis_Ferdinand_Christian_Albrecht
    target: Sophie_of_Isenburg
  AssignClass (3ff7eb76-7cd1-47a4-8c2c-13e0010c073d)
 Call ID: 3ff7eb76-7cd1-47a4-8c2c-13e0010c073d
  Args:
    type: :Man
    source: Heinrich_Albert_Johann_Georg
  AssignClass (275925b3-9830-48a0-80df-afc535c8c75d)
 Call ID: 275925b3-9830-48a0-80df-afc535c8c75d
  Args:
    source: Heinrich_Albert_Johann_Georg
    type: :Person
  AddTriple (727e65d7-c55f-49c2-830f-4837880ba24d)
 Call ID: 727e65d7-c55f-49c2-830f-4837880ba24d
  Args:
    relation: :hasFather
    source: Heinrich_Albert_Johann_Georg
    target: Georg_Friedrich_Prinz_von_Preussen
  AddTriple (eb822107-963c-4e23-90f0-863c1b96509a)
 Call ID: eb822107-963c-4e23-90f0-863c1b96509a
  Args:
    relation: :hasMother
    source: Heinrich_Albert_Johann_Georg
    target: Sophie_of_Isenburg
  AssignClass (4bac41f0-70b3-43e4-ab91-fe00acd1b105)
 Call ID: 4bac41f0-70b3-43e4-ab91-fe00acd1b105
  Args:
    source: Friedrich_Wilhelm
    type: :Man
  AssignClass (8432bfaa-4463-4a9e-9a6e-02953bdd3f94)
 Call ID: 8432bfaa-4463-4a9e-9a6e-02953bdd3f94
  Args:
    type: :Person
    source: Friedrich_Wilhelm
  AssignClass (c20f193a-e5e5-4c97-a6df-89e6457ebb24)
 Call ID: c20f193a-e5e5-4c97-a6df-89e6457ebb24
  Args:
    source: Michael
    type: :Man
  AssignClass (c19a5190-78fd-4ede-9165-8c77af4f6112)
 Call ID: c19a5190-78fd-4ede-9165-8c77af4f6112
  Args:
    source: Michael
    type: :Person
  AddTriple (9efc5cfa-5188-4e33-b180-c6320bdcac75)
 Call ID: 9efc5cfa-5188-4e33-b180-c6320bdcac75
  Args:
    relation: :hasFather
    source: Friedrich_Wilhelm
    target: Louis_Ferdinand_Prinz_von_Preussen
  AddTriple (a6af0d86-cd06-4e91-b129-0387cde6785d)
 Call ID: a6af0d86-cd06-4e91-b129-0387cde6785d
  Args:
    relation: :hasFather
    source: Michael
    target: Louis_Ferdinand_Prinz_von_Preussen
  Finish (256b0575-e727-4faa-853a-4cba81eaa30e)
 Call ID: 256b0575-e727-4faa-853a-4cba81eaa30e
  Args: