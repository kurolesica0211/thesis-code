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
Lady Davina Elizabeth Alice Benedikte Windsor (born 19 November 1977) is a member of the British royal family, and is the elder daughter of the Duke and Duchess of Gloucester.
She was known as Lady Davina Lewis between 2004 and 2018, during her marriage to Gary Lewis.
Early life and education

Davina Elizabeth Alice Benedikte Windsor was born on 19 November 1977 at St Mary's Hospital, London, the second child of Prince Richard, Duke of Gloucester and Birgitte, Duchess of Gloucester.
Her godparents are Captain Mark Phillips, the Duke of Buccleuch, Elisabeth, Lady Camoys, Susan Wigley, Roger Wellesley Smith and Caroline, Baroness Rosenørn-Lehn.
Lady Davina grew up in Kensington Palace.
Marriage and children

On 31 July 2004, Davina married Gary Christie Lewis (born 15 August 1970), a Māori.
Lewis is also the first person of known Māori descent to marry a member of the royal family, or to marry the daughter of a British prince.
As she is a legitimate descendant in the male line of George V and in line to the British throne, the Royal Marriages Act 1772 required that Royal Assent to the wedding be obtained in advance for the marriage to be legal and the descendants thereof to inherit rights of succession to the thrones of the Commonwealth realms, including that of New Zealand.
The wedding took place on 31 July 2004 at the private chapel of Kensington Palace, Davina's childhood home.
Apart from the Duke and Duchess of Gloucester and the bride's siblings, no other members of the royal family were present at the wedding; only close friends and family were involved.
Davina and her former husband have a daughter, Senna Kowhai, who was born on 22 June 2010 and a son, Tāne Mahuta, who was born 25 May 2012.
Davina was also stepmother to Lewis's son from a previous relationship, Ari (born 1992).
Davina does not carry out official functions but does attend family events including royal weddings.
Davina and Gary Lewis were invited to attend the Queen's reception for members of the New Zealand All Blacks at Buckingham Palace in 2005.
She and her then husband also attended Prince William's wedding in 2011.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (f4471e31-c583-4307-883b-75797dd7cff6)
 Call ID: f4471e31-c583-4307-883b-75797dd7cff6
  Args:
    type: :Woman
    source: Lady_Davina_Windsor
  AssignClass (c208252e-56bd-4585-85aa-c9294cbf58e1)
 Call ID: c208252e-56bd-4585-85aa-c9294cbf58e1
  Args:
    type: :Person
    source: Lady_Davina_Windsor
  AddLiteral (e9caa955-b682-44fc-8607-8891975de45e)
 Call ID: e9caa955-b682-44fc-8607-8891975de45e
  Args:
    source: Lady_Davina_Windsor
    relation: :hasBirthYear
    literal_value: 1977
    literal_type: xsd:integer
  AddLiteral (7188bafd-5e8b-4c81-a519-07e4faad30a1)
 Call ID: 7188bafd-5e8b-4c81-a519-07e4faad30a1
  Args:
    literal_value: Lady Davina Lewis
    relation: :alsoKnownAs
    literal_type: xsd:string
    source: Lady_Davina_Windsor
  AssignClass (94a270ea-7c0d-4c30-b64d-6442b8bad883)
 Call ID: 94a270ea-7c0d-4c30-b64d-6442b8bad883
  Args:
    type: :Man
    source: Prince_Richard_Duke_of_Gloucester
  AssignClass (6a1bde81-2808-4064-80b4-00e97e8f29b8)
 Call ID: 6a1bde81-2808-4064-80b4-00e97e8f29b8
  Args:
    source: Prince_Richard_Duke_of_Gloucester
    type: :Person
  AssignClass (a0f74782-5f34-44d5-84c6-e2d23f7a737b)
 Call ID: a0f74782-5f34-44d5-84c6-e2d23f7a737b
  Args:
    source: Birgitte_Duchess_of_Gloucester
    type: :Woman
  AssignClass (dfff597b-d8b6-47c0-a126-2288add4f918)
 Call ID: dfff597b-d8b6-47c0-a126-2288add4f918
  Args:
    type: :Person
    source: Birgitte_Duchess_of_Gloucester
  AddTriple (439f54ca-4809-4e29-8c21-17c73b9f2709)
 Call ID: 439f54ca-4809-4e29-8c21-17c73b9f2709
  Args:
    target: Prince_Richard_Duke_of_Gloucester
    relation: :hasFather
    source: Lady_Davina_Windsor
  AddTriple (273b2c90-f027-4bdf-a357-f485e1074a56)
 Call ID: 273b2c90-f027-4bdf-a357-f485e1074a56
  Args:
    target: Birgitte_Duchess_of_Gloucester
    relation: :hasMother
    source: Lady_Davina_Windsor
  AssignClass (7179c997-8e54-42f0-96f4-a671c9d11a05)
 Call ID: 7179c997-8e54-42f0-96f4-a671c9d11a05
  Args:
    type: :Man
    source: Gary_Christie_Lewis
  AssignClass (c555b4da-7bad-4b1e-a851-e0c7f959d641)
 Call ID: c555b4da-7bad-4b1e-a851-e0c7f959d641
  Args:
    type: :Person
    source: Gary_Christie_Lewis
  AddLiteral (c2a74324-3c5f-4e10-8e07-208550282beb)
 Call ID: c2a74324-3c5f-4e10-8e07-208550282beb
  Args:
    source: Gary_Christie_Lewis
    relation: :hasBirthYear
    literal_value: 1970
    literal_type: xsd:integer
  AddLiteral (6b2080c9-32e4-46ef-b3c9-8bb48cdcc640)
 Call ID: 6b2080c9-32e4-46ef-b3c9-8bb48cdcc640
  Args:
    literal_type: xsd:integer
    literal_value: 2004
    relation: :hasMarriageYear
    source: Lady_Davina_Windsor
  AddTriple (fa761181-dc4a-42ef-a8a6-0861f2612202)
 Call ID: fa761181-dc4a-42ef-a8a6-0861f2612202
  Args:
    source: Lady_Davina_Windsor
    target: Gary_Christie_Lewis
    relation: :hasRelation
  AssignClass (f77aa6f4-467b-4171-a919-9cca1b3c65d7)
 Call ID: f77aa6f4-467b-4171-a919-9cca1b3c65d7
  Args:
    type: :Woman
    source: Senna_Kowhai
  AssignClass (e6ee1edc-9c27-455c-b2ce-9193e3d5aefc)
 Call ID: e6ee1edc-9c27-455c-b2ce-9193e3d5aefc
  Args:
    source: Senna_Kowhai
    type: :Person
  AddTriple (f0f7913f-1e14-4441-bc07-e086fbf4a229)
 Call ID: f0f7913f-1e14-4441-bc07-e086fbf4a229
  Args:
    source: Senna_Kowhai
    target: Lady_Davina_Windsor
    relation: :isDaughterOf
  AddTriple (b436cf7d-af56-47fa-9509-593853389a49)
 Call ID: b436cf7d-af56-47fa-9509-593853389a49
  Args:
    target: Gary_Christie_Lewis
    relation: :isDaughterOf
    source: Senna_Kowhai
  AssignClass (c96e46e2-d793-4c8d-88b6-f1d8a5c56310)
 Call ID: c96e46e2-d793-4c8d-88b6-f1d8a5c56310
  Args:
    source: Tane_Mahuta
    type: :Man
  AssignClass (ec66ed75-374e-416b-940c-0450fdd58ee5)
 Call ID: ec66ed75-374e-416b-940c-0450fdd58ee5
  Args:
    type: :Person
    source: Tane_Mahuta
  AddTriple (e77738c3-96a4-4af8-9125-f35d71914eb3)
 Call ID: e77738c3-96a4-4af8-9125-f35d71914eb3
  Args:
    source: Tane_Mahuta
    relation: :isSonOf
    target: Lady_Davina_Windsor
  AddTriple (fbc498f6-9fd5-48e8-ac27-37df8848f121)
 Call ID: fbc498f6-9fd5-48e8-ac27-37df8848f121
  Args:
    target: Gary_Christie_Lewis
    relation: :isSonOf
    source: Tane_Mahuta
  AssignClass (a7a4b18f-032a-4b9d-ade7-243d874fa255)
 Call ID: a7a4b18f-032a-4b9d-ade7-243d874fa255
  Args:
    source: Ari
    type: :Man
  AssignClass (d2ff02fe-d9ff-407b-821b-f53d7832bfb4)
 Call ID: d2ff02fe-d9ff-407b-821b-f53d7832bfb4
  Args:
    type: :Person
    source: Ari
  AddLiteral (3fd5e7ae-02b4-4166-b774-c1c919025351)
 Call ID: 3fd5e7ae-02b4-4166-b774-c1c919025351
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1992
    source: Ari
  AddTriple (986a7c6a-302e-43d2-aa74-b5c1e19df02e)
 Call ID: 986a7c6a-302e-43d2-aa74-b5c1e19df02e
  Args:
    relation: :isSonOf
    target: Gary_Christie_Lewis
    source: Ari
  Finish (5cf82543-28e8-4730-a18c-c6744859525b)
 Call ID: 5cf82543-28e8-4730-a18c-c6744859525b
  Args: