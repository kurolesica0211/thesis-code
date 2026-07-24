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
The Crown PrinceThe Crown Princess


Princess Tomislav


Princess Alexander


Princess Elizabeth


Princess Katarina of Yugoslavia, Lady de Silva (born 28 November 1959) is an English businessperson specialising in etiquette and decorum courses.
Early life

Katarina was born at King’s College Hospital in London to Princess Margarita of Baden and Prince Tomislav of Yugoslavia.
Her father's dynasty having been deposed and banished from Yugoslavia after World War II, she grew up in exile, largely in England.
She has one brother, Prince Nikola of Yugoslavia, and two half-brothers, Prince George and Prince Michael.
She is a first cousin of Alexander, Crown Prince of Yugoslavia.
Her grandmother, Princess Theodora, Margravine of Baden, was the sister of Prince Philip, Duke of Edinburgh, late husband of Queen Elizabeth II.
Princess Katharina is the senior female-line descendant of Queen Victoria, through the Queen's second daughter Alice, Grand Duchess of Hesse, who was the grandmother of Princess Katharina's great-grandmother, Princess Alice of Battenberg.
Career

In 1978, Katarina was presented as a debutante to high society at the International Debutante Ball at the Waldorf-Astoria Hotel.
As of 2013, Katarina and former Royal butler Grant Harrold develop and sell etiquette and decorum classes.
Personal life

Katarina married barrister Sir Desmond de Silva on 5 December 1987.
They had one daughter, Victoria Marie Esmé Margarita, born on 6 September 1991.
Charity work

In 2009, Katarina supported the charity Project Change: Bermuda to raise funds towards building a hospital and training medical staff in Burundi.
Katarina served as the president of the Guild of Travel and Tourism in the United Kingdom.
In 2013, she became patron of the Society of Genealogists succeeding Prince Michael of Kent.
Honours

Ancestry

Katarina is a member of the House of Karađorđević.
Through her father, Katarina descends from kings Nicholas I of Montenegro, Ferdinand I of Romania, and furthermore from Emperor Nicholas I of Russia, King Ferdinand II and Queen Maria II of Portugal, and Queen Victoria of the United Kingdom of Great Britain and Ireland.
Through her mother, Katarina descends from Leopold, Grand Duke of Baden, kings George V of Hanover, Christian IX of Denmark, George I of Greece and Nicholas I, Emperor of Russia.



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
  AssignClass (e40bfcc7-5944-4f71-9280-c0fa14b8dc84)
 Call ID: e40bfcc7-5944-4f71-9280-c0fa14b8dc84
  Args:
    source: PrincessKatarinaOfYugoslavia
    type: :Woman
  AssignClass (c63c15c5-2825-440a-8d78-97a20466ed2d)
 Call ID: c63c15c5-2825-440a-8d78-97a20466ed2d
  Args:
    type: :Person
    source: PrincessKatarinaOfYugoslavia
  AssignClass (0b005569-8d17-49ac-9869-d26af1f03818)
 Call ID: 0b005569-8d17-49ac-9869-d26af1f03818
  Args:
    source: PrincessMargaritaOfBaden
    type: :Woman
  AssignClass (f78a7bb0-733d-42d2-96bd-cc54def54981)
 Call ID: f78a7bb0-733d-42d2-96bd-cc54def54981
  Args:
    type: :Person
    source: PrincessMargaritaOfBaden
  AssignClass (b8c93026-7177-415e-ac62-4054dd1bbd2d)
 Call ID: b8c93026-7177-415e-ac62-4054dd1bbd2d
  Args:
    source: PrinceTomislavOfYugoslavia
    type: :Man
  AssignClass (6fbc9715-c4c2-4e0b-befd-696034b2b091)
 Call ID: 6fbc9715-c4c2-4e0b-befd-696034b2b091
  Args:
    type: :Person
    source: PrinceTomislavOfYugoslavia
  AssignClass (1e6a2eca-abc8-41d6-8cf9-2644d1e7020a)
 Call ID: 1e6a2eca-abc8-41d6-8cf9-2644d1e7020a
  Args:
    type: :Man
    source: PrinceNikolaOfYugoslavia
  AssignClass (ea028e42-780c-429c-8b38-492756419492)
 Call ID: ea028e42-780c-429c-8b38-492756419492
  Args:
    source: PrinceNikolaOfYugoslavia
    type: :Person
  AssignClass (62ff8cd6-bc10-411c-a5b7-9362d43c9431)
 Call ID: 62ff8cd6-bc10-411c-a5b7-9362d43c9431
  Args:
    source: PrinceGeorge
    type: :Man
  AssignClass (2dc53b69-9d7e-4212-8692-db13da77ab5b)
 Call ID: 2dc53b69-9d7e-4212-8692-db13da77ab5b
  Args:
    source: PrinceGeorge
    type: :Person
  AssignClass (f8ba79f0-83dc-42cc-97c7-0f3d415983aa)
 Call ID: f8ba79f0-83dc-42cc-97c7-0f3d415983aa
  Args:
    type: :Man
    source: PrinceMichael
  AssignClass (adbfb91d-da0b-4ba8-a3de-9063f0eb9a35)
 Call ID: adbfb91d-da0b-4ba8-a3de-9063f0eb9a35
  Args:
    type: :Person
    source: PrinceMichael
  AssignClass (4492842f-7d63-4622-bc11-8bf46b5980c2)
 Call ID: 4492842f-7d63-4622-bc11-8bf46b5980c2
  Args:
    source: SirDesmondDeSilva
    type: :Man
  AssignClass (667ccae6-0dcc-4cd7-9cec-f95c9f28eb39)
 Call ID: 667ccae6-0dcc-4cd7-9cec-f95c9f28eb39
  Args:
    source: SirDesmondDeSilva
    type: :Person
  AssignClass (766e3e49-9bed-47ea-ab84-25179c3fc92e)
 Call ID: 766e3e49-9bed-47ea-ab84-25179c3fc92e
  Args:
    source: VictoriaMarieEsmeMargarita
    type: :Woman
  AssignClass (afab40d0-aeb5-4131-8f7c-862285648bc9)
 Call ID: afab40d0-aeb5-4131-8f7c-862285648bc9
  Args:
    type: :Person
    source: VictoriaMarieEsmeMargarita
  AddLiteral (ecdcded3-a715-413c-86dc-5d65ae12d209)
 Call ID: ecdcded3-a715-413c-86dc-5d65ae12d209
  Args:
    source: PrincessKatarinaOfYugoslavia
    literal_type: xsd:string
    literal_value: 1959-11-28
    relation: :hasBirthYear
  AddTriple (28491408-6662-4ede-8d6e-38e5d7c73a20)
 Call ID: 28491408-6662-4ede-8d6e-38e5d7c73a20
  Args:
    relation: :hasMother
    target: PrincessMargaritaOfBaden
    source: PrincessKatarinaOfYugoslavia
  AddTriple (c3e56eb9-85eb-4aec-abd4-1eef006f6c76)
 Call ID: c3e56eb9-85eb-4aec-abd4-1eef006f6c76
  Args:
    target: PrinceTomislavOfYugoslavia
    source: PrincessKatarinaOfYugoslavia
    relation: :hasFather
  AddTriple (c9f518b4-8c1f-46c1-a0be-777da9f510f1)
 Call ID: c9f518b4-8c1f-46c1-a0be-777da9f510f1
  Args:
    relation: :isBrotherOf
    target: PrincessKatarinaOfYugoslavia
    source: PrinceNikolaOfYugoslavia
  AddTriple (d0b402a2-c372-4631-b113-0ffad8c068ed)
 Call ID: d0b402a2-c372-4631-b113-0ffad8c068ed
  Args:
    target: PrincessKatarinaOfYugoslavia
    source: PrinceGeorge
    relation: :isBrotherOf
  AddTriple (8c8776f6-474d-4c69-a3da-6a675472a673)
 Call ID: 8c8776f6-474d-4c69-a3da-6a675472a673
  Args:
    relation: :isBrotherOf
    target: PrincessKatarinaOfYugoslavia
    source: PrinceMichael
  AddLiteral (5f401d06-bfd1-44fb-a90c-25ba7d1f85e2)
 Call ID: 5f401d06-bfd1-44fb-a90c-25ba7d1f85e2
  Args:
    literal_type: xsd:string
    literal_value: 1987
    source: PrincessKatarinaOfYugoslavia
    relation: :hasMarriageYear
  AddTriple (03eeb848-ce74-4f6d-b3b2-0d93e337402c)
 Call ID: 03eeb848-ce74-4f6d-b3b2-0d93e337402c
  Args:
    target: SirDesmondDeSilva
    source: PrincessKatarinaOfYugoslavia
    relation: :hasRelation
  AddTriple (9a47d815-00ac-4ca9-a9b6-66ccb961a098)
 Call ID: 9a47d815-00ac-4ca9-a9b6-66ccb961a098
  Args:
    relation: :hasMother
    target: PrincessKatarinaOfYugoslavia
    source: VictoriaMarieEsmeMargarita
  AddTriple (d3e02fda-d38b-495f-87fc-4ecaa3514e9f)
 Call ID: d3e02fda-d38b-495f-87fc-4ecaa3514e9f
  Args:
    target: SirDesmondDeSilva
    source: VictoriaMarieEsmeMargarita
    relation: :hasFather
  AddLiteral (ddcd6351-713b-4dcf-aeb8-5caf105f4dfa)
 Call ID: ddcd6351-713b-4dcf-aeb8-5caf105f4dfa
  Args:
    relation: :hasBirthYear
    source: VictoriaMarieEsmeMargarita
    literal_type: xsd:string
    literal_value: 1991-09-06
  Finish (1a8c9bc5-51d7-4d43-81ee-28b9545dd3e2)
 Call ID: 1a8c9bc5-51d7-4d43-81ee-28b9545dd3e2
  Args: