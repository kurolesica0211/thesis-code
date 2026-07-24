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
Lieutenant David Michael Mountbatten, 3rd Marquess of Milford Haven, OBE, DSC (12 May 1919 – 14 April 1970), styled Viscount Alderney before 1921 and Earl of Medina between 1921 and 1938, was the son of George Mountbatten, 2nd Marquess of Milford Haven and Countess Nadejda Mikhailovna of Torby.
Early years and education

David Michael Mountbatten was born on 12 May 1919.
He was the only son of George Mountbatten, 2nd Marquess of Milford Haven (who had been born as Prince George of Battenberg), and Russian Countess Nadejda (Nada) Torby, who were married in 1916.
His paternal grandparents were Prince Louis of Battenberg and Princess Victoria of Hesse and by Rhine.
Therefore, he was a great-great-grandson of Queen Victoria.
He grew up at the family home in Holyport, Berkshire, and enjoyed a close friendship with his first cousin Prince Philip of Greece and Denmark, later the Duke of Edinburgh.
He served as best man to the prince at his marriage in November 1947 to the Princess Elizabeth, later Queen Elizabeth II.
Upon the death of his father on 8 April 1938, he became the 3rd Marquess of Milford Haven and head of the House of Mountbatten.
Navy and postwar social life

During the Second World War Milford Haven served in the Royal Navy.
He then played a prominent part in the London demi-monde of the 1950s, which brought together a colourful mix of aristocrats and shadowy social climbers like osteopath Stephen Ward.
Marriages

Milford Haven was married twice:


Death

Milford Haven died of a heart attack, aged 50, on 14 April 1970 in London.
His ashes were buried in the Battenberg Chapel at St. Mildred's Church, Whippingham, on the Isle of Wight (photo).



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
  AssignClass (77e40b9d-bcd6-4395-89f5-0f8718a5fe1d)
 Call ID: 77e40b9d-bcd6-4395-89f5-0f8718a5fe1d
  Args:
    type: :Man
    source: :David_Michael_Mountbatten
  AssignClass (49f7c84b-51eb-4c02-a16a-1b5ed66a1339)
 Call ID: 49f7c84b-51eb-4c02-a16a-1b5ed66a1339
  Args:
    type: :Person
    source: :David_Michael_Mountbatten
  AddLiteral (77a67972-c1f7-4c30-9eed-22a38e127aa9)
 Call ID: 77a67972-c1f7-4c30-9eed-22a38e127aa9
  Args:
    relation: :hasBirthYear
    literal_value: 1919
    source: :David_Michael_Mountbatten
    literal_type: xsd:integer
  AddLiteral (f3f249e0-e269-4090-947a-bde39fcb33bb)
 Call ID: f3f249e0-e269-4090-947a-bde39fcb33bb
  Args:
    source: :David_Michael_Mountbatten
    literal_value: 1970
    relation: :hasDeathYear
    literal_type: xsd:integer
  AssignClass (ae5fbb92-8f5b-4d36-88de-b97156702111)
 Call ID: ae5fbb92-8f5b-4d36-88de-b97156702111
  Args:
    type: :Man
    source: :George_Mountbatten
  AssignClass (1e1862f8-e328-4c54-9217-2ed0813de49d)
 Call ID: 1e1862f8-e328-4c54-9217-2ed0813de49d
  Args:
    source: :George_Mountbatten
    type: :Person
  AssignClass (036f92c0-8067-46f2-b041-ed0c192ef50f)
 Call ID: 036f92c0-8067-46f2-b041-ed0c192ef50f
  Args:
    type: :Woman
    source: :Nadejda_Mikhailovna_of_Torby
  AssignClass (6c91579b-ef3b-4cd6-ab26-3da466e717e7)
 Call ID: 6c91579b-ef3b-4cd6-ab26-3da466e717e7
  Args:
    source: :Nadejda_Mikhailovna_of_Torby
    type: :Person
  AddTriple (abe1112a-51a2-44d6-bd0c-9d8f53cfb8fc)
 Call ID: abe1112a-51a2-44d6-bd0c-9d8f53cfb8fc
  Args:
    target: :George_Mountbatten
    relation: :hasFather
    source: :David_Michael_Mountbatten
  AddTriple (e3d73f81-b6c6-4cef-a0e0-3210cfea7b85)
 Call ID: e3d73f81-b6c6-4cef-a0e0-3210cfea7b85
  Args:
    relation: :hasMother
    source: :David_Michael_Mountbatten
    target: :Nadejda_Mikhailovna_of_Torby
  AddLiteral (c36fd48c-8db7-45ec-a87c-4453007dfb52)
 Call ID: c36fd48c-8db7-45ec-a87c-4453007dfb52
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1916
    source: :George_Mountbatten
  AddTriple (09207a3f-353d-4936-979c-dca19b42f59d)
 Call ID: 09207a3f-353d-4936-979c-dca19b42f59d
  Args:
    relation: :hasRelation
    source: :George_Mountbatten
    target: :Nadejda_Mikhailovna_of_Torby
  AssignClass (2227fade-a658-4aac-87bd-d88dd49447db)
 Call ID: 2227fade-a658-4aac-87bd-d88dd49447db
  Args:
    source: :Prince_Louis_of_Battenberg
    type: :Man
  AssignClass (79dc8058-25f4-477b-a6fb-ee39aef407f1)
 Call ID: 79dc8058-25f4-477b-a6fb-ee39aef407f1
  Args:
    source: :Prince_Louis_of_Battenberg
    type: :Person
  AssignClass (8267e1c9-d62f-429e-9318-4b389d360429)
 Call ID: 8267e1c9-d62f-429e-9318-4b389d360429
  Args:
    source: :Princess_Victoria_of_Hesse_and_by_Rhine
    type: :Woman
  AssignClass (d5d3640e-cbd8-4e6b-ae0b-cba3adfc95ab)
 Call ID: d5d3640e-cbd8-4e6b-ae0b-cba3adfc95ab
  Args:
    source: :Princess_Victoria_of_Hesse_and_by_Rhine
    type: :Person
  AddTriple (f81f1528-6f21-415f-be16-15aadd39bbec)
 Call ID: f81f1528-6f21-415f-be16-15aadd39bbec
  Args:
    source: :George_Mountbatten
    relation: :hasFather
    target: :Prince_Louis_of_Battenberg
  AddTriple (48eda16c-3f95-436e-8586-1e76763c0e0f)
 Call ID: 48eda16c-3f95-436e-8586-1e76763c0e0f
  Args:
    relation: :hasMother
    source: :George_Mountbatten
    target: :Princess_Victoria_of_Hesse_and_by_Rhine
  AssignClass (5aa5a2e9-db80-4ced-82da-a6b9e0123914)
 Call ID: 5aa5a2e9-db80-4ced-82da-a6b9e0123914
  Args:
    type: :Man
    source: :Prince_Philip_of_Greece_and_Denmark
  AssignClass (68bcf6bc-443e-4556-aa06-bc8f321e6891)
 Call ID: 68bcf6bc-443e-4556-aa06-bc8f321e6891
  Args:
    source: :Prince_Philip_of_Greece_and_Denmark
    type: :Person
  AddTriple (424c47f9-a305-4f53-8ed7-357b005cd051)
 Call ID: 424c47f9-a305-4f53-8ed7-357b005cd051
  Args:
    target: :Prince_Philip_of_Greece_and_Denmark
    source: :David_Michael_Mountbatten
    relation: :hasRelation
  Finish (5c1b45de-6bf1-409d-9888-70f2d693c9b9)
 Call ID: 5c1b45de-6bf1-409d-9888-70f2d693c9b9
  Args: