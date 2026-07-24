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
Queen Anne-Marie


Queen Sofía of Spain


Marina, consort of Prince Michael


Princess Alexandra Elli Francisca Maria of Greece (born 15 October 1968), known professionally as Alexandra Mirzayantz, is a Greek artist, art collector, arts patron, and child life specialist.
As the daughter of Prince Michael of Greece and Denmark, she is a member of the Greek royal family and a relative of the Danish royal family.
A morganatic descendant of the House of Glücksburg, she is not a Danish princess nor is she entitled to the style Royal Highness as other members of the Greek royal family are.
She was born a princess of Greece entitled to the style Your Highness, and was excluded from the line of succession to the Greek throne.
She is a second cousin of Constantine II of Greece, who reigned as King of the Hellenes until the monarchy was abolished in 1973.
Early life and family

Princess Alexandra was born in Athens on 15 October 1968.
She is the daughter of the historian Prince Michael of Greece and Denmark and the artist Marina Karella.
She is the older sister of Princess Olga.
She is a great-granddaughter of George I of Greece and Olga Constantinovna of Russia.
She is also a great-granddaughter of Prince Jean, Duke of Guise and a great-great-granddaughter of Christian IX of Denmark.
As Princess Alexandra's parents' marriage is morganatic, and therefore non-dynastic, she is a Greek princess by birth but not a Danish princess, uses the style Your Highness instead of Her Royal Highness, and is excluded from the line of succession to the former Greek throne.
On 29 July 1973, Princess Alexandra's second cousin, Constantine II of Greece, was deposed and the Greek monarchy was abolished.
Career

Princess Alexandra is a certified child life specialist.
Princess Alexandra and her husband are patrons of the New York art scene.
She owns a portrait of her grandfather, Prince Christopher of Greece and Denmark, painted by Philip de László in 1919, as part of her collection.
Personal life

Princess Alexandra married the perfumer Nicolas Mirzayantz on 27 June 1998 in Torcello.
She attended the funeral of her father, Prince Michael on 1 August 2024, and was seen with other Greek royal family members, including Princess Olga, Queen Anne-Marie of Greece, Queen Sofía of Spain, and Crown Prince Pavlos.



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
  AssignClass (e4552c77-3f19-48bd-8868-3583d428deb8)
 Call ID: e4552c77-3f19-48bd-8868-3583d428deb8
  Args:
    source: :PrincessAlexandra
    type: :Person
  AssignClass (4528e439-abb0-4739-bc0f-50e5df80aae9)
 Call ID: 4528e439-abb0-4739-bc0f-50e5df80aae9
  Args:
    source: :PrincessAlexandra
    type: :Woman
  AssignClass (46d50804-89a8-4972-b9a2-1342e7ebe613)
 Call ID: 46d50804-89a8-4972-b9a2-1342e7ebe613
  Args:
    type: :Person
    source: :PrinceMichael
  AssignClass (94a9fc29-9a2d-4052-aee5-79f766af6fa7)
 Call ID: 94a9fc29-9a2d-4052-aee5-79f766af6fa7
  Args:
    type: :Man
    source: :PrinceMichael
  AssignClass (e0d558b9-f10e-4b00-8684-5770e15f03ee)
 Call ID: e0d558b9-f10e-4b00-8684-5770e15f03ee
  Args:
    type: :Person
    source: :MarinaKarella
  AssignClass (2a137cf4-4484-476d-a368-d0b26bdad3b2)
 Call ID: 2a137cf4-4484-476d-a368-d0b26bdad3b2
  Args:
    type: :Woman
    source: :MarinaKarella
  AssignClass (f0d1e8f4-8267-4293-ac1d-eea8477c0af9)
 Call ID: f0d1e8f4-8267-4293-ac1d-eea8477c0af9
  Args:
    source: :PrincessOlga
    type: :Person
  AssignClass (cd959682-b910-4b87-b637-ff1571ca678d)
 Call ID: cd959682-b910-4b87-b637-ff1571ca678d
  Args:
    source: :PrincessOlga
    type: :Woman
  AssignClass (7cd1f2e7-f7b0-4634-bbda-b261278f7d46)
 Call ID: 7cd1f2e7-f7b0-4634-bbda-b261278f7d46
  Args:
    source: :NicolasMirzayantz
    type: :Person
  AssignClass (c717d67d-90f3-4eac-96f4-10b46f3c13fe)
 Call ID: c717d67d-90f3-4eac-96f4-10b46f3c13fe
  Args:
    type: :Man
    source: :NicolasMirzayantz
  AssignClass (6c1d1097-7af9-4331-9649-2fcdc0fcc64f)
 Call ID: 6c1d1097-7af9-4331-9649-2fcdc0fcc64f
  Args:
    source: :GeorgeIOfGreece
    type: :Person
  AssignClass (2e21bf05-1286-4c64-ae44-cbea8d8d8222)
 Call ID: 2e21bf05-1286-4c64-ae44-cbea8d8d8222
  Args:
    source: :GeorgeIOfGreece
    type: :Man
  AssignClass (99f5aa24-38cb-460d-b602-44ba7333d853)
 Call ID: 99f5aa24-38cb-460d-b602-44ba7333d853
  Args:
    type: :Person
    source: :OlgaConstantinovnaOfRussia
  AssignClass (0f1fe514-3123-4d4b-b746-074e7cee5642)
 Call ID: 0f1fe514-3123-4d4b-b746-074e7cee5642
  Args:
    source: :OlgaConstantinovnaOfRussia
    type: :Woman
  AssignClass (51b76195-b021-4143-9637-d198bf3aa139)
 Call ID: 51b76195-b021-4143-9637-d198bf3aa139
  Args:
    type: :Person
    source: :PrinceJeanDukeOfGuise
  AssignClass (16baa9cd-c97e-41ba-9061-4fe24098bcea)
 Call ID: 16baa9cd-c97e-41ba-9061-4fe24098bcea
  Args:
    type: :Man
    source: :PrinceJeanDukeOfGuise
  AssignClass (a350c53a-8182-4126-9bb3-1b357d6c8fe3)
 Call ID: a350c53a-8182-4126-9bb3-1b357d6c8fe3
  Args:
    source: :ChristianIXOfDenmark
    type: :Person
  AssignClass (4d776834-b1ae-46ab-b237-cb864c9604e4)
 Call ID: 4d776834-b1ae-46ab-b237-cb864c9604e4
  Args:
    source: :ChristianIXOfDenmark
    type: :Man
  AssignClass (65e95ae7-4dd6-4dc3-9312-b4a14e26bd4b)
 Call ID: 65e95ae7-4dd6-4dc3-9312-b4a14e26bd4b
  Args:
    type: :Person
    source: :PrinceChristopherOfGreeceAndDenmark
  AssignClass (7f181810-cda1-4c10-a3a6-e4a536472641)
 Call ID: 7f181810-cda1-4c10-a3a6-e4a536472641
  Args:
    type: :Man
    source: :PrinceChristopherOfGreeceAndDenmark
  AssignClass (db15533d-95dd-4695-be20-6d40e452ca91)
 Call ID: db15533d-95dd-4695-be20-6d40e452ca91
  Args:
    source: :ConstantineIIOfGreece
    type: :Person
  AssignClass (5856b4a0-543b-4c0b-9984-03b90604a804)
 Call ID: 5856b4a0-543b-4c0b-9984-03b90604a804
  Args:
    type: :Man
    source: :ConstantineIIOfGreece
  AssignClass (c196d175-eafb-4ec9-b2e9-979328bdec7e)
 Call ID: c196d175-eafb-4ec9-b2e9-979328bdec7e
  Args:
    source: :QueenAnneMarie
    type: :Person
  AssignClass (1963c1c8-6b66-49ef-8c63-e4ddadc7b437)
 Call ID: 1963c1c8-6b66-49ef-8c63-e4ddadc7b437
  Args:
    source: :QueenAnneMarie
    type: :Woman
  AssignClass (da405d08-0a70-44e8-afd2-f0a7bfd8b9a1)
 Call ID: da405d08-0a70-44e8-afd2-f0a7bfd8b9a1
  Args:
    source: :QueenSofiaOfSpain
    type: :Person
  AssignClass (c95ca330-6872-4c5b-bcec-466387a18f29)
 Call ID: c95ca330-6872-4c5b-bcec-466387a18f29
  Args:
    type: :Woman
    source: :QueenSofiaOfSpain
  AssignClass (44d8294a-88cf-4614-b7ac-08ad896d2d07)
 Call ID: 44d8294a-88cf-4614-b7ac-08ad896d2d07
  Args:
    source: :CrownPrincePavlos
    type: :Person
  AssignClass (ed9e1da7-eedf-445e-b305-987aef72eec3)
 Call ID: ed9e1da7-eedf-445e-b305-987aef72eec3
  Args:
    source: :CrownPrincePavlos
    type: :Man
  AddLiteral (d05b2d93-6954-4439-926c-7341387beb2b)
 Call ID: d05b2d93-6954-4439-926c-7341387beb2b
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :PrincessAlexandra
    literal_value: 1968
  AddLiteral (4a60e6f0-1bea-422c-931a-dbc28ed0bf5b)
 Call ID: 4a60e6f0-1bea-422c-931a-dbc28ed0bf5b
  Args:
    literal_value: Alexandra Mirzayantz
    source: :PrincessAlexandra
    literal_type: xsd:string
    relation: :knownAs
  AddTriple (18a4c684-b751-4c3f-aeae-da8bb2f66110)
 Call ID: 18a4c684-b751-4c3f-aeae-da8bb2f66110
  Args:
    source: :PrincessAlexandra
    target: :PrinceMichael
    relation: :hasFather
  AddTriple (261dd441-4f11-4e8b-9c65-b7d94ee1a668)
 Call ID: 261dd441-4f11-4e8b-9c65-b7d94ee1a668
  Args:
    relation: :hasMother
    source: :PrincessAlexandra
    target: :MarinaKarella
  AddTriple (8dc9e7fa-65b2-49d8-98e5-a4aa807b51c7)
 Call ID: 8dc9e7fa-65b2-49d8-98e5-a4aa807b51c7
  Args:
    relation: :hasSister
    source: :PrincessAlexandra
    target: :PrincessOlga
  AddTriple (b4d67d18-2419-4521-8671-b5ea87d8f8a2)
 Call ID: b4d67d18-2419-4521-8671-b5ea87d8f8a2
  Args:
    source: :PrincessOlga
    target: :PrincessAlexandra
    relation: :isSisterOf
  AddTriple (2f287141-52d8-43f9-9333-e66dce2af97c)
 Call ID: 2f287141-52d8-43f9-9333-e66dce2af97c
  Args:
    source: :PrinceMichael
    target: :PrincessAlexandra
    relation: :isFatherOf
  AddTriple (9af925fb-594c-4931-92eb-b24ae6e550f2)
 Call ID: 9af925fb-594c-4931-92eb-b24ae6e550f2
  Args:
    source: :MarinaKarella
    target: :PrincessAlexandra
    relation: :isMotherOf
  AddTriple (ab014664-b9e7-4598-a4ad-60eb756b577b)
 Call ID: ab014664-b9e7-4598-a4ad-60eb756b577b
  Args:
    relation: :isFatherOf
    source: :PrinceMichael
    target: :PrincessOlga
  AddTriple (baa79f4b-f295-4139-aaf8-acc71775e2ec)
 Call ID: baa79f4b-f295-4139-aaf8-acc71775e2ec
  Args:
    relation: :isMotherOf
    source: :MarinaKarella
    target: :PrincessOlga
  AddTriple (f56b6120-efba-48f6-a675-2310bb855d35)
 Call ID: f56b6120-efba-48f6-a675-2310bb855d35
  Args:
    source: :PrincessOlga
    target: :PrinceMichael
    relation: :hasFather
  AddTriple (24e446f0-5d79-4e3c-b725-22aed183cc82)
 Call ID: 24e446f0-5d79-4e3c-b725-22aed183cc82
  Args:
    source: :PrincessOlga
    target: :MarinaKarella
    relation: :hasMother
  AddTriple (68617f06-c2fb-4af3-aba4-5895cbb249a6)
 Call ID: 68617f06-c2fb-4af3-aba4-5895cbb249a6
  Args:
    source: :PrinceChristopherOfGreeceAndDenmark
    target: :PrinceMichael
    relation: :hasFather
  AddTriple (88854b1a-a892-4861-9519-281252a199dd)
 Call ID: 88854b1a-a892-4861-9519-281252a199dd
  Args:
    relation: :isFatherOf
    source: :PrinceChristopherOfGreeceAndDenmark
    target: :PrinceMichael
  AddTriple (ee2e53a8-bd3b-4338-b6e1-80e8796ef8c7)
 Call ID: ee2e53a8-bd3b-4338-b6e1-80e8796ef8c7
  Args:
    source: :PrinceMichael
    target: :PrincessAlexandra
    relation: :isFatherOf
  AddTriple (dbf65e17-a4a3-4238-a8ba-8735b7bf59bb)
 Call ID: dbf65e17-a4a3-4238-a8ba-8735b7bf59bb
  Args:
    source: :PrincessAlexandra
    target: :PrinceMichael
    relation: :hasFather
  AddTriple (8365114a-d88e-44a3-938f-5dcf0a94ee2e)
 Call ID: 8365114a-d88e-44a3-938f-5dcf0a94ee2e
  Args:
    relation: :isFatherOf
    source: :PrinceMichael
    target: :PrincessOlga
  AddTriple (5ac56bf0-b506-4b2a-a87e-c0e3d3c79df7)
 Call ID: 5ac56bf0-b506-4b2a-a87e-c0e3d3c79df7
  Args:
    relation: :hasFather
    source: :PrincessOlga
    target: :PrinceMichael
  AddTriple (91e6f494-53ec-45fd-b64f-355f67fb3fc7)
 Call ID: 91e6f494-53ec-45fd-b64f-355f67fb3fc7
  Args:
    source: :PrincessAlexandra
    target: :NicolasMirzayantz
    relation: :hasRelation
  AddLiteral (0de67ab5-1613-4b18-b34b-e2117b2efddd)
 Call ID: 0de67ab5-1613-4b18-b34b-e2117b2efddd
  Args:
    source: :PrincessAlexandra
    literal_value: 1998
    literal_type: xsd:integer
    relation: :hasMarriageYear
  Finish (2ae3cd98-b6b6-474e-a3ce-be2d3060247d)
 Call ID: 2ae3cd98-b6b6-474e-a3ce-be2d3060247d
  Args: