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
Lady Mary Cecilia Colman (née Bowes-Lyon; 30 January 1932 – 2 January 2021) was an English socialite, philanthropist, and extra lady-in-waiting to Princess Alexandra, The Honourable Lady Ogilvy.
The daughter of Michael Bowes-Lyon and Elizabeth Margaret Cator, her paternal aunt was Queen Elizabeth
The Queen Mother, and she was thus a first cousin of Queen Elizabeth II and Princess Margaret, Countess of Snowdon.
Early life

Mary Cecilia Bowes-Lyon was born on 30 January 1932 at Gastlings, the Bowes-Lyon family home in Biggleswade, Bedfordshire.
Her father, Michael Bowes-Lyon (1893–1953), was the fifth son of Claude Bowes-Lyon, 14th
Earl of Strathmore and Kinghorne and Cecilia Bowes-Lyon, Countess of Strathmore and Kinghorne (née Cavendish-Bentinck).
Her mother, Elizabeth Margaret Cator (1899–1959), was a great-granddaughter of Charles Yorke, 4th Earl of Hardwicke.
She had a twin sister, Patricia Maud, later Lady Patricia Tetley, an older brother, Fergus Michael Claude, later Fergus Bowes-Lyon, 17th Earl of Strathmore and Kinghorne, and a younger brother, Michael Albemarle.
Lady Mary was also a godmother to Diana, Princess of Wales.
In 1949, a coming-out ball was held for her and her twin sister Patricia at Londonderry House, which was attended by their aunt, the Queen, and their cousins, The Princess Elizabeth and The Princess Margaret.
Marriage and children

On 10 November 1951 at St Bartholomew-the-Great in London, Mary married the then-Lieutenant Timothy Colman, son of the cricketer Geoffrey Colman.
Work and later life

In 1970, Mary was appointed an Extra Lady-in-waiting to another of the Queen's first cousins, Princess Alexandra, The Hon.
After her elder brother succeeded their cousin as 17th Earl of Strathmore and Kinghorne, she received the title and precedence of a daughter of an earl by royal warrant of precedence in 1974.
Lady Mary died at her home in Bixley, Norfolk on 2 January 2021, at the age of 88.



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
  AssignClass (e641c7ca-1561-424f-89d4-cfb1c06830cb)
 Call ID: e641c7ca-1561-424f-89d4-cfb1c06830cb
  Args:
    type: :Woman
    source: Mary_Cecilia_Bowes-Lyon
  AssignClass (91cd6443-c5d0-4974-b217-74e791020b32)
 Call ID: 91cd6443-c5d0-4974-b217-74e791020b32
  Args:
    type: :Person
    source: Mary_Cecilia_Bowes-Lyon
  AddLiteral (758ff7f7-43ba-4b77-9adc-147f374ca06c)
 Call ID: 758ff7f7-43ba-4b77-9adc-147f374ca06c
  Args:
    literal_type: xsd:integer
    source: Mary_Cecilia_Bowes-Lyon
    relation: :hasBirthYear
    literal_value: 1932
  AddLiteral (d62f8e52-2d81-4a25-a478-608dc57b35d6)
 Call ID: d62f8e52-2d81-4a25-a478-608dc57b35d6
  Args:
    literal_value: 2021
    relation: :hasDeathYear
    source: Mary_Cecilia_Bowes-Lyon
    literal_type: xsd:integer
  AssignClass (bf960dd0-08fd-40d4-b325-95fbc152b466)
 Call ID: bf960dd0-08fd-40d4-b325-95fbc152b466
  Args:
    source: Michael_Bowes-Lyon
    type: :Man
  AssignClass (15a90adb-15e3-41ba-affd-ec864fefcec0)
 Call ID: 15a90adb-15e3-41ba-affd-ec864fefcec0
  Args:
    source: Michael_Bowes-Lyon
    type: :Person
  AddLiteral (cb2501b1-c4ac-4ac0-afa0-c78ce81d8aa2)
 Call ID: cb2501b1-c4ac-4ac0-afa0-c78ce81d8aa2
  Args:
    literal_type: xsd:integer
    literal_value: 1893
    source: Michael_Bowes-Lyon
    relation: :hasBirthYear
  AddLiteral (ab5eb0c7-2f10-481c-a9dc-1162c56fa0c2)
 Call ID: ab5eb0c7-2f10-481c-a9dc-1162c56fa0c2
  Args:
    literal_value: 1953
    source: Michael_Bowes-Lyon
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (baf89f6d-838b-4870-885b-e97a2880a574)
 Call ID: baf89f6d-838b-4870-885b-e97a2880a574
  Args:
    type: :Woman
    source: Elizabeth_Margaret_Cator
  AssignClass (6eec825a-d97a-4663-9092-24a218cc9d06)
 Call ID: 6eec825a-d97a-4663-9092-24a218cc9d06
  Args:
    source: Elizabeth_Margaret_Cator
    type: :Person
  AddLiteral (6f54454a-8fe3-410e-92ac-5b8fae77fe44)
 Call ID: 6f54454a-8fe3-410e-92ac-5b8fae77fe44
  Args:
    literal_type: xsd:integer
    literal_value: 1899
    relation: :hasBirthYear
    source: Elizabeth_Margaret_Cator
  AddLiteral (798c863d-5eda-4e27-857e-3fd8ebee3c34)
 Call ID: 798c863d-5eda-4e27-857e-3fd8ebee3c34
  Args:
    relation: :hasDeathYear
    source: Elizabeth_Margaret_Cator
    literal_value: 1959
    literal_type: xsd:integer
  AddTriple (c3555eaa-7f01-4dad-944d-29abc198447d)
 Call ID: c3555eaa-7f01-4dad-944d-29abc198447d
  Args:
    source: Mary_Cecilia_Bowes-Lyon
    relation: :hasFather
    target: Michael_Bowes-Lyon
  AddTriple (ced697e3-a501-42d0-9500-e140b0b41996)
 Call ID: ced697e3-a501-42d0-9500-e140b0b41996
  Args:
    source: Mary_Cecilia_Bowes-Lyon
    relation: :hasMother
    target: Elizabeth_Margaret_Cator
  AssignClass (2b813158-c95a-4883-933a-84c0d7a7443a)
 Call ID: 2b813158-c95a-4883-933a-84c0d7a7443a
  Args:
    source: Claude_Bowes-Lyon
    type: :Man
  AssignClass (8a7d17ef-53b2-4b27-b78b-83d3ea3691d6)
 Call ID: 8a7d17ef-53b2-4b27-b78b-83d3ea3691d6
  Args:
    type: :Person
    source: Claude_Bowes-Lyon
  AssignClass (3fbaa0d0-a716-4ca2-b300-7825b2dce12b)
 Call ID: 3fbaa0d0-a716-4ca2-b300-7825b2dce12b
  Args:
    type: :Woman
    source: Cecilia_Bowes-Lyon
  AssignClass (6af57f83-d9eb-4867-a964-a12afddb53c5)
 Call ID: 6af57f83-d9eb-4867-a964-a12afddb53c5
  Args:
    source: Cecilia_Bowes-Lyon
    type: :Person
  AddTriple (f2277b5f-5d1c-47a2-b73c-97ac61d6636a)
 Call ID: f2277b5f-5d1c-47a2-b73c-97ac61d6636a
  Args:
    source: Michael_Bowes-Lyon
    relation: :hasFather
    target: Claude_Bowes-Lyon
  AddTriple (ad24271e-bbef-4f26-b30a-0cdf425f1163)
 Call ID: ad24271e-bbef-4f26-b30a-0cdf425f1163
  Args:
    source: Michael_Bowes-Lyon
    relation: :hasMother
    target: Cecilia_Bowes-Lyon
  AssignClass (fd2ab5a9-4684-4b24-81e0-c984167bb756)
 Call ID: fd2ab5a9-4684-4b24-81e0-c984167bb756
  Args:
    type: :Woman
    source: Patricia_Maud
  AssignClass (b2d7bf20-bfc1-4c6d-adf0-60a11c1f07d3)
 Call ID: b2d7bf20-bfc1-4c6d-adf0-60a11c1f07d3
  Args:
    type: :Person
    source: Patricia_Maud
  AssignClass (904c836e-7033-48ab-b2dd-524e99f5b23f)
 Call ID: 904c836e-7033-48ab-b2dd-524e99f5b23f
  Args:
    source: Fergus_Michael_Claude
    type: :Man
  AssignClass (9335a52f-05c8-4c2d-adb9-7fe5ff62e6a6)
 Call ID: 9335a52f-05c8-4c2d-adb9-7fe5ff62e6a6
  Args:
    type: :Person
    source: Fergus_Michael_Claude
  AssignClass (fd471e58-5a83-4354-ba63-3605d7b5ac61)
 Call ID: fd471e58-5a83-4354-ba63-3605d7b5ac61
  Args:
    source: Michael_Albemarle
    type: :Man
  AssignClass (e4ef9c50-d9c3-4851-8fe3-96bac72b8819)
 Call ID: e4ef9c50-d9c3-4851-8fe3-96bac72b8819
  Args:
    source: Michael_Albemarle
    type: :Person
  AddTriple (ebe3845f-a5bd-40d0-8598-a6abcc3948be)
 Call ID: ebe3845f-a5bd-40d0-8598-a6abcc3948be
  Args:
    source: Mary_Cecilia_Bowes-Lyon
    relation: :isSiblingOf
    target: Patricia_Maud
  AddTriple (94c2ecd1-c1ac-42b4-8a9d-d9efc3c7bcef)
 Call ID: 94c2ecd1-c1ac-42b4-8a9d-d9efc3c7bcef
  Args:
    source: Mary_Cecilia_Bowes-Lyon
    relation: :isSiblingOf
    target: Fergus_Michael_Claude
  AddTriple (2a222a92-17ac-493c-866c-f40aa4040bb5)
 Call ID: 2a222a92-17ac-493c-866c-f40aa4040bb5
  Args:
    source: Mary_Cecilia_Bowes-Lyon
    relation: :isSiblingOf
    target: Michael_Albemarle
  AssignClass (d2e93712-5491-4e12-8749-1b9eb9911fab)
 Call ID: d2e93712-5491-4e12-8749-1b9eb9911fab
  Args:
    type: :Man
    source: Timothy_Colman
  AssignClass (9d31961f-3f94-4ceb-ac23-2c12592dd986)
 Call ID: 9d31961f-3f94-4ceb-ac23-2c12592dd986
  Args:
    source: Timothy_Colman
    type: :Person
  AddLiteral (4bdd329b-a532-46c8-aedd-045a6614f214)
 Call ID: 4bdd329b-a532-46c8-aedd-045a6614f214
  Args:
    literal_value: 1951
    source: Mary_Cecilia_Bowes-Lyon
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AddTriple (4257818b-6361-4680-9406-bb610f0d1688)
 Call ID: 4257818b-6361-4680-9406-bb610f0d1688
  Args:
    source: Mary_Cecilia_Bowes-Lyon
    relation: :hasRelation
    target: Timothy_Colman
  AssignClass (ba7625df-9bca-4935-9f44-5af9bd5779f0)
 Call ID: ba7625df-9bca-4935-9f44-5af9bd5779f0
  Args:
    source: Geoffrey_Colman
    type: :Man
  AssignClass (3d1b2c92-d045-49e7-8c22-a7c49239e585)
 Call ID: 3d1b2c92-d045-49e7-8c22-a7c49239e585
  Args:
    type: :Person
    source: Geoffrey_Colman
  AddTriple (7b7cf4b5-ef88-49ee-8667-518db8c4154b)
 Call ID: 7b7cf4b5-ef88-49ee-8667-518db8c4154b
  Args:
    source: Timothy_Colman
    relation: :hasFather
    target: Geoffrey_Colman
  Finish (f9bfa399-3748-4031-8937-968d6cd6c50e)
 Call ID: f9bfa399-3748-4031-8937-968d6cd6c50e
  Args: