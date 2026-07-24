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
Princess Josephine of Denmark, Countess of Monpezat RE (Josephine Sophia Ivalo Mathilda; born 8 January 2011) is a member of the Danish royal family.
She is the fourth and youngest child of King Frederik X and Queen Mary, and the seventh grandchild of Queen Margrethe II and Prince Henrik.
She is the twin sister of Prince Vincent.
Josephine is fourth in line to the Danish throne, after her older siblings, Crown Prince Christian and Princess Isabella, and her elder twin brother, Prince Vincent.
Birth and christening

Queen Margrethe II


Josephine was born on 8 January 2011 at Rigshospitalet, the Copenhagen University Hospital, in Copenhagen, at 10:56 am local time, 26 minutes after her twin brother.
Josephine and Vincent were baptised on 14 April at the Church of Holmen in central Copenhagen by the royal confessor, the Bishop of Copenhagen Erik Norman Svendsen.
The twins were baptised at the royal baptismal font which has been used for the baptism of royal children in Denmark since 1671.
Princess Josephine wore a christening gown found among her great-grandmother Queen Ingrid's belongings, making her the first child of a future Danish monarch not to wear the Danish royal family's traditional christening gown (which was worn by her twin brother) since it was taken into use in 1870.
The Princess's name was announced as Josephine Sophia Ivalo Mathilda.
Her godparents are her paternal aunt, Princess Marie of Denmark; her maternal aunt, Patricia Bailey; as well as her parents' friends Prince Carlo, Duke of Castro, Count Bendt Wedell, Birgitte Handwerk and Josephine Rechner.
Public appearances and education

On 3 August 2014, during the family's official visit to Greenland, Josephine, her parents and siblings, took part in a tree planting in Qaqortoq's new poplar grove, Ivalos og Miniks Poppellund, named after Josephine and her brother who are known by their Greenlandic middle names in Greenland.
On 15 August 2017, Josephine and her twin brother started school at Tranegårdsskolen in Gentofte – the same public school as her older siblings.
In August 2023, the Royal House announced that Josephine would be starting at Kildegård Privatskole in Hellerup in September 2023.
Both Josephine and her twin brother were confirmed on 18 April 2026.
Titles, styles, and honours

Josephine is styled as Her Royal Highness Princess Josephine of Denmark, Countess of Monpezat.



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
  AssignClass (56f370cf-4cbc-4fc6-8019-ff369e81b1a9)
 Call ID: 56f370cf-4cbc-4fc6-8019-ff369e81b1a9
  Args:
    source: Princess_Josephine_of_Denmark
    type: :Woman
  AssignClass (59903630-928f-4f92-b5ba-4ff2fd56ca7b)
 Call ID: 59903630-928f-4f92-b5ba-4ff2fd56ca7b
  Args:
    source: Princess_Josephine_of_Denmark
    type: :Person
  AddLiteral (882d3153-6cd5-4213-a388-913f9613b67a)
 Call ID: 882d3153-6cd5-4213-a388-913f9613b67a
  Args:
    literal_type: xsd:integer
    literal_value: 2011
    source: Princess_Josephine_of_Denmark
    relation: :hasBirthYear
  AssignClass (978a670f-fc88-4fcb-893f-3c7aca3a6f3b)
 Call ID: 978a670f-fc88-4fcb-893f-3c7aca3a6f3b
  Args:
    type: :Man
    source: King_Frederik_X
  AssignClass (f8557727-170a-4ae3-aa15-a1a116d41bd5)
 Call ID: f8557727-170a-4ae3-aa15-a1a116d41bd5
  Args:
    source: King_Frederik_X
    type: :Person
  AssignClass (70a4a03b-bd99-47ac-b2e7-e95c7b899641)
 Call ID: 70a4a03b-bd99-47ac-b2e7-e95c7b899641
  Args:
    source: Queen_Mary
    type: :Woman
  AssignClass (e007207f-f5c1-4ece-a8c5-56e266ec531c)
 Call ID: e007207f-f5c1-4ece-a8c5-56e266ec531c
  Args:
    type: :Person
    source: Queen_Mary
  AddTriple (2e0fe437-734e-45ca-bb10-f27098ed401f)
 Call ID: 2e0fe437-734e-45ca-bb10-f27098ed401f
  Args:
    source: Princess_Josephine_of_Denmark
    relation: :isChildOf
    target: King_Frederik_X
  AddTriple (8a35ca53-fb8a-4308-8107-dc6151b461d5)
 Call ID: 8a35ca53-fb8a-4308-8107-dc6151b461d5
  Args:
    relation: :isChildOf
    target: Queen_Mary
    source: Princess_Josephine_of_Denmark
  AssignClass (20c4490d-fadd-4657-8b23-983fb1240354)
 Call ID: 20c4490d-fadd-4657-8b23-983fb1240354
  Args:
    source: Prince_Vincent
    type: :Man
  AssignClass (3efe5fa6-b4cf-468f-815f-97bb2ebc10bc)
 Call ID: 3efe5fa6-b4cf-468f-815f-97bb2ebc10bc
  Args:
    source: Prince_Vincent
    type: :Person
  AddTriple (bffe3743-8c62-4e69-a027-a6839e653dc5)
 Call ID: bffe3743-8c62-4e69-a027-a6839e653dc5
  Args:
    source: Princess_Josephine_of_Denmark
    relation: :isSiblingOf
    target: Prince_Vincent
  AddTriple (1de3b5a1-1ea0-473d-bead-d1832a764326)
 Call ID: 1de3b5a1-1ea0-473d-bead-d1832a764326
  Args:
    source: Prince_Vincent
    relation: :isChildOf
    target: King_Frederik_X
  AddTriple (a43b4817-9dd2-45ff-bd10-9b03d47ca0f3)
 Call ID: a43b4817-9dd2-45ff-bd10-9b03d47ca0f3
  Args:
    relation: :isChildOf
    target: Queen_Mary
    source: Prince_Vincent
  AssignClass (4385f890-579e-4215-837b-f30a87d0342f)
 Call ID: 4385f890-579e-4215-837b-f30a87d0342f
  Args:
    type: :Man
    source: Crown_Prince_Christian
  AssignClass (631ddc78-3f8d-475f-9dc3-d2e3dc80eb5a)
 Call ID: 631ddc78-3f8d-475f-9dc3-d2e3dc80eb5a
  Args:
    source: Crown_Prince_Christian
    type: :Person
  AssignClass (839bda38-c395-43e6-9be8-e7d81844ef3a)
 Call ID: 839bda38-c395-43e6-9be8-e7d81844ef3a
  Args:
    source: Princess_Isabella
    type: :Woman
  AssignClass (f1c509b8-70cd-4c04-bcd1-4b16d753f7e7)
 Call ID: f1c509b8-70cd-4c04-bcd1-4b16d753f7e7
  Args:
    source: Princess_Isabella
    type: :Person
  AddTriple (26555ac7-6be7-4827-96f9-710e1c863c9f)
 Call ID: 26555ac7-6be7-4827-96f9-710e1c863c9f
  Args:
    source: Princess_Josephine_of_Denmark
    target: Crown_Prince_Christian
    relation: :isSiblingOf
  AddTriple (c5cf8637-160a-4bd1-b827-51f8854bb093)
 Call ID: c5cf8637-160a-4bd1-b827-51f8854bb093
  Args:
    target: Princess_Isabella
    relation: :isSiblingOf
    source: Princess_Josephine_of_Denmark
  AssignClass (466ae634-8161-4297-b4a3-612de6e843c3)
 Call ID: 466ae634-8161-4297-b4a3-612de6e843c3
  Args:
    type: :Woman
    source: Queen_Margrethe_II
  AssignClass (1fca6844-eeea-4b63-aac3-1aff07edd1d0)
 Call ID: 1fca6844-eeea-4b63-aac3-1aff07edd1d0
  Args:
    source: Queen_Margrethe_II
    type: :Person
  AssignClass (8f2af0e1-f5ea-44a5-872f-fafd1988e9f6)
 Call ID: 8f2af0e1-f5ea-44a5-872f-fafd1988e9f6
  Args:
    source: Prince_Henrik
    type: :Man
  AssignClass (7468d686-3ec0-4995-bae4-9c7afcc8d710)
 Call ID: 7468d686-3ec0-4995-bae4-9c7afcc8d710
  Args:
    type: :Person
    source: Prince_Henrik
  Finish (bef69fc2-8b26-4c21-9880-be6d2c741332)
 Call ID: bef69fc2-8b26-4c21-9880-be6d2c741332
  Args: