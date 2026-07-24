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
George Ivar Louis Mountbatten, 4th Marquess of Milford Haven (born 6 June 1961), styled Earl of Medina before 1970, is a British hereditary peer and businessman.
Biography

Family

Born on 6 June 1961, Lord Milford Haven is the elder son of the 3rd Marquess of Milford Haven and Janet Mercedes Bryce, the older brother of Lord Ivar Mountbatten, and a descendant of Queen Victoria, Catherine the Great, Alexander Pushkin, and Abram Gannibal.
Upon the death of his father on 14 April 1970, he became the 4th Marquess of Milford Haven and head of the Mountbatten family.
Lord Milford Haven married, first, Sarah Georgina Walker (born London, Middlesex, 17 November 1961/2), in London on 8 March 1989.
She is the daughter of Jean Maureen (née Hatton) and George Alfred Walker.
Lord Milford Haven and Walker had two children:


The couple divorced on 27 February 1996.
In June 2016, Walker married Michael Spencer, Lord Spencer of Alresford.
Lord Milford Haven subsequently married Clare Husted Steel at Coatue Point in Nantucket, Massachusetts, on 20 August 1997.
Career

In 2000, Lord Milford Haven founded uSwitch, a website to help consumers compare and change suppliers of various services.
Lord Milford Haven won the Queen's Cup with the Broncos team in 1988 and he reached the final in 2006.



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
  AssignClass (b2a5f737-1be1-40e6-92ba-95363601ef93)
 Call ID: b2a5f737-1be1-40e6-92ba-95363601ef93
  Args:
    source: George_Ivar_Louis_Mountbatten
    type: :Man
  AssignClass (8c8224af-fb88-405b-bcca-dce14d324439)
 Call ID: 8c8224af-fb88-405b-bcca-dce14d324439
  Args:
    source: George_Ivar_Louis_Mountbatten
    type: :Person
  AddLiteral (7334b6d5-05bf-4fa4-a980-3de57e855c91)
 Call ID: 7334b6d5-05bf-4fa4-a980-3de57e855c91
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: George_Ivar_Louis_Mountbatten
    literal_value: 1961
  AssignClass (2b6e8c0e-7eb8-4d74-b039-300fb5742c49)
 Call ID: 2b6e8c0e-7eb8-4d74-b039-300fb5742c49
  Args:
    source: 3rd_Marquess_of_Milford_Haven
    type: :Man
  AssignClass (4c53fad3-337c-4d5f-854f-b100f9972560)
 Call ID: 4c53fad3-337c-4d5f-854f-b100f9972560
  Args:
    source: 3rd_Marquess_of_Milford_Haven
    type: :Person
  AssignClass (3d7e762f-ba14-42f1-8aa5-e18fe010c26d)
 Call ID: 3d7e762f-ba14-42f1-8aa5-e18fe010c26d
  Args:
    type: :Woman
    source: Janet_Mercedes_Bryce
  AssignClass (47710aab-0ace-4c2d-9d50-18d415d15777)
 Call ID: 47710aab-0ace-4c2d-9d50-18d415d15777
  Args:
    type: :Person
    source: Janet_Mercedes_Bryce
  AddTriple (33e4af94-6f9c-4e70-b537-46ed60857a5a)
 Call ID: 33e4af94-6f9c-4e70-b537-46ed60857a5a
  Args:
    target: 3rd_Marquess_of_Milford_Haven
    source: George_Ivar_Louis_Mountbatten
    relation: :hasFather
  AddTriple (d1ff365e-bce1-43e9-acc5-77bb93197486)
 Call ID: d1ff365e-bce1-43e9-acc5-77bb93197486
  Args:
    target: Janet_Mercedes_Bryce
    relation: :hasMother
    source: George_Ivar_Louis_Mountbatten
  AssignClass (33bb66be-0a09-4594-9806-ad843dbebf16)
 Call ID: 33bb66be-0a09-4594-9806-ad843dbebf16
  Args:
    type: :Man
    source: Lord_Ivar_Mountbatten
  AssignClass (4f6db04c-68fd-4bb7-8ffb-a3b3bc0ae643)
 Call ID: 4f6db04c-68fd-4bb7-8ffb-a3b3bc0ae643
  Args:
    source: Lord_Ivar_Mountbatten
    type: :Person
  AddTriple (7eef8100-6775-44f1-88d6-018811df76a3)
 Call ID: 7eef8100-6775-44f1-88d6-018811df76a3
  Args:
    relation: :hasBrother
    source: George_Ivar_Louis_Mountbatten
    target: Lord_Ivar_Mountbatten
  AssignClass (7b635163-0ca3-4062-b4a2-7760f9903066)
 Call ID: 7b635163-0ca3-4062-b4a2-7760f9903066
  Args:
    type: :Woman
    source: Sarah_Georgina_Walker
  AssignClass (d719ed77-ccfc-4522-9ba3-e438b1a53578)
 Call ID: d719ed77-ccfc-4522-9ba3-e438b1a53578
  Args:
    source: Sarah_Georgina_Walker
    type: :Person
  AddLiteral (efe4afdd-ed3a-478f-b00c-17044f9f4f70)
 Call ID: efe4afdd-ed3a-478f-b00c-17044f9f4f70
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    source: George_Ivar_Louis_Mountbatten
    literal_value: 1989
  AssignClass (9c848534-40de-4b01-a521-df1bde035ddf)
 Call ID: 9c848534-40de-4b01-a521-df1bde035ddf
  Args:
    type: :Woman
    source: Jean_Maureen_Hatton
  AssignClass (b62a24fc-9ea6-4ca2-9489-52e6f532034f)
 Call ID: b62a24fc-9ea6-4ca2-9489-52e6f532034f
  Args:
    type: :Person
    source: Jean_Maureen_Hatton
  AssignClass (64926c25-792b-4a8b-8b85-f106e9075f29)
 Call ID: 64926c25-792b-4a8b-8b85-f106e9075f29
  Args:
    type: :Man
    source: George_Alfred_Walker
  AssignClass (2df7c29e-37b9-4ea7-999f-5f4fdd3a9756)
 Call ID: 2df7c29e-37b9-4ea7-999f-5f4fdd3a9756
  Args:
    source: George_Alfred_Walker
    type: :Person
  AddTriple (6c586900-ae97-4c9f-858a-8e10250bdb9e)
 Call ID: 6c586900-ae97-4c9f-858a-8e10250bdb9e
  Args:
    relation: :hasMother
    source: Sarah_Georgina_Walker
    target: Jean_Maureen_Hatton
  AddTriple (176f579f-89fa-41a2-9a55-7480402cddb2)
 Call ID: 176f579f-89fa-41a2-9a55-7480402cddb2
  Args:
    target: George_Alfred_Walker
    relation: :hasFather
    source: Sarah_Georgina_Walker
  AssignClass (eaa31ad9-e59e-4f8a-b76f-674147705205)
 Call ID: eaa31ad9-e59e-4f8a-b76f-674147705205
  Args:
    type: :Man
    source: Michael_Spencer
  AssignClass (5272ef01-5dc0-4339-9410-ad90fff3043c)
 Call ID: 5272ef01-5dc0-4339-9410-ad90fff3043c
  Args:
    type: :Person
    source: Michael_Spencer
  AssignClass (c032b5fc-6e89-4f23-b284-7ecbf373f715)
 Call ID: c032b5fc-6e89-4f23-b284-7ecbf373f715
  Args:
    type: :Woman
    source: Clare_Husted_Steel
  AssignClass (136e389a-be40-46c1-9c7d-a6558ffaee9a)
 Call ID: 136e389a-be40-46c1-9c7d-a6558ffaee9a
  Args:
    type: :Person
    source: Clare_Husted_Steel
  AddLiteral (7384056a-85f2-4268-89fe-6e1d4bec38ce)
 Call ID: 7384056a-85f2-4268-89fe-6e1d4bec38ce
  Args:
    literal_value: 1997
    source: George_Ivar_Louis_Mountbatten
    relation: :hasMarriageYear
    literal_type: xsd:integer
  Finish (bd4eafe2-94e2-49f1-a532-259d6f0486a2)
 Call ID: bd4eafe2-94e2-49f1-a532-259d6f0486a2
  Args: