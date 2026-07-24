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
  AssignClass (679361f6-8847-40c0-94f3-db01d163ed5f)
 Call ID: 679361f6-8847-40c0-94f3-db01d163ed5f
  Args:
    source: Georg_Friedrich_Prinz_von_Preussen
    type: :Man
  AssignClass (2a2197ae-e4b4-43c4-9258-adde1bcfb215)
 Call ID: 2a2197ae-e4b4-43c4-9258-adde1bcfb215
  Args:
    source: Louis_Ferdinand_Prinz_von_Preussen
    type: :Man
  AssignClass (e90b2838-f7dd-46df-a1d9-f2fd366a5169)
 Call ID: e90b2838-f7dd-46df-a1d9-f2fd366a5169
  Args:
    source: Donata_of_Castell-Rüdenhausen
    type: :Woman
  AssignClass (061f5db8-3904-46c8-ac2e-79f5057a363c)
 Call ID: 061f5db8-3904-46c8-ac2e-79f5057a363c
  Args:
    source: Wilhelm_II
    type: :Man
  AssignClass (4191335a-5ab0-45d1-a816-c90ddd10a173)
 Call ID: 4191335a-5ab0-45d1-a816-c90ddd10a173
  Args:
    type: :Man
    source: Friedrich_August_of_Oldenburg
  AssignClass (e2aa1506-220a-412e-937a-49149b750fed)
 Call ID: e2aa1506-220a-412e-937a-49149b750fed
  Args:
    source: Marie_Cécile_of_Prussia
    type: :Woman
  AssignClass (4d9bf5c3-e453-4617-9810-afa923eda2c8)
 Call ID: 4d9bf5c3-e453-4617-9810-afa923eda2c8
  Args:
    type: :Woman
    source: Kira_of_Russia
  AssignClass (85c765c1-e69a-4520-8132-3dae66acf38b)
 Call ID: 85c765c1-e69a-4520-8132-3dae66acf38b
  Args:
    type: :Woman
    source: Sophie_of_Isenburg
  AssignClass (3ac06c6e-2f0a-486b-bc2e-a3f0c389d400)
 Call ID: 3ac06c6e-2f0a-486b-bc2e-a3f0c389d400
  Args:
    source: Carl_Friedrich_Franz_Alexander
    type: :Man
  AssignClass (dfe7109f-d736-45c3-af0f-92bf8c05d49b)
 Call ID: dfe7109f-d736-45c3-af0f-92bf8c05d49b
  Args:
    type: :Man
    source: Louis_Ferdinand_Christian_Albrecht
  AssignClass (652873a8-97fc-4b2d-8ad2-bb6077167d67)
 Call ID: 652873a8-97fc-4b2d-8ad2-bb6077167d67
  Args:
    type: :Man
    source: Heinrich_Albert_Johann_Georg
  AssignClass (8329b5ef-d62d-4c59-ba55-667b7dc637f9)
 Call ID: 8329b5ef-d62d-4c59-ba55-667b7dc637f9
  Args:
    source: Friedrich_Wilhelm
    type: :Man
  AssignClass (920c600d-c187-4a5d-abd5-3df523211b95)
 Call ID: 920c600d-c187-4a5d-abd5-3df523211b95
  Args:
    source: Michael
    type: :Man
  AddLiteral (4b39b286-9ab3-4a01-99fb-dd0ef218be1b)
 Call ID: 4b39b286-9ab3-4a01-99fb-dd0ef218be1b
  Args:
    relation: :hasBirthYear
    literal_value: 1976
    source: Georg_Friedrich_Prinz_von_Preussen
    literal_type: xsd:integer
  AddTriple (e8760d87-768c-4ea1-8aad-0f82f90d5303)
 Call ID: e8760d87-768c-4ea1-8aad-0f82f90d5303
  Args:
    source: Georg_Friedrich_Prinz_von_Preussen
    relation: :hasFather
    target: Louis_Ferdinand_Prinz_von_Preussen
  AddTriple (341dc5ee-e82f-423e-8388-d56085072387)
 Call ID: 341dc5ee-e82f-423e-8388-d56085072387
  Args:
    target: Donata_of_Castell-Rüdenhausen
    source: Georg_Friedrich_Prinz_von_Preussen
    relation: :hasMother
  AddTriple (4615cde2-6686-4b3a-b625-d8558721b303)
 Call ID: 4615cde2-6686-4b3a-b625-d8558721b303
  Args:
    target: Louis_Ferdinand_of_Prussia_Grandfather
    relation: :hasFather
    source: Louis_Ferdinand_Prinz_von_Preussen
  AssignClass (67843997-1b63-4ca5-97d2-e1f740957cf8)
 Call ID: 67843997-1b63-4ca5-97d2-e1f740957cf8
  Args:
    type: :Man
    source: Louis_Ferdinand_of_Prussia_Grandfather
  AddTriple (656d5714-dc92-4860-93cd-5238ea63f930)
 Call ID: 656d5714-dc92-4860-93cd-5238ea63f930
  Args:
    relation: :hasMother
    source: Georg_Friedrich_Prinz_von_Preussen
    target: Donata_of_Castell-Rüdenhausen
  AddTriple (566ac08a-b007-4b5f-bbb9-eb911a8e3b9b)
 Call ID: 566ac08a-b007-4b5f-bbb9-eb911a8e3b9b
  Args:
    target: Donata_of_Castell-Rüdenhausen
    relation: :hasMother
    source: Georg_Friedrich_Prinz_von_Preussen
  AddTriple (6224f35a-7646-451c-88bd-9eeca5c46ea3)
 Call ID: 6224f35a-7646-451c-88bd-9eeca5c46ea3
  Args:
    target: Louis_Ferdinand_Prinz_von_Preussen
    source: Georg_Friedrich_Prinz_von_Preussen
    relation: :hasFather
  AddTriple (5ee9fef1-f278-413c-98c2-5e51c4044e0a)
 Call ID: 5ee9fef1-f278-413c-98c2-5e51c4044e0a
  Args:
    relation: :hasMother
    source: Georg_Friedrich_Prinz_von_Preussen
    target: Donata_of_Castell-Rüdenhausen
  AddTriple (d0cc20e6-9c06-480c-8859-c38cbf747da6)
 Call ID: d0cc20e6-9c06-480c-8859-c38cbf747da6
  Args:
    relation: :hasFather
    source: Carl_Friedrich_Franz_Alexander
    target: Georg_Friedrich_Prinz_von_Preussen
  AddTriple (f8453c66-7bfd-41ac-9e44-46c1fbe0e58b)
 Call ID: f8453c66-7bfd-41ac-9e44-46c1fbe0e58b
  Args:
    relation: :hasMother
    source: Carl_Friedrich_Franz_Alexander
    target: Sophie_of_Isenburg
  AddTriple (eaae4daf-ea14-46e5-b9b4-8d7bf5cee1bd)
 Call ID: eaae4daf-ea14-46e5-b9b4-8d7bf5cee1bd
  Args:
    target: Georg_Friedrich_Prinz_von_Preussen
    source: Louis_Ferdinand_Christian_Albrecht
    relation: :hasFather
  AddTriple (82af994a-729a-451e-9c24-45e2997e091a)
 Call ID: 82af994a-729a-451e-9c24-45e2997e091a
  Args:
    relation: :hasMother
    source: Louis_Ferdinand_Christian_Albrecht
    target: Sophie_of_Isenburg
  AddTriple (d3baf26e-752a-4fd3-bebc-7670c0770477)
 Call ID: d3baf26e-752a-4fd3-bebc-7670c0770477
  Args:
    target: Georg_Friedrich_Prinz_von_Preussen
    source: Heinrich_Albert_Johann_Georg
    relation: :hasFather
  AddTriple (2fad3a94-edd0-4759-b50b-3c42a2af7954)
 Call ID: 2fad3a94-edd0-4759-b50b-3c42a2af7954
  Args:
    target: Sophie_of_Isenburg
    relation: :hasMother
    source: Heinrich_Albert_Johann_Georg
  AddTriple (73960f39-43b0-4a5d-97e9-c81a3377eeba)
 Call ID: 73960f39-43b0-4a5d-97e9-c81a3377eeba
  Args:
    target: Louis_Ferdinand_Christian_Albrecht
    source: Carl_Friedrich_Franz_Alexander
    relation: :isBrotherOf
  AddTriple (584e2994-577d-45ed-8a43-ae4b911829f3)
 Call ID: 584e2994-577d-45ed-8a43-ae4b911829f3
  Args:
    target: Heinrich_Albert_Johann_Georg
    source: Carl_Friedrich_Franz_Alexander
    relation: :isBrotherOf
  AddTriple (3f55c0e3-ffd0-4fce-a153-b2d58a5d8d22)
 Call ID: 3f55c0e3-ffd0-4fce-a153-b2d58a5d8d22
  Args:
    target: Heinrich_Albert_Johann_Georg
    relation: :isBrotherOf
    source: Louis_Ferdinand_Christian_Albrecht
  AddTriple (cd36423a-b69f-40da-9579-f13fc9bed1a2)
 Call ID: cd36423a-b69f-40da-9579-f13fc9bed1a2
  Args:
    target: Louis_Ferdinand_of_Prussia_Grandfather
    relation: :hasFather
    source: Friedrich_Wilhelm
  AddTriple (50eb8f88-e223-4ca2-8132-5d07b264c113)
 Call ID: 50eb8f88-e223-4ca2-8132-5d07b264c113
  Args:
    relation: :hasFather
    source: Michael
    target: Louis_Ferdinand_of_Prussia_Grandfather
  Finish (d621de73-f4a4-435f-946f-61b080ec4088)
 Call ID: d621de73-f4a4-435f-946f-61b080ec4088
  Args: