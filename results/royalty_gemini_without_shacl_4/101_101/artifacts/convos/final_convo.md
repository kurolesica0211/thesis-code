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
Gustav, 7th Prince of Sayn-Wittgenstein-Berleburg (Gustav Frederik Philip Richard; born 12 January 1969), is the eldest child and only son of Princess Benedikte of Denmark and Richard, 6th Prince of Sayn-Wittgenstein-Berleburg.
His first cousin is King Frederik X of Denmark.
Biography

Prince Gustav is the head of the House of Sayn-Wittgenstein-Berleburg, the senior branch of the formerly princely house of Sayn-Wittgenstein.
He resides at Schloss Berleburg-Wittgenstein in the town of Bad Berleburg, in North Rhine-Westphalia, Germany.
He is the son of Prince Richard of Sayn-Wittgenstein-Berleburg and Princess Benedikte of Denmark and has two sisters, Princess Alexandra of Sayn-Wittgenstein-Berleburg and Princess Nathalie of Sayn-Wittgenstein-Berleburg.
The principality and princely title of Sayn-Wittgenstein-Berleburg descended, historically, according to semi-Salic primogeniture.
If Gustav were to die without legitimate issue, the family heritage would devolve upon his father's younger brother, Prince Robin zu Sayn-Wittgenstein-Berleburg.
Gustav was formerly engaged to be married to Elvire Pasté de Rochefort (granddaughter of French Ambassador André Rodocanachi and wife Nada Diplarakou, herself sister of Aliki Diplarakou and grand-aunt of Princess Sibilla of Luxembourg); the engagement was announced on 16 August 2000 and the wedding planned for 12 May 2001 in Paris.
For many years, he resided with his partner, Carina Axelsson, although they were unable to marry due to a clause in Gustav's grandfather's will preventing him from inheriting family property if he marries someone not of Protestant, noble and Aryan descent.
However, on 27 April 2022, the Danish court confirmed that Gustav could marry Axelsson on 3 June 2022, civilly and on 4 June 2022, religiously in Bad Berleburg.
The couple's son, Prince Gustav Albrecht, was born on 26 May 2023 in the United States via surrogacy.
On 26 April 2024, the couple welcomed their second child, a girl, Princess Mafalda, also via surrogacy.
He is the godfather of Count Richard von Pfeil und Klein-Ellguth, son of his sister Alexandra; Konstantin Johannsmann, son of his second sister Nathalie; and Prince Vincent of Denmark, son of his first cousin, Frederik X.


Ancestry




References

External links



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
  AssignClass (53c8bb86-aeb2-47e3-95d8-8910fef9f5b4)
 Call ID: 53c8bb86-aeb2-47e3-95d8-8910fef9f5b4
  Args:
    type: :Man
    source: Gustav_Prince_of_Sayn-Wittgenstein-Berleburg
  AssignClass (1dcf1064-7840-4966-905f-9f0d28b8b8d9)
 Call ID: 1dcf1064-7840-4966-905f-9f0d28b8b8d9
  Args:
    type: :Woman
    source: Princess_Benedikte_of_Denmark
  AssignClass (9eeff1ec-9b20-4fa0-87bc-285e4695862f)
 Call ID: 9eeff1ec-9b20-4fa0-87bc-285e4695862f
  Args:
    type: :Man
    source: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
  AddLiteral (7992c4b4-80fe-47da-93a7-aea334cf06b1)
 Call ID: 7992c4b4-80fe-47da-93a7-aea334cf06b1
  Args:
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
    literal_value: 1969
    source: Gustav_Prince_of_Sayn-Wittgenstein-Berleburg
  AddTriple (625eb13d-e87e-4d8b-bd81-0ce22a2837ef)
 Call ID: 625eb13d-e87e-4d8b-bd81-0ce22a2837ef
  Args:
    target: Princess_Benedikte_of_Denmark
    source: Gustav_Prince_of_Sayn-Wittgenstein-Berleburg
    relation: :hasMother
  AddTriple (5e71c61d-00af-4420-aba8-5add83ebe106)
 Call ID: 5e71c61d-00af-4420-aba8-5add83ebe106
  Args:
    source: Gustav_Prince_of_Sayn-Wittgenstein-Berleburg
    relation: :hasFather
    target: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
  AssignClass (b537f721-17c1-4203-b1ea-a294b5d99f76)
 Call ID: b537f721-17c1-4203-b1ea-a294b5d99f76
  Args:
    type: :Woman
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AssignClass (3d3c601c-817c-465c-b550-52472dab1765)
 Call ID: 3d3c601c-817c-465c-b550-52472dab1765
  Args:
    type: :Woman
    source: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
  AddTriple (80965e03-1ae8-4612-a48b-8c1202ded6a3)
 Call ID: 80965e03-1ae8-4612-a48b-8c1202ded6a3
  Args:
    relation: :hasSister
    source: Gustav_Prince_of_Sayn-Wittgenstein-Berleburg
    target: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
  AddTriple (e30fc0c2-7809-4b4c-b39f-3f7021203a0f)
 Call ID: e30fc0c2-7809-4b4c-b39f-3f7021203a0f
  Args:
    source: Gustav_Prince_of_Sayn-Wittgenstein-Berleburg
    relation: :hasSister
    target: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
  AddTriple (aab4b7cf-9897-4b9b-a843-993217d68431)
 Call ID: aab4b7cf-9897-4b9b-a843-993217d68431
  Args:
    relation: :hasFather
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    target: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
  AddTriple (e1b29059-9ea6-4b46-9096-c5c522a4b1e9)
 Call ID: e1b29059-9ea6-4b46-9096-c5c522a4b1e9
  Args:
    target: Princess_Benedikte_of_Denmark
    source: Princess_Alexandra_of_Sayn-Wittgenstein-Berleburg
    relation: :hasMother
  AddTriple (c3edc6d5-f390-4f94-a6e0-7d18bbea5a8b)
 Call ID: c3edc6d5-f390-4f94-a6e0-7d18bbea5a8b
  Args:
    target: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
    relation: :hasFather
    source: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
  AddTriple (af717a1f-d128-4cb7-921b-b4514ad7be0a)
 Call ID: af717a1f-d128-4cb7-921b-b4514ad7be0a
  Args:
    target: Princess_Benedikte_of_Denmark
    relation: :hasMother
    source: Princess_Nathalie_of_Sayn-Wittgenstein-Berleburg
  AssignClass (0cfc5188-98f7-4dbc-aa0f-c6f34930423a)
 Call ID: 0cfc5188-98f7-4dbc-aa0f-c6f34930423a
  Args:
    type: :Man
    source: King_Frederik_X_of_Denmark
  AddTriple (01336abe-025c-4e2c-8d54-d97429ee75e8)
 Call ID: 01336abe-025c-4e2c-8d54-d97429ee75e8
  Args:
    source: Gustav_Prince_of_Sayn-Wittgenstein-Berleburg
    relation: :isBloodrelationOf
    target: King_Frederik_X_of_Denmark
  AssignClass (6525d369-27da-423d-93ca-d025dd3ef45a)
 Call ID: 6525d369-27da-423d-93ca-d025dd3ef45a
  Args:
    type: :Man
    source: Prince_Robin_zu_Sayn-Wittgenstein-Berleburg
  AddTriple (e9063e03-13e1-45f1-99e1-007d593e5f4e)
 Call ID: e9063e03-13e1-45f1-99e1-007d593e5f4e
  Args:
    source: Richard_6th_Prince_of_Sayn-Wittgenstein-Berleburg
    relation: :hasBrother
    target: Prince_Robin_zu_Sayn-Wittgenstein-Berleburg
  AssignClass (8f422814-835d-434a-9c08-10a105d0e261)
 Call ID: 8f422814-835d-434a-9c08-10a105d0e261
  Args:
    type: :Woman
    source: Carina_Axelsson
  AssignClass (4bcf6223-50ec-4754-b2e0-37831e603291)
 Call ID: 4bcf6223-50ec-4754-b2e0-37831e603291
  Args:
    type: :Man
    source: Prince_Gustav_Albrecht
  AssignClass (12f4855e-eee4-4f6e-b924-d003efff23c5)
 Call ID: 12f4855e-eee4-4f6e-b924-d003efff23c5
  Args:
    type: :Woman
    source: Princess_Mafalda
  AddTriple (60392a09-22a8-4e6b-bd9b-a94d2fe5d2be)
 Call ID: 60392a09-22a8-4e6b-bd9b-a94d2fe5d2be
  Args:
    source: Prince_Gustav_Albrecht
    relation: :hasFather
    target: Gustav_Prince_of_Sayn-Wittgenstein-Berleburg
  AddTriple (8c52d0bf-36c6-48bf-a75c-4beef934cf1f)
 Call ID: 8c52d0bf-36c6-48bf-a75c-4beef934cf1f
  Args:
    relation: :hasMother
    source: Prince_Gustav_Albrecht
    target: Carina_Axelsson
  AddTriple (93ead198-ebe6-4cc0-b40f-d903ce8f3720)
 Call ID: 93ead198-ebe6-4cc0-b40f-d903ce8f3720
  Args:
    relation: :hasFather
    source: Princess_Mafalda
    target: Gustav_Prince_of_Sayn-Wittgenstein-Berleburg
  AddTriple (80384103-0bd9-45a1-bf59-aaf6b66c3a7d)
 Call ID: 80384103-0bd9-45a1-bf59-aaf6b66c3a7d
  Args:
    source: Princess_Mafalda
    relation: :hasMother
    target: Carina_Axelsson
  Finish (7078626e-723b-4950-b467-4cf4fc5ec523)
 Call ID: 7078626e-723b-4950-b467-4cf4fc5ec523
  Args: