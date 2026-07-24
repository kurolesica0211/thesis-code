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


Prince Nikolaos of Greece and Denmark (Greek: Νικόλαος Ντε Γκρες, romanized: Nikólaos de Grèce; born 1 October 1969) is the third child of Constantine II and Anne-Marie, who were the last King and Queen of Greece, from 1964 to 1973.
Early life and education

Nikolaos was born at Casa di Cura Privata Nuova Villa Claudia in Rome, Italy, on October 1, 1969.
He is the first royal child to be born in hospital from Constantine II of Greece and Anne-Marie of Denmark.
His godparents were Queen Sofía, Queen of Spain (his paternal aunt), Princess Irene of Greece and Denmark (another paternal aunt), Margareta of Romania (his paternal second cousin), and Crown Prince Alexander of Yugoslavia (another paternal second cousin).
He is a member of board of the Anna-Maria Foundation, designed to help victims of natural disasters like floods and earthquakes in Greece.
Nikolaos has an older sister Princess Alexia, an older brother Crown Prince Pavlos, a younger sister Princess Theodora, and a younger brother, Prince Philippos.
Personal life

Relationships

The engagement of Nikolaos to Tatiana Ellinka Blatnik, with whom he had been in a long-term relationship, was announced on 28 December 2009 by the office of King Constantine in London.
On 25 August 2010, the couple married at the Orthodox Church of St. Nicholas in Spetses, Greece.
In January 2025, Nikolaos became engaged to Chrysí Vardinogiánni, daughter of Greek businessman Giórgos Vardinogiánnis and Agapi Politi.
Citizenship

Οn 20 December 2024, Nikolaos along with other members of the former royal family acquired Greek citizenship, under the surname de Grèce.



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
  AssignClass (db81bb52-0cb2-40e1-a060-7e6da8c5d6c6)
 Call ID: db81bb52-0cb2-40e1-a060-7e6da8c5d6c6
  Args:
    type: :Woman
    source: :Anne-Marie
  AssignClass (5e4c3cb9-6e62-492b-aae6-388cd90f975e)
 Call ID: 5e4c3cb9-6e62-492b-aae6-388cd90f975e
  Args:
    type: :Woman
    source: :SofiaOfSpain
  AssignClass (c6229a8f-cfec-46d2-9997-b8fcec6e13f5)
 Call ID: c6229a8f-cfec-46d2-9997-b8fcec6e13f5
  Args:
    type: :Woman
    source: :Marina
  AssignClass (714ce0a4-e724-4afd-aed5-6f36691cf29f)
 Call ID: 714ce0a4-e724-4afd-aed5-6f36691cf29f
  Args:
    type: :Man
    source: :Michael
  AssignClass (2c339cfe-8b6b-43f4-aae6-4d79263e7239)
 Call ID: 2c339cfe-8b6b-43f4-aae6-4d79263e7239
  Args:
    type: :Man
    source: :NikolaosOfGreeceAndDenmark
  AssignClass (19947ac9-fa8c-439f-83cd-a7aca937131b)
 Call ID: 19947ac9-fa8c-439f-83cd-a7aca937131b
  Args:
    type: :Man
    source: :ConstantineII
  AssignClass (be9ce4c9-fbd6-4adb-8687-a8241ee94d93)
 Call ID: be9ce4c9-fbd6-4adb-8687-a8241ee94d93
  Args:
    type: :Woman
    source: :IreneOfGreeceAndDenmark
  AssignClass (c33a1f86-bd24-4951-8fe0-b0b478afa603)
 Call ID: c33a1f86-bd24-4951-8fe0-b0b478afa603
  Args:
    type: :Woman
    source: :MargaretaOfRomania
  AssignClass (ec581757-1ea5-4240-9407-b99e93133812)
 Call ID: ec581757-1ea5-4240-9407-b99e93133812
  Args:
    type: :Man
    source: :AlexanderOfYugoslavia
  AssignClass (c3bc7405-05af-4fb3-a4a6-00c543b5fa11)
 Call ID: c3bc7405-05af-4fb3-a4a6-00c543b5fa11
  Args:
    type: :Woman
    source: :Alexia
  AssignClass (d2fa6800-a6f5-485e-96ae-66f66aee6d5d)
 Call ID: d2fa6800-a6f5-485e-96ae-66f66aee6d5d
  Args:
    type: :Man
    source: :Pavlos
  AssignClass (00a994ff-b606-412d-9e19-e9555b2deae3)
 Call ID: 00a994ff-b606-412d-9e19-e9555b2deae3
  Args:
    type: :Woman
    source: :Theodora
  AssignClass (0197f788-e136-4bec-9c4d-7a13e47a7790)
 Call ID: 0197f788-e136-4bec-9c4d-7a13e47a7790
  Args:
    type: :Man
    source: :Philippos
  AssignClass (6b2d8b32-52b0-466b-b88d-28899f8ff3c3)
 Call ID: 6b2d8b32-52b0-466b-b88d-28899f8ff3c3
  Args:
    type: :Woman
    source: :TatianaEllinkaBlatnik
  AssignClass (d6a63a4b-f71a-494a-9de0-f8d7cb869fab)
 Call ID: d6a63a4b-f71a-494a-9de0-f8d7cb869fab
  Args:
    type: :Woman
    source: :ChrysiVardinogianni
  AssignClass (4c2f2349-35b8-4134-b472-7e6413b9837f)
 Call ID: 4c2f2349-35b8-4134-b472-7e6413b9837f
  Args:
    type: :Man
    source: :GiorgosVardinogiannis
  AssignClass (a1e6e548-cf50-4013-8464-6043dda37b3d)
 Call ID: a1e6e548-cf50-4013-8464-6043dda37b3d
  Args:
    type: :Woman
    source: :AgapiPoliti
  AddLiteral (1bf18c6d-d547-4b5d-9761-e9b7a6b2a783)
 Call ID: 1bf18c6d-d547-4b5d-9761-e9b7a6b2a783
  Args:
    source: :NikolaosOfGreeceAndDenmark
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1969
  AddTriple (33360791-9962-4e15-a429-e56b102cdbc2)
 Call ID: 33360791-9962-4e15-a429-e56b102cdbc2
  Args:
    relation: :hasFather
    target: :ConstantineII
    source: :NikolaosOfGreeceAndDenmark
  AddTriple (37a17c4e-e44b-48c2-bf09-7e1e9fe33d0c)
 Call ID: 37a17c4e-e44b-48c2-bf09-7e1e9fe33d0c
  Args:
    relation: :hasMother
    target: :Anne-Marie
    source: :NikolaosOfGreeceAndDenmark
  AddTriple (13b72c7c-6542-4013-9a0e-beeed12b0f57)
 Call ID: 13b72c7c-6542-4013-9a0e-beeed12b0f57
  Args:
    source: :NikolaosOfGreeceAndDenmark
    target: :Alexia
    relation: :hasSister
  AddTriple (422c070b-7c35-4591-8753-4c1ab01605e4)
 Call ID: 422c070b-7c35-4591-8753-4c1ab01605e4
  Args:
    target: :Pavlos
    source: :NikolaosOfGreeceAndDenmark
    relation: :hasBrother
  AddTriple (7c60d4e5-3f5c-4bb1-8112-8d3bca6b6e80)
 Call ID: 7c60d4e5-3f5c-4bb1-8112-8d3bca6b6e80
  Args:
    relation: :hasSister
    source: :NikolaosOfGreeceAndDenmark
    target: :Theodora
  AddTriple (e61130be-8197-4c88-b157-1770812efae2)
 Call ID: e61130be-8197-4c88-b157-1770812efae2
  Args:
    source: :NikolaosOfGreeceAndDenmark
    target: :Philippos
    relation: :hasBrother
  AddTriple (61a8f25a-4170-4dc9-b876-52aa3ce829d7)
 Call ID: 61a8f25a-4170-4dc9-b876-52aa3ce829d7
  Args:
    relation: :hasFather
    target: :GiorgosVardinogiannis
    source: :ChrysiVardinogianni
  AddTriple (88484005-2e3b-4c3e-890e-659cc3c4c52c)
 Call ID: 88484005-2e3b-4c3e-890e-659cc3c4c52c
  Args:
    target: :AgapiPoliti
    source: :ChrysiVardinogianni
    relation: :hasMother
  AddTriple (6be3c6b3-c77e-43bb-878c-c7f298581e41)
 Call ID: 6be3c6b3-c77e-43bb-878c-c7f298581e41
  Args:
    source: :NikolaosOfGreeceAndDenmark
    target: :TatianaEllinkaBlatnik
    relation: :hasRelation
  AddTriple (d7850e59-2eb2-4930-974c-6a4369685ded)
 Call ID: d7850e59-2eb2-4930-974c-6a4369685ded
  Args:
    source: :NikolaosOfGreeceAndDenmark
    target: :ChrysiVardinogianni
    relation: :hasRelation
  AddTriple (ff98ef4c-83dd-417d-b89e-b23ab0863954)
 Call ID: ff98ef4c-83dd-417d-b89e-b23ab0863954
  Args:
    relation: :hasRelation
    source: :Michael
    target: :Marina
  Finish (6f42e297-50b4-4919-b30a-71fa600da1e2)
 Call ID: 6f42e297-50b4-4919-b30a-71fa600da1e2
  Args: