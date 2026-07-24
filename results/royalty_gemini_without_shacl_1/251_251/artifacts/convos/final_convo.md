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
Captain George Louis Victor Henry Serge Mountbatten, 2nd Marquess of Milford Haven (6 November 1892 – 8 April 1938), born Prince George of Battenberg, styled Earl of Medina between 1917 and 1921, was a Royal Navy officer and the elder son of Louis Mountbatten, 1st Marquess of Milford Haven (Prince Louis of Battenberg), and Princess Victoria of Hesse and by Rhine.
Biography

George was born 6 November 1892 in Darmstadt in the Grand Duchy of Hesse, then ruled by his maternal uncle Ernest Louis, Grand Duke of Hesse.
From birth, he was a prince of the Hessian royal family, albeit of a morganatic branch.
His siblings were Princess Alice (mother of Prince Philip, Duke of Edinburgh, to whom he was a mentor in Philip's adolescence), Queen Louise of Sweden and Louis Mountbatten, 1st
Earl Mountbatten of Burma (who assumed the role of Philip's mentor after George's death).
George followed his father into the Royal Navy, and after passing out from the Royal Naval College at Dartmouth, was promoted to sub-lieutenant on 15 January 1913.
In 1917, his father and several of his relations relinquished their German names, styles and titles in exchange for British peerages at the behest of George V. Accordingly, Prince George dropped the style of Serene Highness and his surname was anglicised to "Mountbatten."
When his father was created Marquess of Milford Haven in late 1917, George received the courtesy title of Earl of Medina, succeeding to his father's peerage after his death in September 1921.
Lord Milford Haven, as George was now known, remained in the Royal Navy after the war; he was promoted to lieutenant-commander on 15 February 1922 and to commander on 31 December 1926.
An accomplished mathematician, the Marquess "could work out complicated gunnery problems in his head" and "read books on calculus casually on trains".
Marriage and issue

Prince George of Battenberg, as he then was known, married Countess Nadejda Mikhailovna de Torby (daughter of Russian Grand Duke Michael Mikhailovich Romanov and his morganatic wife, Countess Sophie von Merenberg) on 15 November 1916 at the Russian Embassy, Welbeck Street, London.
They lived at Lynden Manor at Holyport in Berkshire and had two children:


Death

Lord Milford Haven died in London on 8 April 1938 of bone marrow cancer, aged 45.
His funeral took place at St Michael's Church, Bray, Berkshire, and he was buried in Bray Parish Cemetery.
Legacy to the British Museum

Lord Milford Haven left a collection of pornography, including artificial sex organs, to the British Museum.



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
  AssignClass (802ea49e-4d1d-440a-95e7-13d843675585)
 Call ID: 802ea49e-4d1d-440a-95e7-13d843675585
  Args:
    type: :Man
    source: George_Mountbatten
  AssignClass (e4630b73-b5c2-4339-8b81-7e7e3d80e011)
 Call ID: e4630b73-b5c2-4339-8b81-7e7e3d80e011
  Args:
    type: :Person
    source: George_Mountbatten
  AssignClass (0949f0b3-f717-4776-b327-d37a3bdd42d9)
 Call ID: 0949f0b3-f717-4776-b327-d37a3bdd42d9
  Args:
    type: :Man
    source: Louis_Mountbatten_1st_Marquess
  AssignClass (64ea2d90-c0d5-476c-b69f-1bc8c0134e50)
 Call ID: 64ea2d90-c0d5-476c-b69f-1bc8c0134e50
  Args:
    type: :Person
    source: Louis_Mountbatten_1st_Marquess
  AssignClass (2da628c1-d9a1-4e0c-96dd-a12fb40db9af)
 Call ID: 2da628c1-d9a1-4e0c-96dd-a12fb40db9af
  Args:
    type: :Woman
    source: Victoria_of_Hesse_and_by_Rhine
  AssignClass (15e7539c-e626-4860-bc8e-d033e33f8ac7)
 Call ID: 15e7539c-e626-4860-bc8e-d033e33f8ac7
  Args:
    type: :Person
    source: Victoria_of_Hesse_and_by_Rhine
  AddLiteral (bdbf83b0-2248-4d5c-b1ec-74826dc89674)
 Call ID: bdbf83b0-2248-4d5c-b1ec-74826dc89674
  Args:
    literal_type: xsd:integer
    source: George_Mountbatten
    literal_value: 1892
    relation: :hasBirthYear
  AddLiteral (3159434a-d6d2-4ae9-b4cd-4504c9f5fe50)
 Call ID: 3159434a-d6d2-4ae9-b4cd-4504c9f5fe50
  Args:
    source: George_Mountbatten
    relation: :hasDeathYear
    literal_value: 1938
    literal_type: xsd:integer
  AddTriple (cf9e6bf4-a7ab-45f4-b551-6905c57a8ae3)
 Call ID: cf9e6bf4-a7ab-45f4-b551-6905c57a8ae3
  Args:
    target: Louis_Mountbatten_1st_Marquess
    source: George_Mountbatten
    relation: :hasFather
  AddTriple (7cdfcf9a-013a-43de-b290-866639326aca)
 Call ID: 7cdfcf9a-013a-43de-b290-866639326aca
  Args:
    target: Victoria_of_Hesse_and_by_Rhine
    source: George_Mountbatten
    relation: :hasMother
  AssignClass (8fd93a99-4049-4f19-962b-ccdc6fc8ee00)
 Call ID: 8fd93a99-4049-4f19-962b-ccdc6fc8ee00
  Args:
    type: :Woman
    source: Princess_Alice
  AssignClass (0de65f72-4eb5-49ee-a124-8dc62f6739c8)
 Call ID: 0de65f72-4eb5-49ee-a124-8dc62f6739c8
  Args:
    type: :Person
    source: Princess_Alice
  AssignClass (90db4ca6-cd48-49fd-ac17-e86eae789b64)
 Call ID: 90db4ca6-cd48-49fd-ac17-e86eae789b64
  Args:
    type: :Woman
    source: Queen_Louise_of_Sweden
  AssignClass (58abd7e7-730c-40b7-be21-689437585a9f)
 Call ID: 58abd7e7-730c-40b7-be21-689437585a9f
  Args:
    type: :Person
    source: Queen_Louise_of_Sweden
  AssignClass (1b81e6aa-d0fc-46f0-82ef-3321640cebef)
 Call ID: 1b81e6aa-d0fc-46f0-82ef-3321640cebef
  Args:
    type: :Man
    source: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
  AssignClass (231c0e5e-896b-4f82-a004-dad81c4f5688)
 Call ID: 231c0e5e-896b-4f82-a004-dad81c4f5688
  Args:
    type: :Person
    source: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
  AddTriple (d586eaf1-ab48-4241-b6da-4e8595e25ff1)
 Call ID: d586eaf1-ab48-4241-b6da-4e8595e25ff1
  Args:
    source: George_Mountbatten
    target: Princess_Alice
    relation: :isSiblingOf
  AddTriple (506af37f-dccc-4f57-b955-92b0631cb437)
 Call ID: 506af37f-dccc-4f57-b955-92b0631cb437
  Args:
    relation: :isSiblingOf
    target: Queen_Louise_of_Sweden
    source: George_Mountbatten
  AddTriple (966193c9-83ad-4611-ab61-85d084b62f96)
 Call ID: 966193c9-83ad-4611-ab61-85d084b62f96
  Args:
    relation: :isSiblingOf
    source: George_Mountbatten
    target: Louis_Mountbatten_1st_Earl_Mountbatten_of_Burma
  AssignClass (d552978a-ece6-4e26-a9bb-95566370677a)
 Call ID: d552978a-ece6-4e26-a9bb-95566370677a
  Args:
    type: :Woman
    source: Nadejda_Mikhailovna_de_Torby
  AssignClass (a37f7044-1307-46a3-b298-d08abefcc811)
 Call ID: a37f7044-1307-46a3-b298-d08abefcc811
  Args:
    type: :Person
    source: Nadejda_Mikhailovna_de_Torby
  AddLiteral (c9ee71a3-2577-460b-9c03-c84105252a7d)
 Call ID: c9ee71a3-2577-460b-9c03-c84105252a7d
  Args:
    relation: :hasMarriageYear
    literal_value: 1916
    source: George_Mountbatten
    literal_type: xsd:integer
  AddTriple (729e39f9-b32b-48b1-a07a-c175ab6cf55e)
 Call ID: 729e39f9-b32b-48b1-a07a-c175ab6cf55e
  Args:
    relation: :hasRelation
    target: Nadejda_Mikhailovna_de_Torby
    source: George_Mountbatten
  AssignClass (bf82df2c-3ecf-465c-a60a-66e1235df847)
 Call ID: bf82df2c-3ecf-465c-a60a-66e1235df847
  Args:
    type: :Man
    source: Michael_Mikhailovich_Romanov
  AssignClass (1a4b8b60-56a2-4511-ba6d-3064b52170cd)
 Call ID: 1a4b8b60-56a2-4511-ba6d-3064b52170cd
  Args:
    type: :Person
    source: Michael_Mikhailovich_Romanov
  AssignClass (835ab8e1-e539-439d-8a47-1839051d6864)
 Call ID: 835ab8e1-e539-439d-8a47-1839051d6864
  Args:
    type: :Woman
    source: Sophie_von_Merenberg
  AssignClass (fbc703dc-dc49-4225-83fb-daac93184b0e)
 Call ID: fbc703dc-dc49-4225-83fb-daac93184b0e
  Args:
    type: :Person
    source: Sophie_von_Merenberg
  AddTriple (03921595-3a20-4511-ba35-2a9b9e94a5e8)
 Call ID: 03921595-3a20-4511-ba35-2a9b9e94a5e8
  Args:
    relation: :hasFather
    source: Nadejda_Mikhailovna_de_Torby
    target: Michael_Mikhailovich_Romanov
  AddTriple (e871673b-a33f-4b4f-9757-35ca4b873bcf)
 Call ID: e871673b-a33f-4b4f-9757-35ca4b873bcf
  Args:
    relation: :hasMother
    target: Sophie_von_Merenberg
    source: Nadejda_Mikhailovna_de_Torby
  Finish (78608370-4722-4378-b047-9d0121e9bef3)
 Call ID: 78608370-4722-4378-b047-9d0121e9bef3
  Args: